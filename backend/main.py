from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from pydantic import BaseModel
from database import engine, get_db
from models import Base, CrimeIncident, CrimeStat
from seed_data import seed_database
from ai_engine import CrimeAnalysisEngine
from import_dataset import import_csv
import json
import csv
import io
import re
import traceback
import pandas as pd

import secrets
import hashlib

Base.metadata.create_all(bind=engine)

OFFICER_CREDENTIALS = {
    "inspector.singh": {"password": "crimsense@2025", "name": "Inspector Singh", "badge": "IPC-4421"},
    "officer.sharma": {"password": "crimsense@2025", "name": "Officer Sharma", "badge": "IPC-3312"},
    "admin": {"password": "admin@123", "name": "Admin Officer", "badge": "ADM-001"},
}

active_tokens: dict = {}

app = FastAPI(title="CrimeSense AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class IncidentCreate(BaseModel):
    crime_type: str
    location_name: str
    latitude: float
    longitude: float
    date_time: str
    severity: str = "Medium"
    description: str = ""


class IncidentResponse(BaseModel):
    id: int
    crime_type: str
    location_name: str
    latitude: float
    longitude: float
    date_time: datetime
    severity: str
    description: str | None = None

    class Config:
        from_attributes = True


@app.on_event("startup")
def startup():
    seed_database()
    try:
        import_csv()
    except Exception as e:
        print(f"Crime stat import skipped: {e}")


class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/api/auth/login")
def login(req: LoginRequest):
    officer = OFFICER_CREDENTIALS.get(req.username)
    if not officer:
        for cred in OFFICER_CREDENTIALS.values():
            if cred["badge"] == req.username:
                officer = cred
                break
    if not officer or officer["password"] != req.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = secrets.token_hex(32)
    active_tokens[token] = {
        "username": req.username,
        "name": officer["name"],
        "badge": officer["badge"],
    }
    return {"token": token, "name": officer["name"], "badge": officer["badge"]}

@app.post("/api/auth/verify")
def verify_token(authorization: str = Header("")):
    token = authorization.replace("Bearer ", "")
    info = active_tokens.get(token)
    if not info:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return info

@app.get("/")
def root():
    return {"message": "CrimeSense AI API", "docs": "/docs"}

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "CrimeSense AI"}


@app.get("/api/incidents", response_model=List[IncidentResponse])
def get_incidents(
    skip: int = 0,
    limit: int = 5000,
    search: str = "",
    crime_type: str = "",
    severity: str = "",
    location: str = "",
    db: Session = Depends(get_db),
):
    q = db.query(CrimeIncident)
    if search:
        like = f"%{search}%"
        q = q.filter(
            CrimeIncident.location_name.like(like) |
            CrimeIncident.crime_type.like(like)
        )
    if crime_type:
        q = q.filter(CrimeIncident.crime_type == crime_type)
    if severity:
        q = q.filter(CrimeIncident.severity == severity)
    if location:
        q = q.filter(CrimeIncident.location_name.like(f"%{location}%"))
    incidents = q.order_by(CrimeIncident.date_time.desc()).offset(skip).limit(limit).all()
    return incidents


