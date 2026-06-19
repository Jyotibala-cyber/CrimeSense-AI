from datetime import datetime, timedelta
import random
import math
from database import SessionLocal, engine
from models import Base, CrimeIncident

CRIME_TYPES = [
    "Theft", "Assault", "Burglary", "Robbery", "Vandalism",
    "Drug Offense", "Fraud", "Vehicle Theft", "Homicide", "Cyber Crime"
]

LOCATIONS = [
    ("Sector 14 Market", 28.7041, 77.1025),
    ("Sector 18 Plaza", 28.7080, 77.1070),
    ("Old Town", 28.6900, 77.0950),
    ("Industrial Area", 28.7200, 77.1200),
    ("Railway Station", 28.7000, 77.0900),
    ("University Campus", 28.7150, 77.0800),
    ("Downtown Square", 28.7100, 77.1050),
    ("Riverfront", 28.6950, 77.1000),
    ("East Colony", 28.7250, 77.1150),
    ("West End", 28.7050, 77.0850),
    ("Bus Terminal", 28.7120, 77.0980),
    ("Hospital Road", 28.6980, 77.0920),
    ("Shopping Mall", 28.7160, 77.1100),
    ("Park Area", 28.7020, 77.0880),
    ("Residential Zone A", 28.7180, 77.0950),
]

SEVERITIES = ["Low", "Medium", "High", "Critical"]


SEED_FAKE_LOCATIONS = [loc[0] for loc in LOCATIONS]

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    existing_fake = db.query(CrimeIncident).filter(CrimeIncident.location_name.in_(SEED_FAKE_LOCATIONS)).limit(1).first()
    if existing_fake is not None:
        db.close()
        return

    now = datetime.now()
    incidents = []

    crime_weights = {
        "Theft": (0.25, 0.3, 0.3, 0.15),
        "Assault": (0.15, 0.3, 0.35, 0.2),
        "Burglary": (0.2, 0.35, 0.3, 0.15),
        "Robbery": (0.1, 0.25, 0.4, 0.25),
        "Vandalism": (0.3, 0.4, 0.25, 0.05),
        "Drug Offense": (0.2, 0.3, 0.35, 0.15),
        "Fraud": (0.3, 0.4, 0.25, 0.05),
        "Vehicle Theft": (0.25, 0.35, 0.3, 0.1),
        "Homicide": (0.0, 0.05, 0.3, 0.65),
        "Cyber Crime": (0.3, 0.4, 0.25, 0.05),
    }

    hot_spots = [
        (0, 28.7041, 77.1025, 0.0015),
        (2, 28.6900, 77.0950, 0.002),
        (4, 28.7000, 77.0900, 0.002),
        (5, 28.7150, 77.0800, 0.0015),
        (1, 28.7080, 77.1070, 0.001),
        (13, 28.7160, 77.1100, 0.001),
        (3, 28.7200, 77.1200, 0.0015),
    ]

    for _ in range(500):
        spot = random.choice(hot_spots)
        loc_idx, base_lat, base_lng, radius = spot

        lat = base_lat + random.uniform(-radius, radius)
        lng = base_lng + random.uniform(-radius, radius)

        crime_type = random.choice(CRIME_TYPES)
        severity_weights = crime_weights.get(crime_type, (0.25, 0.25, 0.25, 0.25))
        severity = random.choices(SEVERITIES, weights=severity_weights, k=1)[0]

        days_ago = random.randint(0, 365)
        hours = random.randint(0, 23)
        minutes = random.randint(0, 59)
        incident_time = now - timedelta(days=days_ago, hours=hours, minutes=minutes)

        location_name = LOCATIONS[loc_idx][0]

        descriptions = {
            "Theft": ["Stolen wallet", "Phone snatching", "Shoplifting incident", "Bag theft"],
            "Assault": ["Physical altercation", "Street fight", "Aggravated assault"],
            "Burglary": ["House break-in", "Office burglary", "Store break-in"],
            "Robbery": ["Armed robbery", "Bank robbery", "Street mugging"],
            "Vandalism": ["Property damage", "Graffiti", "Vehicle vandalism"],
            "Drug Offense": ["Drug possession", "Drug trafficking", "Illegal substance sale"],
            "Fraud": ["Online scam", "Credit card fraud", "Identity theft"],
            "Vehicle Theft": ["Car stolen", "Motorcycle theft", "Bike theft"],
            "Homicide": ["Murder investigation", "Manslaughter case"],
            "Cyber Crime": ["Phishing attack", "Data breach", "Ransomware"],
        }
        desc = random.choice(descriptions.get(crime_type, ["Incident reported"]))

        incident = CrimeIncident(
            crime_type=crime_type,
            location_name=location_name,
            latitude=round(lat, 6),
            longitude=round(lng, 6),
            date_time=incident_time,
            severity=severity,
            description=desc,
        )
        incidents.append(incident)

    db.add_all(incidents)
    db.commit()
    db.close()
    print(f"Seeded {len(incidents)} crime incidents")


if __name__ == "__main__":
    seed_database()
