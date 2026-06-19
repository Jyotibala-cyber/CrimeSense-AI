<div align="center">
  <br/>
  <table>
    <tr>
      <td align="center"><a href="#overview">Overview</a></td>
      <td align="center"><a href="#features">Features</a></td>
      <td align="center"><a href="#tech-stack">Tech Stack</a></td>
      <td align="center"><a href="#getting-started">Getting Started</a></td>
      <td align="center"><a href="#api-endpoints">API</a></td>
      <td align="center"><a href="#project-structure">Structure</a></td>
    </tr>
  </table>
</div>

<br/>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=28&duration=3000&pause=500&color=1E90FF&center=true&vCenter=true&width=600&lines=CrimeSense+AI;AI-Powered+Crime+Intelligence+Platform;Law+Enforcement+Analytics;Real-Time+Crime+Prediction" alt="Typing SVG" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Next.js%2016-000000?style=flat-square&logo=next.js&logoColor=white" alt="Next.js" />
  <img src="https://img.shields.io/badge/React%2019-61DAFB?style=flat-square&logo=react&logoColor=black" alt="React" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/Tailwind%20CSS%204-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white" alt="Tailwind" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/SQLite-07405E?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white" alt="scikit-learn" />
  <img src="https://img.shields.io/badge/Leaflet-199900?style=flat-square&logo=leaflet&logoColor=white" alt="Leaflet" />
</p>

<br/>

---

<h2 id="overview">🚀 Overview</h2>

<p align="center">
  <b>CrimeSense AI</b> is a full-stack crime intelligence and prediction platform that empowers law enforcement agencies with <b>real-time analytics</b>, <b>AI-driven predictions</b>, and an <b>interactive geospatial interface</b>.
</p>

<br/>

<table align="center">
  <tr>
    <td align="center" width="200">
      <br/>
      <code>🔍 Crime Mapping</code>
      <br/>
      <sub>Interactive heatmaps with DBSCAN hotspot clustering</sub>
      <br/><br/>
    </td>
    <td align="center" width="200">
      <br/>
      <code>📊 Analytics</code>
      <br/>
      <sub>Trend analysis, severity distribution, category breakdowns</sub>
      <br/><br/>
    </td>
    <td align="center" width="200">
      <br/>
      <code>🤖 AI Predictions</code>
      <br/>
      <sub>Forecast peak crime hours, high-risk zones, growth rates</sub>
      <br/><br/>
    </td>
  </tr>
  <tr>
    <td align="center" width="200">
      <br/>
      <code>🚨 Smart Alerts</code>
      <br/>
      <sub>Automated notifications for crime spikes and anomalies</sub>
      <br/><br/>
    </td>
    <td align="center" width="200">
      <br/>
      <code>📁 Data Management</code>
      <br/>
      <sub>Bulk upload (CSV/JSON/PDF/Excel) and manual entry</sub>
      <br/><br/>
    </td>
    <td align="center" width="200">
      <br/>
      <code>🗺️ Location Search</code>
      <br/>
      <sub>Geocode any Indian city, village, or state via OSM</sub>
      <br/><br/>
    </td>
  </tr>
</table>

<br/>

---

<h2 id="features">✨ Features</h2>

<br/>

<h3>🛡️ Officer Authentication</h3>
<ul>
  <li>Secure login with role-based access control</li>
  <li>Persistent sessions with JWT token management</li>
  <li>One-click logout with session cleanup</li>
</ul>

<h3>🗺️ Interactive Crime Map</h3>
<ul>
  <li>Multi-style map views (Dark / Light / Satellite)</li>
  <li>Severity-based circle markers with popup details</li>
  <li>DBSCAN hotspot clusters with risk scoring</li>
  <li>Per-location risk zone overlays</li>
  <li>Real-time filtering by crime type, severity, and location</li>
  <li>Nominatim-powered location search for any Indian city, village, or state</li>
</ul>

<h3>📈 Analytics Dashboard</h3>
<ul>
  <li>Summary statistics: total incidents, most common crime, risk score</li>
  <li>Monthly trend charts with per-crime breakdown</li>
  <li>Crime category distribution (pie/donut chart)</li>
  <li>Severity distribution (bar chart)</li>
  <li>Top high-risk locations ranking</li>
  <li>Critical / High / Medium / Low severity counts with trend direction</li>
