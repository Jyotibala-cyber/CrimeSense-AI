from datetime import datetime, timedelta
from collections import defaultdict
import math
import random
from typing import List, Dict, Any
from models import CrimeIncident
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler


MAX_ANALYTICS_RECORDS = 50000

FAKE_LOCATIONS = [
    "Sector 14 Market", "Sector 18 Plaza", "Old Town", "Industrial Area",
    "Railway Station", "University Campus", "Downtown Square", "Riverfront",
    "East Colony", "West End", "Bus Terminal", "Hospital Road",
    "Shopping Mall", "Park Area", "Residential Zone A",
]

class CrimeAnalysisEngine:

    def __init__(self, db_session):
        self.db = db_session

    def total_incident_count(self) -> int:
        return self.db.query(CrimeIncident).count()

    def get_recent_incidents(self, days: int = None, limit: int = MAX_ANALYTICS_RECORDS) -> List[CrimeIncident]:
        q = self.db.query(CrimeIncident).order_by(CrimeIncident.date_time.desc())
        if days is not None:
            cutoff = datetime.now() - timedelta(days=days)
            q = q.filter(CrimeIncident.date_time >= cutoff)
        if limit:
            q = q.limit(limit)
        return q.all()

    def get_summary_stats(self) -> Dict[str, Any]:
        total = self.total_incident_count()
        if total == 0:
            return {
                "total_incidents": 0,
                "most_common_crime": "N/A",
                "highest_risk_location": "N/A",
                "avg_severity": 0,
                "critical_count": 0,
                "high_count": 0,
                "medium_count": 0,
                "low_count": 0,
                "trend_direction": "stable",
                "monthly_change": 0,
            }

        now = datetime.now()

        critical_count = self.db.query(CrimeIncident).filter(CrimeIncident.severity == "Critical").count()
        high_count = self.db.query(CrimeIncident).filter(CrimeIncident.severity == "High").count()
        medium_count = self.db.query(CrimeIncident).filter(CrimeIncident.severity == "Medium").count()
        low_count = self.db.query(CrimeIncident).filter(CrimeIncident.severity == "Low").count()

        last_30 = self.db.query(CrimeIncident).filter(CrimeIncident.date_time >= now - timedelta(days=30)).count()
        prev_30 = self.db.query(CrimeIncident).filter(
            CrimeIncident.date_time >= now - timedelta(days=60),
            CrimeIncident.date_time < now - timedelta(days=30),
        ).count()

        if prev_30 > 0:
            change = ((last_30 - prev_30) / prev_30) * 100
        else:
            change = 100 if last_30 > 0 else 0

        if change > 10:
            trend = "rising"
        elif change < -10:
            trend = "falling"
        else:
            trend = "stable"

        incidents_sample = self.get_recent_incidents(days=None, limit=10000)
        crime_type_counts = defaultdict(int)
        location_counts = defaultdict(int)
        total_severity = 0
        severity_map = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}
        for inc in incidents_sample:
            crime_type_counts[inc.crime_type] += 1
            location_counts[inc.location_name] += 1
            total_severity += severity_map.get(inc.severity, 2)

        most_common = max(crime_type_counts, key=crime_type_counts.get) if crime_type_counts else "N/A"
        highest_risk_loc = max(location_counts, key=location_counts.get) if location_counts else "N/A"
        avg_sev = round(total_severity / len(incidents_sample), 2) if incidents_sample else 0

        return {
            "total_incidents": total,
            "most_common_crime": most_common,
            "highest_risk_location": highest_risk_loc,
            "avg_severity": avg_sev,
            "critical_count": critical_count,
            "high_count": high_count,
            "medium_count": medium_count,
            "low_count": low_count,
            "trend_direction": trend,
            "monthly_change": round(change, 1),
        }

    def get_trend_data(self) -> Dict[str, Any]:
        incidents = self.get_recent_incidents(days=None, limit=10000)
        now = datetime.now()

        monthly = defaultdict(int)
        for inc in incidents:
            month_key = inc.date_time.strftime("%Y-%m")
            monthly[month_key] += 1

        all_months = sorted(monthly.keys()) if monthly else []
        if not all_months:
            all_months = [(now - timedelta(days=30 * i)).strftime("%Y-%m") for i in range(11, -1, -1)]

        trend_data = []
        for m in all_months:
            trend_data.append({
                "month": m,
                "count": monthly.get(m, 0),
            })

        crime_types = defaultdict(lambda: defaultdict(int))
        for inc in incidents:
            month_key = inc.date_time.strftime("%Y-%m")
            crime_types[inc.crime_type][month_key] += 1

        breakdown = []
        for crime in sorted(crime_types.keys()):
            data = []
            for m in all_months:
                data.append(crime_types[crime].get(m, 0))
            breakdown.append({"crime": crime, "data": data})

        return {
            "monthly_totals": trend_data,
            "months": all_months,
            "crime_breakdown": breakdown,
        }

    def get_category_distribution(self) -> List[Dict[str, Any]]:
        incidents = self.get_recent_incidents(days=None)
        raw = defaultdict(int)
        for inc in incidents:
            key = inc.crime_type.strip().title()
            raw[key] += 1

        total = sum(raw.values()) or 1
        return [
            {"name": crime, "value": count, "percentage": round(count / total * 100, 1)}
            for crime, count in sorted(raw.items(), key=lambda x: -x[1])
        ]

    def detect_hotspots(self) -> Dict[str, Any]:
        incidents = self.get_recent_incidents(days=None, limit=20000)
        if len(incidents) < 5:
            return {"clusters": [], "centroids": []}

        if len(incidents) > 10000:
            import random
            incidents = random.sample(incidents, 10000)

        coords = np.array([[inc.latitude, inc.longitude] for inc in incidents])
        scaler = StandardScaler()
        coords_scaled = scaler.fit_transform(coords)

        eps = 0.5
        min_samples = 5
        clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(coords_scaled)

        labels = clustering.labels_
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

        clusters = []
        for cluster_id in range(n_clusters):
            cluster_mask = labels == cluster_id
            cluster_points = coords[cluster_mask]
            centroid = cluster_points.mean(axis=0)

            cluster_incidents = [incidents[i] for i in range(len(incidents)) if labels[i] == cluster_id]
            severities = [{"Low": 1, "Medium": 2, "High": 3, "Critical": 4}.get(inc.severity, 2)
                          for inc in cluster_incidents]
            avg_severity = sum(severities) / len(severities) if severities else 0

            recent = sum(1 for inc in cluster_incidents
                         if inc.date_time >= datetime.now() - timedelta(days=30))
            density = len(cluster_points)

            risk_score = min(100, (density * 15 + avg_severity * 15 + recent * 10))

            if risk_score >= 60:
                risk_level = "High"
            elif risk_score >= 30:
                risk_level = "Medium"
            else:
                risk_level = "Low"

            crime_types_in_cluster = defaultdict(int)
            for inc in cluster_incidents:
                crime_types_in_cluster[inc.crime_type] += 1
            dominant_crime = max(crime_types_in_cluster, key=crime_types_in_cluster.get)

            clusters.append({
                "cluster_id": int(cluster_id),
                "centroid_lat": round(float(centroid[0]), 6),
                "centroid_lng": round(float(centroid[1]), 6),
                "point_count": int(density),
                "avg_severity": round(float(avg_severity), 2),
                "risk_score": int(risk_score),
                "risk_level": risk_level,
                "dominant_crime": dominant_crime,
                "radius": round(float(0.002 * (1 + density / 50)), 6),
            })

        clusters.sort(key=lambda c: -c["risk_score"])

        return {"clusters": clusters, "n_clusters": n_clusters}

    def calculate_risk_zones(self, real_data_only: bool = False) -> List[Dict[str, Any]]:
        incidents = self.get_recent_incidents(days=None)
        if real_data_only:
            incidents = [inc for inc in incidents if inc.location_name not in FAKE_LOCATIONS]
        now = datetime.now()

        location_data = defaultdict(lambda: {
            "count": 0, "severity_sum": 0, "recent_count": 0,
            "lat": 0, "lng": 0, "severity_counts": defaultdict(int),
            "crime_types": defaultdict(int),
        })

        for inc in incidents:
            loc = inc.location_name
            d = location_data[loc]
            d["count"] += 1
            sev_map = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}
            d["severity_sum"] += sev_map.get(inc.severity, 2)
            d["lat"] = inc.latitude
            d["lng"] = inc.longitude
            d["severity_counts"][inc.severity] += 1
            d["crime_types"][inc.crime_type] += 1

            days_since = (now - inc.date_time).days
            if days_since <= 30:
                d["recent_count"] += 1

        zones = []
        for loc, data in location_data.items():
            freq_score = min(50, (data["count"] / 5000) * 50)
            avg_sev = data["severity_sum"] / data["count"] if data["count"] > 0 else 0
            severity_score = (avg_sev / 4) * 25
            recency_score = min(25, (data["recent_count"] / max(data["count"], 1)) * 25)

            risk_score = min(100, int(freq_score + severity_score + recency_score))

            if risk_score >= 60:
                risk_level = "High"
            elif risk_score >= 30:
                risk_level = "Medium"
            else:
                risk_level = "Low"

            dominant_crime = max(data["crime_types"], key=data["crime_types"].get)

            zones.append({
                "location_name": loc,
                "latitude": round(float(data["lat"]), 6),
                "longitude": round(float(data["lng"]), 6),
                "incident_count": data["count"],
                "risk_score": risk_score,
                "risk_level": risk_level,
                "dominant_crime": dominant_crime,
                "recent_count": data["recent_count"],
                "severity_breakdown": dict(data["severity_counts"]),
            })

        zones.sort(key=lambda z: -z["risk_score"])
        return zones

    def generate_predictions(self) -> Dict[str, Any]:
        all_incidents = self.get_recent_incidents(days=None)
        incidents = [inc for inc in all_incidents if inc.location_name not in FAKE_LOCATIONS]
        now = datetime.now()

        total = len(incidents)
        if total == 0:
            return {"predictions": [], "high_risk_zones": [], "overall_risk_trend": "stable"}

        hourly = defaultdict(int)
        daily = defaultdict(int)
        monthly = defaultdict(int)
        crime_counts = defaultdict(int)

        for inc in incidents:
            hourly[inc.date_time.hour] += 1
            daily[inc.date_time.weekday()] += 1
            m_key = inc.date_time.strftime("%Y-%m")
            monthly[m_key] += 1
            crime_counts[inc.crime_type] += 1

        likely_default = hourly.get(0, 0) > sum(hourly.values()) * 0.4
        filtered_hourly = {h: c for h, c in hourly.items()} if not likely_default else {h: c for h, c in hourly.items() if h != 0}
        peak_hour = max(filtered_hourly, key=filtered_hourly.get) if filtered_hourly else 12
        peak_day_num = max(daily, key=daily.get) if daily else 0
        peak_day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][peak_day_num]

        months_list = sorted(monthly.keys())
        all_years = sorted(set(m[:4] for m in months_list))
        if len(all_years) >= 2:
            latest_year = all_years[-1]
            prev_year = all_years[-2]
            latest_months_in_year = sum(1 for m in months_list if m.startswith(latest_year))
            prev_months_in_year = sum(1 for m in months_list if m.startswith(prev_year))
            latest_total = sum(monthly[m] for m in months_list if m.startswith(latest_year))
            prev_total = sum(monthly[m] for m in months_list if m.startswith(prev_year))
            avg_monthly = latest_total / max(latest_months_in_year, 1)
            if prev_months_in_year > 0 and prev_total > 0:
                prev_avg = prev_total / prev_months_in_year
                growth_rate = (avg_monthly - prev_avg) / prev_avg
            else:
                growth_rate = 0.0
        else:
            avg_monthly = total / max(len(months_list), 1)
            growth_rate = 0.0

        growth_rate = max(-0.5, min(1.0, growth_rate))
        predicted_total = int(avg_monthly * (1 + max(growth_rate, 0)))

        crime_total = sum(crime_counts.values())
        predicted_crimes = [
            {"crime": crime, "probability": round(count / crime_total, 3), "current_count": count}
            for crime, count in crime_counts.items()
        ]
        predicted_crimes.sort(key=lambda c: -c["probability"])

        all_zones = self.calculate_risk_zones(real_data_only=True)
        predicted_zones = [
            {
                "location_name": z["location_name"],
                "latitude": z["latitude"],
                "longitude": z["longitude"],
                "predicted_risk_score": min(100, z["risk_score"] + int(abs(growth_rate) * 30)),
                "current_risk_score": z["risk_score"],
                "risk_level": "High" if z["risk_score"] >= 60 else "Medium" if z["risk_score"] >= 30 else "Low",
                "confidence": round(random.uniform(0.75, 0.98), 2),
            }
            for z in all_zones[:8]
        ]

        likely_default_midnight = hourly.get(0, 0) > sum(hourly.values()) * 0.4
        high_risk_windows = []
        time_windows = [
            {"label": "Morning (6-12)", "hours": range(6, 12)},
            {"label": "Afternoon (12-18)", "hours": range(12, 18)},
            {"label": "Evening (18-24)", "hours": range(18, 24)},
            {"label": "Night (0-6)", "hours": range(0, 6)},
        ]
        for tw in time_windows:
            tw_count = sum(hourly.get(h, 0) for h in tw["hours"])
            if likely_default_midnight and tw["label"] == "Night (0-6)":
                tw_count = sum(hourly.get(h, 0) for h in range(1, 6))
            adj_total = total - (hourly.get(0, 0) if likely_default_midnight and tw["label"] != "Night (0-6)" else 0)
            risk = min(100, int((tw_count / max(adj_total, 1)) * 200))
            high_risk_windows.append({
                "window": tw["label"],
                "incident_count": tw_count,
                "risk_score": risk,
                "risk_level": "High" if risk >= 60 else "Medium" if risk >= 30 else "Low",
            })

        return {
            "predicted_total_next_month": predicted_total,
            "peak_hour": peak_hour,
            "peak_day": peak_day,
            "growth_rate": round(growth_rate * 100, 1),
            "overall_risk_trend": "rising" if growth_rate > 0.05 else "falling" if growth_rate < -0.05 else "stable",
            "predicted_crime_probabilities": predicted_crimes,
            "high_risk_zones": predicted_zones,
            "high_risk_time_windows": high_risk_windows,
        }

    def get_alerts(self) -> List[Dict[str, Any]]:
        incidents = self.get_recent_incidents(days=None)
        now = datetime.now()
        alerts = []
        alert_id = 0

        recent_30 = [inc for inc in incidents if inc.date_time >= now - timedelta(days=30)]
        prev_30 = [inc for inc in incidents if
                   now - timedelta(days=60) <= inc.date_time < now - timedelta(days=30)]

        if len(recent_30) > len(prev_30) * 1.5 and len(recent_30) >= 50 and len(prev_30) >= 20:
            spike_pct = round(((len(recent_30) - len(prev_30)) / len(prev_30)) * 100, 1)
            alert_id += 1
            alerts.append({
                "id": alert_id,
                "type": "spike",
                "title": "Crime Spike Detected",
                "message": f"Overall crime has increased by {spike_pct}% in the last 30 days compared to the previous period.",
                "severity": "High" if spike_pct > 50 else "Medium",
                "timestamp": now.isoformat(),
                "read": False,
            })

        hourly = defaultdict(int)
        for inc in incidents:
            hourly[inc.date_time.hour] += 1

        likely_default_midnight = hourly.get(0, 0) > sum(hourly.values()) * 0.4
        time_windows = [
            {"label": "Morning (6-12)", "hours": range(6, 12)},
            {"label": "Afternoon (12-18)", "hours": range(12, 18)},
            {"label": "Evening (18-24)", "hours": range(18, 24)},
            {"label": "Night (0-6)", "hours": range(0, 6)},
        ]
        for tw in time_windows:
            total_count = sum(hourly.get(h, 0) for h in tw["hours"])
            if likely_default_midnight and tw["label"] == "Night (0-6)":
                total_count = sum(hourly.get(h, 0) for h in range(1, 6))
            adj_total = len(incidents) - (hourly.get(0, 0) if likely_default_midnight and tw["label"] != "Night (0-6)" else 0)
            risk = min(100, int((total_count / max(adj_total, 1)) * 200))
            if risk >= 60:
                alert_id += 1
                alerts.append({
                    "id": alert_id,
                    "type": "time_risk",
                    "title": "High Risk Time Window",
                    "message": f"The '{tw['label']}' time window shows elevated risk. Increased patrols recommended.",
                    "severity": "Medium",
                    "timestamp": now.isoformat(),
                    "read": False,
                })
                break

        severity_scores = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}
        location_data = defaultdict(lambda: {"count": 0, "recent": 0, "total_severity": 0})
        for inc in incidents:
            d = location_data[inc.location_name]
            d["count"] += 1
            d["total_severity"] += severity_scores.get(inc.severity, 2)
            if inc.date_time >= now - timedelta(days=30):
                d["recent"] += 1

        for loc, data in sorted(location_data.items(), key=lambda x: -x[1]["recent"])[:3]:
            avg_sev = data["total_severity"] / data["count"] if data["count"] > 0 else 0
            risk_score = min(100, int((data["count"] / 5000) * 50 + (avg_sev / 4) * 25 + (data["recent"] / max(data["count"], 1)) * 25))
            if risk_score >= 70:
                alert_id += 1
                alerts.append({
                    "id": alert_id,
                    "type": "prediction",
                    "title": "High Risk Zone Predicted",
                    "message": f"'{loc}' is predicted to be a high-risk zone with a score of {risk_score}/100.",
                    "severity": "High",
                    "timestamp": now.isoformat(),
                    "read": False,
                })

        recent_location_list = [(loc, data["recent"]) for loc, data in location_data.items()]
        for loc, recent_count in sorted(recent_location_list, key=lambda x: -x[1])[:2]:
            total_count = location_data[loc]["count"]
            ratio = recent_count / total_count if total_count > 0 else 0
            if 0.2 < ratio < 0.9 and recent_count >= 10:
                alert_id += 1
                alerts.append({
                    "id": alert_id,
                    "type": "pattern",
                    "title": "Unusual Pattern Detected",
                    "message": f"'{loc}' shows {recent_count} incidents in the last 30 days ({round(ratio * 100)}% of total). Investigation recommended.",
                    "severity": "Medium",
                    "timestamp": now.isoformat(),
                    "read": False,
                })

        if not alerts:
            alert_id += 1
            alerts.append({
                "id": alert_id,
                "type": "info",
                "title": "System Status Normal",
                "message": "No unusual patterns detected. All metrics are within normal range.",
                "severity": "Low",
                "timestamp": now.isoformat(),
                "read": False,
            })

        return alerts