@app.post("/api/incidents")
def create_incident(incident: IncidentCreate, db: Session = Depends(get_db)):
    try:
        dt = datetime.fromisoformat(incident.date_time)
    except:
        dt = datetime.now()

    db_incident = CrimeIncident(
        crime_type=incident.crime_type,
        location_name=incident.location_name,
        latitude=incident.latitude,
        longitude=incident.longitude,
        date_time=dt,
        severity=incident.severity,
        description=incident.description,
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return {"message": "Incident recorded", "id": db_incident.id}


def parse_pdf_text(text: str) -> list[dict]:
    rows = []
    text = text.strip()

    try:
        parsed = json.loads(text)
        data = parsed if isinstance(parsed, list) else [parsed]
        for item in data:
            if isinstance(item, dict) and any(k in item for k in ['crime_type', 'location_name', 'latitude']):
                rows.append({
                    "crime_type": str(item.get("crime_type", "Unknown")),
                    "location_name": str(item.get("location_name", "Unknown")),
                    "latitude": float(item.get("latitude", 0)),
                    "longitude": float(item.get("longitude", 0)),
                    "date_time": str(item.get("date_time", "")),
                    "severity": str(item.get("severity", "Medium")),
                    "description": str(item.get("description", "")),
                })
        if rows:
            return rows
    except json.JSONDecodeError:
        pass

    lines = [l.strip() for l in text.split('\n') if l.strip()]
    if not lines:
        return rows

    csv_text = '\n'.join(lines)
    try:
        reader = csv.DictReader(io.StringIO(csv_text))
        for row in reader:
            if any(k in row for k in ['crime_type', 'location_name', 'latitude']):
                rows.append({
                    "crime_type": str(row.get("crime_type", row.get("Crime Type", "Unknown"))),
                    "location_name": str(row.get("location_name", row.get("Location", "Unknown"))),
                    "latitude": float(row.get("latitude", row.get("Latitude", 0))),
                    "longitude": float(row.get("longitude", row.get("Longitude", 0))),
                    "date_time": str(row.get("date_time", row.get("Date Time", ""))),
                    "severity": str(row.get("severity", row.get("Severity", "Medium"))),
                    "description": str(row.get("description", row.get("Description", ""))),
                })
        if rows:
            return rows
    except Exception:
        pass

    headers = re.split(r'\s{2,}|\t', lines[0]) if len(lines) > 1 else []
    if len(headers) >= 3:
        col_map = {}
        for h in headers:
            hl = h.lower().strip()
            if 'type' in hl: col_map['crime_type'] = h
            elif 'locat' in hl: col_map['location_name'] = h
            elif 'lat' in hl: col_map['latitude'] = h
            elif 'lon' in hl or 'lng' in hl: col_map['longitude'] = h
            elif 'date' in hl or 'time' in hl: col_map['date_time'] = h
            elif 'sever' in hl: col_map['severity'] = h
            elif 'desc' in hl: col_map['description'] = h

        if 'crime_type' in col_map:
            for line in lines[1:]:
                parts = re.split(r'\s{2,}|\t', line)
                if len(parts) >= len(headers):
                    row = dict(zip(headers, parts))
                    rows.append({
                        "crime_type": str(row.get(col_map.get('crime_type', ''), 'Unknown')),
                        "location_name": str(row.get(col_map.get('location_name', ''), 'Unknown')),
                        "latitude": float(row.get(col_map.get('latitude', ''), 0)),
                        "longitude": float(row.get(col_map.get('longitude', ''), 0)),
                        "date_time": str(row.get(col_map.get('date_time', ''), '')),
                        "severity": str(row.get(col_map.get('severity', ''), 'Medium')),
                        "description": str(row.get(col_map.get('description', ''), '')),
                    })

    if not rows:
        for line in lines:
            parts = [p.strip() for p in re.split(r',|\t', line) if p.strip()]
            if len(parts) >= 4:
                rows.append({
                    "crime_type": parts[0],
                    "location_name": parts[1],
                    "latitude": float(parts[2]) if parts[2].replace('.', '').replace('-', '').isdigit() else 0,
                    "longitude": float(parts[3]) if parts[3].replace('.', '').replace('-', '').isdigit() else 0,
                    "date_time": parts[4] if len(parts) > 4 else "",
                    "severity": parts[5] if len(parts) > 5 else "Medium",
                    "description": parts[6] if len(parts) > 6 else "",
                })

    return rows


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    count = 0
    rows = []

    if file.filename.endswith(".csv"):
        text = content.decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(text))
        for row in reader:
            rows.append(row)
    elif file.filename.endswith(".json"):
        data = json.loads(content)
        rows = data if isinstance(data, list) else [data]
    elif file.filename.endswith(".pdf"):
        try:
            import fitz
            doc = fitz.open(stream=content, filetype="pdf")
            full_text = ""
            for page in doc:
                full_text += page.get_text() + "\n"
            doc.close()
            rows = parse_pdf_text(full_text)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"PDF parsing failed: {str(e)}")
    elif file.filename.endswith((".xls", ".xlsx")):
        try:
            df = pd.read_excel(io.BytesIO(content), engine="openpyxl")
            df.columns = [c.lower().strip() for c in df.columns]
            col_map = {}
            for c in df.columns:
                if 'type' in c: col_map['crime_type'] = c
                elif 'locat' in c: col_map['location_name'] = c
                elif 'lat' in c: col_map['latitude'] = c
                elif 'lon' in c or 'lng' in c: col_map['longitude'] = c
                elif 'date' in c or 'time' in c: col_map['date_time'] = c
                elif 'sever' in c: col_map['severity'] = c
                elif 'desc' in c: col_map['description'] = c
            rows = []
            for _, r in df.iterrows():
                rows.append({
                    "crime_type": str(r.get(col_map.get('crime_type', ''), 'Unknown')),
                    "location_name": str(r.get(col_map.get('location_name', ''), 'Unknown')),
                    "latitude": float(r.get(col_map.get('latitude', ''), 0)),
                    "longitude": float(r.get(col_map.get('longitude', ''), 0)),
                    "date_time": str(r.get(col_map.get('date_time', ''), '')),
                    "severity": str(r.get(col_map.get('severity', ''), 'Medium')),
                    "description": str(r.get(col_map.get('description', ''), '')),
                })
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Excel parsing failed: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format. Use CSV, JSON, PDF, or XLS/XLSX.")

    for i, row in enumerate(rows, 1):
        try:
            dt = None
            dt_str = row.get("date_time") or row.get("Date Time") or ""
            for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"]:
                try:
                    dt = datetime.strptime(dt_str[:19], fmt)
                    break
                except:
                    pass
            if dt is None:
                dt = datetime.now()

            incident = CrimeIncident(
                crime_type=str(row.get("crime_type", row.get("Crime Type", "Unknown"))),
                location_name=str(row.get("location_name", row.get("Location", "Unknown"))),
                latitude=float(row.get("latitude", row.get("Latitude", 0))),
                longitude=float(row.get("longitude", row.get("Longitude", 0))),
                date_time=dt,
                severity=str(row.get("severity", row.get("Severity", "Medium"))),
                description=str(row.get("description", row.get("Description", ""))),
            )
            db.add(incident)
            count += 1
            if i % 500 == 0:
                db.commit()
        except Exception:
            pass

    db.commit()
    return {"message": f"Uploaded {count} incidents", "count": count}


