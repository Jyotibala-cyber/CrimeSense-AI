<div align="center">

<br/>

# 🔵 CrimeSense AI

### AI-Powered Crime Intelligence & Prediction Platform

<p>
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square" />
  <img src="https://img.shields.io/badge/License-MIT-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/Version-1.0.0-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/Made%20in-India-FF9933?style=flat-square" />
</p>

<p>
  <img src="https://img.shields.io/badge/Next.js%2016-000000?style=flat-square&logo=next.js&logoColor=white" />
  <img src="https://img.shields.io/badge/React%2019-61DAFB?style=flat-square&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-07405E?style=flat-square&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white" />
  <img src="https://img.shields.io/badge/Tailwind%20CSS-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white" />
</p>

<br/>

> CrimeSense AI is a full-stack AI-powered crime intelligence platform designed for law enforcement agencies. It integrates geospatial mapping, machine learning, and NCRB data analytics into a unified command center for predictive policing.

<br/>

</div>

---

## 📌 Overview

CrimeSense AI addresses the lack of a unified data-driven system for crime monitoring and prediction.

It uses **41,732+ NCRB records across 29 Indian cities** to provide:
- Crime hotspot detection
- Future crime prediction
- Real-time alert system
- Interactive crime intelligence dashboard

---

## 🎯 Problem Statement

Law enforcement systems lack:
- Predictive crime analysis
- Unified dashboard for monitoring
- AI-based hotspot detection
- Data-driven decision support

---

## 💡 Solution

- AI-powered crime prediction engine  
- DBSCAN-based hotspot clustering  
- Interactive geospatial crime mapping  
- Smart alert system for anomaly detection  
- Centralized police command dashboard  

---

## ✨ Features

### 🗺️ Crime Map Intelligence
- Interactive Leaflet map
- Crime hotspot visualization
- Risk zone overlays
- Real-time filtering system

### 📊 Analytics Dashboard
- Crime trends over time
- Category-wise analysis
- Severity distribution
- High-risk location ranking

### 🧠 AI Prediction Engine
- Next-month crime forecasting
- Peak crime hour prediction
- Risk analysis per region
- Trend estimation

### 🔔 Smart Alert System
- Anomaly detection
- Crime spike alerts
- Severity-based notifications

### 📁 Data System
- CSV / JSON / Excel / PDF upload
- NCRB dataset (41,732+ records)
- Multi-city crime coverage

---

## 🛠️ Tech Stack

Frontend: Next.js 16, React 19, TypeScript  
Backend: FastAPI (Python)  
Database: SQLite + SQLAlchemy  
ML: Scikit-learn, Pandas, NumPy  
Maps: Leaflet.js  
Charts: Recharts  
Auth: JWT  
Geocoding: OpenStreetMap Nominatim  

---

## ⚙️ Getting Started

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

## ⚡ Getting Started

### Prerequisites

| Requirement | Version |
|---|---|
| Node.js | >= 18 |
| Python | >= 3.10 |
| pip | Latest |

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/Jyotibala-cyber/CrimeSense-AI.git
cd CrimeSense-AI
```

**2. Install backend dependencies**
```bash
cd backend
pip install -r requirements.txt
cd ..
```

**3. Install frontend dependencies**
```bash
cd frontend
npm install
cd ..
```

### Running the Application

Open two separate terminals:

**Terminal 1 — Backend**
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 — Frontend**
```bash
cd frontend
npm run dev
```

### Access Points

| Service | URL |
|---|---|
| 🌐 Web Dashboard | http://localhost:3000 |
| ⚙️ REST API | http://localhost:8000 |
| 📖 Swagger Docs | http://localhost:8000/docs |

> **Note:** On first startup, the application automatically seeds **500 demo crime incidents** and imports **41,732+ real NCRB records** across 29 Indian cities.

---

## 🔐 Login Credentials

| Username | Password | Name | Badge |
|---|---|---|---|
| `inspector.singh` | `crimsense@2025` | Inspector Singh | IPC-4421 |
| `officer.sharma` | `crimsense@2025` | Officer Sharma | IPC-3312 |
| `admin` | `admin@123` | Admin Officer | ADM-001 |

---

## 📡 API Reference

<details>
<summary><b>Authentication</b></summary>

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health check |
| `POST` | `/api/auth/login` | Officer login |
| `POST` | `/api/auth/verify` | Verify JWT token |

</details>

<details>
<summary><b>Incidents</b></summary>

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/incidents` | List incidents with filters |
| `POST` | `/api/incidents` | Create a new incident |
| `POST` | `/api/upload` | Bulk upload (CSV/JSON/PDF/Excel) |

</details>

<details>
<summary><b>Analytics</b></summary>

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/analytics/summary` | Dashboard summary statistics |
| `GET` | `/api/analytics/trends` | Monthly crime trends |
| `GET` | `/api/analytics/categories` | Category distribution |
| `GET` | `/api/analytics/hotspots` | DBSCAN hotspot clusters |
| `GET` | `/api/analytics/risk-zones` | Per-location risk analysis |

</details>

<details>
<summary><b>Predictions & Alerts</b></summary>

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/predictions` | AI-powered forecast data |
| `GET` | `/api/alerts` | Crime alerts and anomalies |

</details>

<details>
<summary><b>Geocoding & Locations</b></summary>

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/geocode` | Geocode a location (DB + Nominatim fallback) |
| `GET` | `/api/geocode/search` | Location suggestions |
| `GET` | `/api/locations` | List all known locations |

</details>

<details>
<summary><b>Crime Statistics</b></summary>

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/crime-stats` | NCRB crime statistics |
| `GET` | `/api/crime-stats/summary` | Aggregated crime stats |
| `GET` | `/api/crime-stats/categories` | Stats by law category |

</details>

---

## 📁 Project Structure

```
CrimeSense-AI/
│
├── backend/ 
│
├── frontend/                       # Next.js web application
│
├── dataset/                        # Crime data files
│
├── start.ps1                       # PowerShell launcher
└── README.md
```

---

## 📊 Data Sources

| Source | Records | Description |
|---|---|---|
| NCRB Crime Dataset | **41,732+** | Real Indian crime statistics across 29 cities (Jan–Aug 2025) |
| Demo Seed Data | **500** | Randomized incidents for immediate visualization on first launch |
| Custom Uploads | **Unlimited** | CSV, JSON, PDF, or Excel imports by officers |

---

## 🗺️ Roadmap

- [x] Officer authentication & role-based access
- [x] Interactive crime map with heatmap & DBSCAN hotspots
- [x] Analytics dashboard with charts and trend analysis
- [x] AI-powered crime predictions engine
- [x] Smart alert system for anomaly detection
- [x] Bulk data upload (CSV / JSON / PDF / Excel)
- [x] Nominatim geocoding for any Indian location
- [ ] Real-time data streaming
- [ ] Mobile-responsive optimizations
- [ ] Multi-language support
- [ ] PDF report generation

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

Copyright © 2025 CrimeSense AI — Built for law enforcement and public safety analytics.

---

<div align="center">

Made with ❤️ by [Jyotibala](https://github.com/Jyotibala-cyber) & [Harsh](https://github.com/harsh160311)
=======
<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License" />
  <br/><br/>
  Copyright &copy; 2025 CrimeSense AI
  <br/><br/>
  <sub>Built for law enforcement and public safety analytics</sub>
  <br/>
  
</p>


<br/>

*Empowering law enforcement with intelligent, data-driven crime analytics.*

</div>