</ul>

<h3>🧠 AI Predictions Engine</h3>
<ul>
  <li>Next month incident volume forecasting</li>
  <li>Peak crime hour and day prediction</li>
  <li>Crime growth rate estimation</li>
  <li>Per-crime probability analysis with radar visualization</li>
  <li>High-risk zone identification for upcoming period</li>
  <li>Time-window based risk assessment</li>
</ul>

<h3>🔔 Smart Alert System</h3>
<ul>
  <li>Automatic detection of crime spikes and anomalies</li>
  <li>Severity-coded notifications (Critical / High / Medium / Low)</li>
  <li>Filterable alert history</li>
  <li>Visual indicators for unread alerts</li>
</ul>

<h3>📋 Data Management</h3>
<ul>
  <li>Bulk upload: CSV, JSON, PDF, or Excel file import</li>
  <li>Manual entry: Form-based single incident recording</li>
  <li>Supports 21 crime types across 29 Indian cities</li>
  <li>Server-side file parsing with validation</li>
</ul>

<br/>

---

<h2 id="tech-stack">🛠️ Tech Stack</h2>

<br/>

<table align="center">
  <tr>
    <th colspan="2">Frontend</th>
    <th colspan="2">Backend</th>
  </tr>
  <tr>
    <td align="center">
      <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nextjs/nextjs-original.svg" width="40" alt="Next.js"/><br/>
      <b>Next.js 16</b>
    </td>
    <td align="center">
      <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg" width="40" alt="React"/><br/>
      <b>React 19</b>
    </td>
    <td align="center">
      <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="40" alt="Python"/><br/>
      <b>Python 3</b>
    </td>
    <td align="center">
      <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg" width="40" alt="FastAPI"/><br/>
      <b>FastAPI</b>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg" width="40" alt="TypeScript"/><br/>
      <b>TypeScript</b>
    </td>
    <td align="center">
      <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/tailwindcss/tailwindcss-original.svg" width="40" alt="Tailwind"/><br/>
      <b>Tailwind CSS 4</b>
    </td>
    <td align="center">
      <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlite/sqlite-original.svg" width="40" alt="SQLite"/><br/>
      <b>SQLite</b>
    </td>
    <td align="center">
      <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/numpy/numpy-original.svg" width="40" alt="NumPy"/><br/>
      <b>NumPy / Pandas</b>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/leaflet/leaflet-original.svg" width="40" alt="Leaflet"/><br/>
      <b>Leaflet</b>
    </td>
    <td align="center">
      <img src="https://www.chartlets.io/img/logo-recharts.png" width="40" alt="Recharts"/><br/>
      <b>Recharts</b>
    </td>
    <td align="center">
      <img src="https://upload.wikimedia.org/wikipedia/commons/0/05/Scikit_learn_logo_small.svg" width="40" alt="scikit-learn"/><br/>
      <b>scikit-learn</b>
    </td>
    <td align="center">
      <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlalchemy/sqlalchemy-original.svg" width="40" alt="SQLAlchemy"/><br/>
      <b>SQLAlchemy</b>
    </td>
  </tr>
</table>

<br/>

---

<h2 id="getting-started">⚡ Getting Started</h2>

<br/>

### Prerequisites

<table>
  <tr>
    <td><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg" width="20"/></td>
    <td><b>Node.js</b> >= 18</td>
    <td><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="20"/></td>
    <td><b>Python</b> >= 3.10</td>
    <td><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pycharm/pycharm-original.svg" width="20"/></td>
    <td><b>pip</b> (Python package manager)</td>
  </tr>
</table>

### Installation