@app.get("/api/analytics/summary")
def get_summary(db: Session = Depends(get_db)):
    engine = CrimeAnalysisEngine(db)
    return engine.get_summary_stats()


@app.get("/api/analytics/trends")
def get_trends(db: Session = Depends(get_db)):
    engine = CrimeAnalysisEngine(db)
    return engine.get_trend_data()


@app.get("/api/analytics/categories")
def get_categories(db: Session = Depends(get_db)):
    engine = CrimeAnalysisEngine(db)
    return engine.get_category_distribution()


@app.get("/api/analytics/hotspots")
def get_hotspots(db: Session = Depends(get_db)):
    engine = CrimeAnalysisEngine(db)
    return engine.detect_hotspots()


@app.get("/api/analytics/risk-zones")
def get_risk_zones(db: Session = Depends(get_db)):
    engine = CrimeAnalysisEngine(db)
    return engine.calculate_risk_zones()


@app.get("/api/predictions")
def get_predictions(db: Session = Depends(get_db)):
    engine = CrimeAnalysisEngine(db)
    return engine.generate_predictions()


@app.get("/api/alerts")
def get_alerts(db: Session = Depends(get_db)):
    engine = CrimeAnalysisEngine(db)
    return engine.get_alerts()


@app.get("/api/crime-stats")
def get_crime_stats(db: Session = Depends(get_db)):
    stats = db.query(CrimeStat).order_by(CrimeStat.law_category, CrimeStat.crime_section).all()
    return stats


