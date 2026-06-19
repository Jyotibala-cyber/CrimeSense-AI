import pandas as pd
import openpyxl
from datetime import datetime
from database import SessionLocal, engine
from models import Base, CrimeStat, CrimeIncident

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "..", "dataset", "indian-crimes-from-jan-to-aug-2025.csv")
XLTX_PATH = os.path.join(BASE_DIR, "..", "dataset", "data.xltx")

CITY_COORDS = {
    "Agra": (27.1767, 78.0081), "Ahmedabad": (23.0225, 72.5714),
    "Bangalore": (12.9716, 77.5946), "Bhopal": (23.2599, 77.4126),
    "Chennai": (13.0827, 80.2707), "Delhi": (28.7041, 77.1025),
    "Faridabad": (28.4089, 77.3178), "Ghaziabad": (28.6692, 77.4538),
    "Hyderabad": (17.3850, 78.4867), "Indore": (22.7196, 75.8577),
    "Jaipur": (26.9124, 75.7873), "Kalyan": (19.2350, 73.1290),
    "Kanpur": (26.4499, 80.3319), "Kolkata": (22.5726, 88.3639),
    "Lucknow": (26.8467, 80.9462), "Ludhiana": (30.9010, 75.8573),
    "Meerut": (28.9845, 77.7064), "Mumbai": (19.0760, 72.8777),
    "Nagpur": (21.1458, 79.0882), "Nashik": (19.9975, 73.7898),
    "Patna": (25.5941, 85.1376), "Pune": (18.5204, 73.8567),
    "Rajkot": (22.3039, 70.8022), "Srinagar": (34.0837, 74.7973),
    "Surat": (21.1702, 72.8311), "Thane": (19.2183, 72.9781),
    "Vadodara": (22.3072, 73.1812), "Varanasi": (25.3176, 82.9739),
    "Visakhapatnam": (17.6868, 83.2185),
}

SEVERITY_MAP = {
    "HOMICIDE": "Critical", "SEXUAL ASSAULT": "Critical", "KIDNAPPING": "High",
    "ARSON": "High", "ROBBERY": "High", "ASSAULT": "High", "BURGLARY": "Medium",
    "EXTORTION": "Medium", "FIREARM OFFENSE": "Medium", "DRUG OFFENSE": "Medium",
    "DOMESTIC VIOLENCE": "Medium", "IDENTITY THEFT": "Medium", "FRAUD": "Medium",
    "CYBERCRIME": "Medium", "COUNTERFEITING": "Medium", "VANDALISM": "Low",
    "SHOPLIFTING": "Low", "TRAFFIC VIOLATION": "Low", "PUBLIC INTOXICATION": "Low",
    "ILLEGAL POSSESSION": "Medium",
}


def import_csv_stats():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(CrimeStat).limit(1).first() is not None:
        db.close()
        return
    if not os.path.exists(CSV_PATH):
        print(f"Skipping CSV import: file not found at {CSV_PATH}")
        db.close()
        return
    df = pd.read_csv(CSV_PATH).fillna("")
    records = []
    for _, row in df.iterrows():
        records.append(CrimeStat(
            law_category=str(row.iloc[0]).strip() if row.iloc[0] else "",
            crime_section=str(row.iloc[1]).strip() if row.iloc[1] else "",
            reason=str(row.iloc[2]).strip() if row.iloc[2] else "",
            cases_jan_aug_2025=int(row.iloc[3]) if str(row.iloc[3]).strip() else 0,
            cases_aug_2024=int(row.iloc[4]) if str(row.iloc[4]).strip() else 0,
            cases_jul_2025=int(row.iloc[5]) if str(row.iloc[5]).strip() else 0,
            cases_aug_2025=int(row.iloc[6]) if str(row.iloc[6]).strip() else 0,
        ))
    db.add_all(records)
    db.commit()
    count = len(records)
    db.close()
    print(f"Imported {count} crime stat records")


def import_xltx_incidents():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    xltx_crime_types = [
        "BURGLARY", "VANDALISM", "FRAUD", "DOMESTIC VIOLENCE", "FIREARM OFFENSE",
        "ROBBERY", "KIDNAPPING", "IDENTITY THEFT", "SEXUAL ASSAULT", "ASSAULT",
        "TRAFFIC VIOLATION", "PUBLIC INTOXICATION", "HOMICIDE", "CYBERCRIME",
        "ILLEGAL POSSESSION", "ARSON", "DRUG OFFENSE", "EXTORTION",
        "COUNTERFEITING", "VEHICLE - STOLEN", "SHOPLIFTING"
    ]
    has_xltx = db.query(CrimeIncident).filter(
        CrimeIncident.crime_type.in_(xltx_crime_types)
    ).limit(1).first() is not None
    if has_xltx:
        db.close()
        return
    if not os.path.exists(XLTX_PATH):
        print(f"Skipping XLTX import: file not found at {XLTX_PATH}")
        db.close()
        return

    wb = openpyxl.load_workbook(XLTX_PATH)
    ws = wb.active
    records = []
    batch_size = 500

    for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True), 1):
        try:
            report_no, date_reported, date_occurrence, time_occurrence, city, crime_code, crime_desc, age, gender, weapon, crime_domain, police_deployed, case_closed, date_closed = (row + (None,) * 14)[:14]
        except:
            continue

        city_name = str(city).strip() if city else "Unknown"
        coords = CITY_COORDS.get(city_name, (28.7041, 77.1025))

        crime_type = str(crime_desc).strip() if crime_desc else "Unknown"
        severity = SEVERITY_MAP.get(crime_type, "Medium")

        dt = None
        if date_occurrence:
            try:
                date_str = str(date_occurrence)[:10]
                time_val = time_occurrence
                time_str = None
                if time_val is not None:
                    t = str(time_val).strip()
                    if t not in ('None', '0', ''):
                        if len(t) >= 19 and t[10] == ' ':
                            time_str = t[11:19]
                        elif len(t) == 8 and t.count(':') == 2:
                            time_str = t
                if time_str:
                    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
                else:
                    dt = datetime.strptime(date_str, "%Y-%m-%d")
            except:
                pass
        if dt is None and date_reported:
            try:
                dt = datetime.strptime(str(date_reported)[:10], "%Y-%m-%d")
            except:
                pass
        if dt is None:
            dt = datetime.now()

        records.append(CrimeIncident(
            crime_type=crime_type,
            location_name=city_name,
            latitude=round(coords[0] + (hash(str(i)) % 100 - 50) * 0.002, 6),
            longitude=round(coords[1] + (hash(str(i * 7)) % 100 - 50) * 0.002, 6),
            date_time=dt,
            severity=severity,
            description=f"{crime_domain or ''} | Weapon: {weapon or 'None'} | Victim: {gender or 'Unknown'}/{age or '?'}",
        ))

        if i % batch_size == 0:
            db.add_all(records)
            db.commit()
            print(f"  Imported {i} incidents...")
            records = []

    if records:
        db.add_all(records)
        db.commit()

    total = i
    db.close()
    wb.close()
    print(f"Imported {total} crime incident records")


def import_csv():
    import_csv_stats()
    import_xltx_incidents()


if __name__ == "__main__":
    import_csv()