```bash
# Clone the repository
git clone https://github.com/Jyotibala-cyber/CrimeSense-AI.git
cd CrimeSense-AI

# Install backend dependencies
cd backend
pip install -r requirements.txt
cd ..

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### Running the Application

<table>
  <tr>
    <th>Terminal 1 — Backend</th>
    <th>Terminal 2 — Frontend</th>
  </tr>
  <tr>
    <td>

```bash
cd backend
uvicorn main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload
```

</td>
    <td>

```bash
cd frontend
npm run dev
```

</td>
  </tr>
</table>

### Access Points

| Service | URL | Description |
|---------|-----|-------------|
| 🌐 **Frontend** | http://localhost:3000 | Web application dashboard |
| ⚙️ **Backend** | http://localhost:8000 | REST API server |
| 📖 **API Docs** | http://localhost:8000/docs | Interactive Swagger documentation |

<br/>

> **Note:** The application seeds 500 demo crime incidents on first startup and imports real NCRB crime data (41,732+ records across 29 Indian cities).

---

<h2 id="credentials">🔐 Login Credentials</h2>

<br/>

<table align="center">
  <tr>
    <th>Username</th>
    <th>Password</th>
    <th>Name</th>
    <th>Badge</th>
  </tr>
  <tr>
    <td><code>inspector.singh</code></td>
    <td><code>crimsense@2025</code></td>
    <td>Inspector Singh</td>
    <td>IPC-4421</td>
  </tr>
  <tr>
    <td><code>officer.sharma</code></td>
    <td><code>crimsense@2025</code></td>
    <td>Officer Sharma</td>
    <td>IPC-3312</td>
  </tr>
  <tr>
    <td><code>admin</code></td>
    <td><code>admin@123</code></td>
    <td>Admin Officer</td>
    <td>ADM-001</td>
  </tr>
</table>

<br/>

---

<h2 id="api-endpoints">📡 API Endpoints</h2>

<br/>

<details>
<summary><b>🔐 Authentication</b></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check |
| `POST` | `/api/auth/login` | Officer login |
| `POST` | `/api/auth/verify` | Verify authentication token |

</details>

<details>
<summary><b>📋 Incidents</b></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/incidents` | List crime incidents (with filters) |
| `POST` | `/api/incidents` | Create a new incident |
| `POST` | `/api/upload` | Upload data file (CSV/JSON/PDF/Excel) |

</details>

<details>
<summary><b>📊 Analytics</b></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/analytics/summary` | Dashboard summary statistics |
| `GET` | `/api/analytics/trends` | Monthly crime trends |
| `GET` | `/api/analytics/categories` | Crime category distribution |
| `GET` | `/api/analytics/hotspots` | DBSCAN hotspot clusters |
| `GET` | `/api/analytics/risk-zones` | Per-location risk analysis |

</details>

<details>
<summary><b>🤖 Predictions & Alerts</b></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/predictions` | AI-powered predictions |
| `GET` | `/api/alerts` | Crime alerts |

</details>

<details>
<summary><b>🗺️ Geocoding & Locations</b></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/geocode` | Geocode a location (DB + Nominatim fallback) |
| `GET` | `/api/geocode/search` | Location suggestions via Nominatim |
| `GET` | `/api/locations` | List all known locations |

</details>

<details>
<summary><b>📈 Crime Statistics</b></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/crime-stats` | NCRB crime statistics |
| `GET` | `/api/crime-stats/summary` | Aggregated crime stats |
| `GET` | `/api/crime-stats/categories` | Crime stats by law category |

</details>

<br/>

---

<h2 id="project-structure">📁 Project Structure</h2>

<br/>

