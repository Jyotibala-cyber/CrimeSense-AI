from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum as SAEnum, Index
from sqlalchemy.sql import func
from database import Base
import enum


class SeverityEnum(str, enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class CrimeIncident(Base):
    __tablename__ = "crime_incidents"

    id = Column(Integer, primary_key=True, index=True)
    crime_type = Column(String(100), nullable=False, index=True)
    location_name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    date_time = Column(DateTime, nullable=False, index=True)
    severity = Column(String(20), nullable=False, default="Medium")
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("ix_crime_incidents_location", "location_name"),
        Index("ix_crime_incidents_severity", "severity"),
        Index("ix_crime_incidents_type_severity", "crime_type", "severity"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "crime_type": self.crime_type,
            "location_name": self.location_name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "date_time": self.date_time.isoformat() if self.date_time else None,
            "severity": self.severity,
            "description": self.description,
        }


class CrimeStat(Base):
    __tablename__ = "crime_stats"

    id = Column(Integer, primary_key=True, index=True)
    law_category = Column(String(100), nullable=False, index=True)
    crime_section = Column(String(300), nullable=False, index=True)
    reason = Column(String(300), nullable=False)
    cases_jan_aug_2025 = Column(Integer, default=0)
    cases_aug_2024 = Column(Integer, default=0)
    cases_jul_2025 = Column(Integer, default=0)
    cases_aug_2025 = Column(Integer, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "law_category": self.law_category,
            "crime_section": self.crime_section,
            "reason": self.reason,
            "cases_jan_aug_2025": self.cases_jan_aug_2025,
            "cases_aug_2024": self.cases_aug_2024,
            "cases_jul_2025": self.cases_jul_2025,
            "cases_aug_2025": self.cases_aug_2025,
        }
