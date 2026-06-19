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

> **CrimeSense AI** is a full-stack crime intelligence platform built for law enforcement agencies.  
> It combines real-time geospatial mapping, AI-driven predictions, and NCRB data analytics  
> into a unified command center — purpose-built for Indian law enforcement.

<br/>

[Overview](#-overview) • [Features](#-features) • [Tech Stack](#-tech-stack) • [Getting Started](#-getting-started) • [API Reference](#-api-reference) • [Project Structure](#-project-structure) • [Data Sources](#-data-sources)

</div>

---

## 📌 Overview

CrimeSense AI addresses a critical gap in law enforcement tooling — the lack of a unified, data-driven platform for crime monitoring and prediction. By integrating **41,732+ real NCRB records** across 29 Indian cities with machine learning models, it enables officers to:

- Identify crime hotspots using DBSCAN spatial clustering
- Predict next-month crime volumes and peak risk hours
- Monitor live alerts for anomalies and crime spikes
- Upload and analyze field data in bulk (CSV, JSON, Excel, PDF)

---

## ✨ Features

### 🛡️ Officer Authentication
- Role-based access control with secure JWT session management
- Persistent login state with one-click logout and session cleanup
- Pre-configured officer accounts for immediate access

### 🗺️ Interactive Crime Map
- Multi-style map views: **Dark**, **Light**, and **Satellite**
- Severity-coded circle markers with detailed incident popups
- **DBSCAN hotspot clustering** with automated risk scoring
- Per-location risk zone overlays for patrol planning
- Real-time filtering by crime type, severity, date, and location
- **Nominatim-powered geocoding** — search any Indian city, village, or state

### 📊 Analytics Dashboard
- Summary statistics: total incidents, dominant crime type, risk score
- Monthly trend charts with per-category crime breakdown
- Crime category distribution via pie/donut chart
- Severity distribution bar chart (Critical / High / Medium / Low)
- Top high-risk locations leaderboard with trend direction indicators

### 🧠 AI Predictions Engine
- Next-month incident volume forecasting
- Peak crime hour and day-of-week prediction
- Crime growth rate estimation per category
- Per-crime probability analysis with radar visualization
- High-risk zone identification for upcoming periods
- Time-window based risk assessment

### 🔔 Smart Alert System
- Automatic detection of crime spikes and statistical anomalies
- Severity-coded notifications with visual unread indicators
- Filterable alert history by severity and crime type

### 📁 Data Management
- Bulk upload support: **CSV, JSON, PDF, and Excel**
- Manual incident entry via structured form
- Covers **21 crime types** across **29 Indian cities**
- Server-side file parsing with full validation

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend Framework** | Next.js 16 + React 19 | App routing, SSR, component architecture |
| **Language** | TypeScript | Type-safe frontend development |
| **Styling** | Tailwind CSS 4 | Utility-first responsive UI |
| **Maps** | Leaflet.js | Interactive geospatial rendering |
| **Charts** | Recharts | Analytics visualizations |
| **Backend Framework** | FastAPI (Python) | REST API server with async support |
| **Database** | SQLite + SQLAlchemy | Persistent data storage and ORM |
| **ML / Analytics** | scikit-learn, NumPy, Pandas | DBSCAN clustering, predictions, analytics |
| **Geocoding** | OpenStreetMap Nominatim | Indian location search and geocoding |
| **Auth** | JWT Tokens | Secure officer session management |

---

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
├── backend/                        # Python FastAPI server
│   ├── main.py                     # Entry point & all API endpoints
│   ├── database.py                 # SQLAlchemy configuration
│   ├── models.py                   # ORM models (CrimeIncident, CrimeStat)
│   ├── ai_engine.py                # Analytics, predictions & alerts engine
│   ├── seed_data.py                # Demo data seeder (500 records)
│   ├── import_dataset.py           # NCRB dataset importer
│   ├── requirements.txt            # Python dependencies
│   └── crime_data.db               # SQLite database
│
├── frontend/                       # Next.js web application
│   └── src/
│       ├── app/                    # Next.js App Router pages
│       │   ├── page.tsx            # Dashboard / Command Center
│       │   ├── login/              # Officer authentication
│       │   ├── map/                # Crime intelligence map
│       │   ├── analytics/          # Deep analytics
│       │   ├── predictions/        # AI predictions
│       │   ├── alerts/             # Alert center
│       │   ├── crime-stats/        # NCRB statistics
│       │   └── upload/             # Data upload & manual entry
│       ├── components/             # Reusable UI components
│       │   ├── Sidebar.tsx
│       │   ├── StatsCard.tsx
│       │   ├── CrimeTrendChart.tsx
│       │   ├── CategoryPieChart.tsx
│       │   ├── TopLocations.tsx
│       │   ├── AlertsPanel.tsx
│       │   ├── CrimeHeatmap.tsx
│       │   └── LazyMap.tsx
│       └── lib/                    # Core libraries
│           ├── api.ts              # API client & TypeScript interfaces
│           ├── auth.tsx            # Auth context & provider
│           └── utils.ts            # Utility functions
│
├── dataset/                        # Crime data files
│   ├── indian-crimes-from-jan-to-aug-2025.csv
│   └── data.xltx
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
