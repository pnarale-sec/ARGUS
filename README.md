# 👁️ ARGUS — Advanced Real-time Guard & Unified Security System

> Named after the Greek giant with 100 eyes who could see everything.  
> ARGUS watches your entire infrastructure and never misses a threat.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active%20Development-brightgreen)

A production-style **SIEM (Security Information and Event Management)** system  
built from scratch using Python, FastAPI, and PostgreSQL.  
Developed as a **Final Year Engineering Mega Project**.

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
- 🔐 Role-based access control with JWT authentication
- 🐳 Deployable via Docker

---

## 🚀 Project Roadmap

| Phase | Feature | Status |
|-------|---------|--------|
| 1 | Log file reader | ✅ Completed |
| 2 | Log parser + PostgreSQL storage | ✅ Completed |
| 3 | FastAPI backend + REST APIs | ✅ Completed |
| 4 | Frontend dashboard with charts | ✅ Completed |
| 5 | Rule engine + brute force detection | ✅ Completed |
| 6 | Backend refactoring — modular architecture | 🔄 In Progress |
| 7 | SQLAlchemy ORM + Alembic migrations | ⏳ Pending |
| 8 | Improved detection engine (10+ rules) | ⏳ Pending |
| 9 | Alert system with severity levels | ⏳ Pending |
| 10 | Dashboard improvements | ⏳ Pending |
| 11 | Charts and analytics | ⏳ Pending |
| 12 | Investigation features | ⏳ Pending |
| 13 | Advanced search system | ⏳ Pending |
| 14 | Real-time WebSocket monitoring | ⏳ Pending |
| 15 | Multi-source log parsers | ⏳ Pending |
| 16 | Reporting (PDF, CSV, JSON) | ⏳ Pending |
| 17 | JWT authentication + RBAC | ⏳ Pending |
| 18 | Security hardening | ⏳ Pending |
| 19 | Threat intelligence (VirusTotal, AbuseIPDB) | ⏳ Pending |
| 20 | MITRE ATT&CK mapping | ⏳ Pending |
| 21 | Performance optimization | ⏳ Pending |
| 22 | Testing (pytest) | ⏳ Pending |
| 23 | Docker deployment | ⏳ Pending |
| 24 | Documentation | ⏳ Pending |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, FastAPI |
| ORM | SQLAlchemy 2.0 + Alembic |
| Database | PostgreSQL 15 |
| Frontend | HTML, CSS, JavaScript, Chart.js |
| Auth | JWT + bcrypt |
| Security | MITRE ATT&CK, VirusTotal, AbuseIPDB |
| Testing | pytest |
| Deployment | Docker + docker-compose |

---

## 📁 Project Structure
ARGUS/
├── app/
│   ├── api/              # API route handlers
│   │   ├── logs.py
│   │   ├── alerts.py
│   │   ├── stats.py
│   │   └── health.py
│   ├── core/             # Core configuration
│   │   ├── config.py
│   │   └── logger.py
│   ├── database/         # Database models and connection
│   │   ├── connection.py
│   │   └── models.py
│   ├── schemas/          # Pydantic schemas
│   │   ├── log.py
│   │   └── alert.py
│   ├── detection/        # Rule engine
│   │   └── rule_engine.py
│   ├── parser/           # Log parsers
│   │   └── log_parser.py
│   └── services/         # Business logic
│       ├── log_service.py
│       └── alert_service.py
├── logs/                 # Raw log files
├── static/               # Frontend dashboard
├── tests/                # pytest test suite
├── main.py               # Application entry point
├── .env.example          # Environment variables template
├── docker-compose.yml    # Docker deployment
└── README.md
---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/pnarale-sec/ARGUS.git
cd ARGUS
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

### 5. Run database migrations
```bash
alembic upgrade head
```

### 6. Start the server
```bash
uvicorn main:app --reload
```

### 7. Open dashboard
---

## 🔌 API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | Dashboard | No |
| GET | `/api/logs` | Get all logs | Yes |
| GET | `/api/logs/{id}` | Get log by ID | Yes |
| GET | `/api/alerts` | Get all alerts | Yes |
| PUT | `/api/alerts/{id}/status` | Update alert status | Yes |
| GET | `/api/stats` | Dashboard statistics | Yes |
| GET | `/api/health` | System health check | No |

---

## 🔐 Detection Rules

| Rule | Severity | Description |
|------|----------|-------------|
| BRUTE_FORCE | HIGH | 5+ failed logins from same IP |
| ERROR_STORM | MEDIUM | 3+ errors from same source |
| SUSPICIOUS_KEYWORD | CRITICAL | Known attack keywords |
| PORT_SCAN | HIGH | Multiple port connection attempts |
| SQL_INJECTION | CRITICAL | SQL injection patterns |
| XSS | HIGH | Cross-site scripting patterns |
| PRIVILEGE_ESCALATION | CRITICAL | Sudo/root access attempts |
| DIRECTORY_TRAVERSAL | HIGH | Path traversal patterns |

---

## 📊 Dashboard Features

- ✅ Real-time log monitoring
- ✅ Severity distribution charts
- ✅ Logs over time visualization
- ✅ Alert management center
- ✅ Global search with highlighting
- ✅ Multi-filter support
- ✅ Sortable, paginated log table
- ✅ Expandable log details
- ✅ One-click copy log entry
- ✅ Auto-refresh every 30 seconds
- ⏳ WebSocket live streaming
- ⏳ GeoIP attack map
- ⏳ MITRE ATT&CK matrix view

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 🐳 Docker Deployment

```bash
docker-compose up --build
```

---

## 👨‍💻 Developer

**Prathamesh Narale**  
Computer Science Engineering — Final Year  
Shivaji University, Kolhapur 

[![GitHub](https://img.shields.io/badge/GitHub-pnarale--sec-black?logo=github)](https://github.com/pnarale-sec)

---

## 📜 License

MIT License — Free to use and modify

---

## ⭐ Star this repo if you find it useful!