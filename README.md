# 👁️ ARGUS — Advanced Real-time Guard & Unified Security System

> Named after the Greek giant with 100 eyes who could see everything.
> ARGUS watches your entire infrastructure and never misses a threat.

A production-style SIEM (Security Information and Event Management) 
system built from scratch using Python, FastAPI, and PostgreSQL.


---

## 📌 What is ARGUS?

ARGUS is an open-source SIEM system that:
- 📥 Collects logs from multiple sources
- 🔍 Parses and normalizes log data
- 🗄️ Stores logs in PostgreSQL database
- 🌐 Exposes data via REST APIs
- 📊 Visualizes logs in a real-time dashboard
- 🚨 Detects threats using a rule engine
- 🗺️ Maps attacks to MITRE ATT&CK framework
- 🌍 Performs GeoIP and threat intelligence lookups
- 📧 Sends email alerts and generates PDF reports
- 🐳 Deployable via Docker

---

## 🚀 Project Roadmap

| Phase | Feature | Status |
|-------|---------|--------|
| 1 | Log file reader | ✅ Completed |
| 2 | Log parser + PostgreSQL storage | ✅ Completed |
| 3 | FastAPI backend + REST APIs | ✅ Completed |
| 4 | Frontend dashboard | 🔄 In Progress |
| 5 | Rule engine + brute-force detection | ⏳ Pending |
| 6 | Severity levels + alert dashboard | ⏳ Pending |
| 7 | Multi-source log support | ⏳ Pending |
| 8 | MITRE ATT&CK mapping | ⏳ Pending |
| 9 | GeoIP + Threat Intelligence | ⏳ Pending |
| 10 | Email alerts, PDF reports, Auth, Docker | ⏳ Pending |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.x, FastAPI |
| Database | PostgreSQL |
| Frontend | HTML, CSS, JavaScript |
| Security | MITRE ATT&CK, VirusTotal, AbuseIPDB |
| Deployment | Docker |

---

## 📁 Project Structure
ARGUS/
├── logs/               # Raw log files
│   └── sample.log
├── src/                # Python source code
│   ├── log_reader.py   # Phase 1 - Log ingestion
│   ├── log_parser.py   # Phase 2 - Log parsing
│   ├── database.py     # Phase 2-3 - Database operations
│   ├── main.py         # Phase 2 - Pipeline controller
│   └── api.py          # Phase 3 - REST API
├── data/               # Local database files
├── .env.example        # Environment variables template
└── README.md

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/pnarale-sec/ARGUS.git
cd ARGUS
```

### 2. Install dependencies
```bash
pip install fastapi uvicorn psycopg2-binary python-dotenv
```

### 3. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

### 4. Run log ingestion
```bash
python src/main.py
```

### 5. Start the API server
```bash
cd src
uvicorn api:app --reload
```