@app.get("/api/crime-stats/summary")
def get_crime_stats_summary(db: Session = Depends(get_db)):
    from sqlalchemy import func
    rows = db.query(
        CrimeStat.law_category,
        CrimeStat.crime_section,
        func.sum(CrimeStat.cases_jan_aug_2025).label("total_jan_aug"),
        func.sum(CrimeStat.cases_aug_2025).label("total_aug"),
    ).group_by(CrimeStat.law_category, CrimeStat.crime_section).order_by(
        CrimeStat.law_category, CrimeStat.crime_section
    ).all()
    return [{
        "law_category": r.law_category,
        "crime_section": r.crime_section,
        "total_jan_aug_2025": int(r.total_jan_aug),
        "total_aug_2025": int(r.total_aug),
    } for r in rows]


@app.get("/api/geocode/search")
def geocode_search(q: str = ""):
    if not q or len(q.strip()) < 2:
        return []
    try:
        import requests
        resp = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": q, "format": "json", "limit": 6, "countrycodes": "IN"},
            headers={"User-Agent": "CrimeSenseAI/1.0"},
            timeout=10,
        )
        if resp.status_code == 200:
            results = resp.json()
            return [{
                "name": r.get("display_name", "").split(",")[0],
                "full_name": r.get("display_name", ""),
                "lat": float(r["lat"]),
                "lng": float(r["lon"]),
                "type": r.get("type", ""),
            } for r in results]
    except Exception as e:
        print(f"Geocode search error: {e}")
    return []


@app.get("/api/geocode")
def geocode_location(q: str = "", db: Session = Depends(get_db)):
    if not q:
        raise HTTPException(status_code=400, detail="Missing query parameter 'q'")
    name = q.strip().title()
    match = db.query(CrimeIncident).filter(CrimeIncident.location_name.like(f"%{name}%")).first()
    if match:
        return {"name": match.location_name, "lat": match.latitude, "lng": match.longitude, "source": "database"}
    try:
        import requests
        resp = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": q, "format": "json", "limit": 1},
            headers={"User-Agent": "CrimeSenseAI/1.0"},
            timeout=10,
        )
        if resp.status_code == 200 and len(resp.json()) > 0:
            data = resp.json()[0]
            return {"name": data.get("display_name", q), "lat": float(data["lat"]), "lng": float(data["lon"]), "source": "nominatim"}
    except Exception as e:
        print(f"Geocode error: {e}")
    raise HTTPException(status_code=404, detail=f"Location '{q}' not found")


@app.get("/api/locations")
def get_locations(db: Session = Depends(get_db)):
    from sqlalchemy import func
    rows = db.query(
        CrimeIncident.location_name,
        func.avg(CrimeIncident.latitude).label("lat"),
        func.avg(CrimeIncident.longitude).label("lng"),
        func.count(CrimeIncident.id).label("count"),
    ).group_by(CrimeIncident.location_name).order_by(CrimeIncident.location_name).all()
    return [{"name": r.location_name, "lat": round(float(r.lat), 6), "lng": round(float(r.lng), 6), "count": r.count} for r in rows]


@app.get("/api/crime-stats/categories")
def get_crime_stats_categories(db: Session = Depends(get_db)):
    from sqlalchemy import func
    rows = db.query(
        CrimeStat.law_category,
        func.sum(CrimeStat.cases_jan_aug_2025).label("total"),
    ).group_by(CrimeStat.law_category).all()
    total = sum(r.total for r in rows) or 1
    return [{"name": r.law_category, "total": int(r.total), "percentage": round(int(r.total) / total * 100, 1)} for r in rows]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