<pre>
CrimeSense-AI/
│
├── <b>backend/</b>                  <i># Python FastAPI server</i>
│   ├── 📄 main.py              <i># Application entry point &amp; all API endpoints</i>
│   ├── 📄 database.py          <i># SQLAlchemy database configuration</i>
│   ├── 📄 models.py            <i># ORM models (CrimeIncident, CrimeStat)</i>
│   ├── 📄 ai_engine.py         <i># Analytics, predictions, alerts engine</i>
│   ├── 📄 seed_data.py         <i># Demo data seeder (500 records)</i>
│   ├── 📄 import_dataset.py    <i># NCRB dataset importer</i>
│   ├── 📄 requirements.txt     <i># Python dependencies</i>
│   └── 🗄️ crime_data.db        <i># SQLite database</i>
│
├── <b>frontend/</b>                 <i># Next.js web application</i>
│   ├── <b>src/</b>
│   │   ├── <b>app/</b>              <i># Next.js App Router pages</i>
│   │   │   ├── 📄 page.tsx      <i># Dashboard / Command Center</i>
│   │   │   ├── 📂 login/        <i># Officer authentication</i>
│   │   │   ├── 📂 map/          <i># Crime intelligence map</i>
│   │   │   ├── 📂 analytics/    <i># Deep analytics</i>
│   │   │   ├── 📂 predictions/  <i># AI predictions</i>
│   │   │   ├── 📂 alerts/       <i># Alert center</i>
│   │   │   ├── 📂 crime-stats/  <i># NCRB crime statistics</i>
│   │   │   └── 📂 upload/       <i># Data upload &amp; manual entry</i>
│   │   ├── <b>components/</b>       <i># Reusable UI components</i>
│   │   │   ├── 📄 Sidebar.tsx
│   │   │   ├── 📄 StatsCard.tsx
│   │   │   ├── 📄 CrimeTrendChart.tsx
│   │   │   ├── 📄 CategoryPieChart.tsx
│   │   │   ├── 📄 TopLocations.tsx
│   │   │   ├── 📄 AlertsPanel.tsx
│   │   │   ├── 📄 CrimeHeatmap.tsx
│   │   │   └── 📄 LazyMap.tsx
│   │   └── <b>lib/</b>               <i># Core libraries</i>
│   │       ├── 📄 api.ts        <i># API client &amp; TypeScript interfaces</i>
│   │       ├── 📄 auth.tsx      <i># Authentication context &amp; provider</i>
│   │       └── 📄 utils.ts      <i># Utility functions</i>
│   ├── 📄 package.json
│   ├── 📄 next.config.ts
│   ├── 📄 tsconfig.json
│   └── 📄 postcss.config.mjs
│
├── <b>dataset/</b>                  <i># Crime data files</i>
│   ├── 📄 indian-crimes-from-jan-to-aug-2025.csv
│   └── 📄 data.xltx
│
├── 📄 start.bat               <i># Windows batch launcher</i>
├── 📄 start.ps1               <i># PowerShell launcher</i>
├── 📄 .gitignore
└── 📄 README.md
</pre>

<br/>

---

<h2 id="data">📊 Data</h2>

<br/>

<table align="center">
  <tr>
    <th>Data Source</th>
    <th>Records</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>NCRB Crime Dataset</td>
    <td align="center"><b>41,732+</b></td>
    <td>Real Indian crime statistics across 29 cities (Jan–Aug 2025)</td>
  </tr>
  <tr>
    <td>Demo Seed Data</td>
    <td align="center"><b>500</b></td>
    <td>Randomized crime incidents for immediate visualization</td>
  </tr>
  <tr>
    <td>Custom Upload</td>
    <td align="center"><i>Unlimited</i></td>
    <td>Import via CSV, JSON, PDF, or Excel files</td>
  </tr>
</table>

<br/>

---

<h2 id="screenshots">🖼️ Screenshots</h2>

<br/>

<p align="center">
  <i>(Screenshots coming soon)</i>
</p>

<br/>

---

<h2 id="roadmap">🗺️ Roadmap</h2>

<br/>

<ul>
  <li><input type="checkbox" checked disabled /> Officer authentication &amp; session management</li>
  <li><input type="checkbox" checked disabled /> Interactive crime map with heatmap &amp; hotspots</li>
  <li><input type="checkbox" checked disabled /> Analytics dashboard with charts &amp; trends</li>
  <li><input type="checkbox" checked disabled /> AI-powered crime predictions</li>
  <li><input type="checkbox" checked disabled /> Smart alert system</li>
  <li><input type="checkbox" checked disabled /> Data upload (CSV/JSON/PDF/Excel)</li>
  <li><input type="checkbox" checked disabled /> Nominatim geocoding for any Indian location</li>
  <li><input type="checkbox" disabled /> Real-time data streaming</li>
  <li><input type="checkbox" disabled /> Mobile responsive optimizations</li>
  <li><input type="checkbox" disabled /> Multi-language support</li>
  <li><input type="checkbox" disabled /> PDF report generation</li>
</ul>

<br/>

---

<h2 id="license">📄 License</h2>

<br/>

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License" />
  <br/><br/>
  Copyright &copy; 2025 CrimeSense AI
  <br/><br/>
  <sub>Built for law enforcement and public safety analytics</sub>
  <br/>
  <sub>Made with ❤️ by <a href="https://github.com/Jyotibala-cyber">Jyotibala</a> &amp; <a href="https://github.com/harsh160311">Harsh</a></sub>
</p>

<br/>

---

<p align="center">
  <a href="#top">⬆️ Back to Top</a>
</p>
