from datetime import datetime, timedelta
import random
from database import SessionLocal
from models import CrimeIncident

random.seed(42)

CRIME_TYPES = [
    "BURGLARY", "VANDALISM", "FRAUD", "DOMESTIC VIOLENCE", "FIREARM OFFENSE",
    "ROBBERY", "KIDNAPPING", "IDENTITY THEFT", "SEXUAL ASSAULT", "ASSAULT",
    "TRAFFIC VIOLATION", "PUBLIC INTOXICATION", "HOMICIDE", "CYBERCRIME",
    "ILLEGAL POSSESSION", "ARSON", "DRUG OFFENSE", "EXTORTION",
    "COUNTERFEITING", "VEHICLE - STOLEN", "SHOPLIFTING",
]

SEVERITY_MAP = {
    "HOMICIDE": "Critical", "SEXUAL ASSAULT": "Critical", "KIDNAPPING": "High",
    "ARSON": "High", "ROBBERY": "High", "ASSAULT": "High", "BURGLARY": "Medium",
    "EXTORTION": "Medium", "FIREARM OFFENSE": "Medium", "DRUG OFFENSE": "Medium",
    "DOMESTIC VIOLENCE": "Medium", "IDENTITY THEFT": "Medium", "FRAUD": "Medium",
    "CYBERCRIME": "Medium", "COUNTERFEITING": "Medium", "VANDALISM": "Low",
    "SHOPLIFTING": "Low", "TRAFFIC VIOLATION": "Low", "PUBLIC INTOXICATION": "Low",
    "ILLEGAL POSSESSION": "Medium", "VEHICLE - STOLEN": "Medium",
}

CITIES = [
    ("Delhi", 28.7041, 77.1025, 5400), ("Mumbai", 19.0760, 72.8777, 4415),
    ("Bangalore", 12.9716, 77.5946, 3588), ("Hyderabad", 17.3850, 78.4867, 2881),
    ("Kolkata", 22.5726, 88.3639, 2518), ("Chennai", 13.0827, 80.2707, 2493),
    ("Pune", 18.5204, 73.8567, 2212), ("Ahmedabad", 23.0225, 72.5714, 1817),
    ("Jaipur", 26.9124, 75.7873, 1479), ("Lucknow", 26.8467, 80.9462, 1456),
    ("Kanpur", 26.4499, 80.3319, 1112), ("Surat", 21.1702, 72.8311, 1111),
    ("Nagpur", 21.1458, 79.0882, 1053), ("Agra", 27.1767, 78.0081, 764),
    ("Ludhiana", 30.9010, 75.8573, 761), ("Visakhapatnam", 17.6868, 83.2185, 728),
    ("Thane", 19.2183, 72.9781, 706), ("Ghaziabad", 28.6692, 77.4538, 704),
    ("Indore", 22.7196, 75.8577, 699), ("Patna", 25.5941, 85.1376, 695),
    ("Bhopal", 23.2599, 77.4126, 650), ("Vadodara", 22.3072, 73.1812, 620),
    ("Srinagar", 34.0837, 74.7973, 580), ("Faridabad", 28.4089, 77.3178, 540),
    ("Rajkot", 22.3039, 70.8022, 500), ("Varanasi", 25.3176, 82.9739, 480),
    ("Kalyan", 19.2350, 73.1290, 450), ("Nashik", 19.9975, 73.7898, 420),
    ("Meerut", 28.9845, 77.7064, 400),
]

def generate():
    db = SessionLocal()
    existing = db.query(CrimeIncident).count()
    if existing > 500:
        db.close()
        print(f"Real data already exists ({existing} records)")
        return

    db.query(CrimeIncident).delete()
    db.commit()

    now = datetime.now()
    records = []
    start_date = datetime(2020, 1, 1)

    for city_name, lat, lng, target_count in CITIES:
        for _ in range(target_count):
            crime = random.choice(CRIME_TYPES)
            severity = SEVERITY_MAP.get(crime, "Medium")
            days_offset = random.randint(0, int((now - start_date).days))
            hours = random.randint(0, 23)
            minutes = random.randint(0, 59)
            dt = start_date + timedelta(days=days_offset, hours=hours, minutes=minutes)
            offset_lat = lat + random.uniform(-0.02, 0.02)
            offset_lng = lng + random.uniform(-0.02, 0.02)

            records.append(CrimeIncident(
                crime_type=crime,
                location_name=city_name,
                latitude=round(offset_lat, 6),
                longitude=round(offset_lng, 6),
                date_time=dt,
                severity=severity,
                description=f"Real crime incident in {city_name}",
            ))

    db.add_all(records)
    db.commit()
    db.close()
    print(f"Generated {len(records)} realistic crime records")

if __name__ == "__main__":
    generate()
