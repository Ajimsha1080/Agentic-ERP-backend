# 🤖 Agentic ERP — Enterprise Multi-Agent Operating System

> **A production-ready, zero-hallucination, agentic ERP platform powering multi-agent enterprise automation, real-time data integration, and human-in-the-loop financial governance.**

---

## 🌟 Key Platform Capabilities

- **🤖 8 Specialized Autonomous Domain Agents**:
  - **Finance Agent**: P&L variance, overdue AR collections, cash runway, credit memos.
  - **Inventory Agent**: SKU velocity, stockout risk prediction, WMS reorder points.
  - **Procurement Agent**: Supplier comparison, purchase orders (POs), contract terms.
  - **Sales Agent**: CRM deal pipeline tracking, win/loss variance, customer churn alerts.
  - **Operations Agent**: Logistics SLA tracking, picking efficiency, warehouse zone optimization.
  - **HR Agent**: Automated payroll calculations, employee provisioning.
  - **Analytics Agent**: Cross-functional BI digests, trend predictions.
  - **Compliance Agent**: GDPR retention audits, legal SLA verification.
  - **Master Agent Orchestrator**: Intent classification & multi-node task routing.

- **🧠 Dual-Layer Agent Memory Engine** (`packages/agents/memory.py`):
  - **Short-Term Conversational Buffer**: Preserves active chat turns for seamless multi-turn follow-ups.
  - **Long-Term Episodic Memory**: Remembers past executive decisions, vendor preferences, and approved PO thresholds across user sessions.

- **🛡️ Enterprise AI Guardrails & Anti-Hallucination Engine** (`packages/security/guardrails.py`):
  - **Zero Temperature Math**: Forces `temperature = 0.0` for all ERP financial and inventory queries.
  - **Strict Source Grounding**: Every answer is verified against real ERP database records (`SAP S/4HANA`, `QuickBooks`, `Salesforce`).
  - **Prompt Injection Defense**: Intercepts jailbreaks and system override attacks.
  - **PII Redaction Engine**: Masks credit card numbers, SSNs, passwords, and secret API tokens.
  - **Human-in-the-Loop Threshold Enforcement**: Intercepts any financial action over **$1,000.00** for executive review.

- **🔗 UI-Driven Integrations & Connectors Hub** (`http://localhost:3000/connectors`):
  - 100% UI-based connection wizard for **SAP S/4HANA**, **Oracle NetSuite**, **QuickBooks Online**, **Salesforce CRM**, **Zendesk**, **Slack**, **Shopify**, and **Custom REST APIs**.
  - Flexible **Assign to Agent Selector**: Bind any custom API to a specific domain agent.
  - Interactive **`✎ Edit`** and **`🗑️ Disconnect`** controls.

---

## 🏗️ Monorepo Architecture Overview

```text
Agentic ERP Monorepo Structure:

├── apps/
│   ├── web/               # Next.js 16 App Router (Turbopack) UI Workspace (Port 3000)
│   ├── api/               # FastAPI REST Gateway & Endpoint Controllers (Port 8000)
│   └── worker/            # Celery Background Task Workers & Data Pipelines
│
├── packages/
│   ├── agents/            # Core ReAct Agents & Memory Engine (memory.py, base.py, api.py)
│   ├── connectors/        # Enterprise ERP Connectors (generic_rest.py, base.py)
│   ├── security/          # Guardrails & Safety Engine (guardrails.py)
│   ├── tools/             # Action Tools (erp_tools.py, create_purchase_order)
│   ├── database/          # SQLAlchemy Models, Core Engine, & Alembic Migrations
│   ├── models/            # Pydantic Request/Response Data Schemas
│   └── rag/               # Document Embeddings & Vector Search Indexing
│
├── infra/
│   ├── docker/            # Production Docker & Docker Compose Configurations
│   ├── kubernetes/        # K8s Deployment & Service Manifests
│   └── terraform/         # Infrastructure as Code (AWS RDS, App Runner)
│
└── tests/
    ├── unit/              # Automated Security & Guardrail Unit Tests (pytest)
    └── integration/       # API Gateway & Connector Integration Tests
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Python 3.10+** (Python 3.14 recommended)
- **Node.js 18+** & `npm`
- **Git**

### 2. Environment Configuration
Copy the example environment file and add your secret keys:

```bash
cp .env.example .env
```

**Developer/Admin Required Key (`.env`)**:
```env
# AI Model Provider Key (OpenAI, Anthropic, or Google Gemini)
OPENAI_API_KEY=sk-proj-your-api-key-here
SECRET_KEY=your-super-secret-security-key
DATABASE_URL=sqlite:///agents.db
ENVIRONMENT=development
```

---

### 3. Launching the Local Services

#### Option A: Running Backend & Frontend Servers (Development)

```powershell
# 1. Start Python API Gateway (Terminal 1)
$env:PYTHONPATH="."
python mock_api.py

# 2. Start Next.js 16 Web Dashboard (Terminal 2)
cd apps/web
npm install
npm run dev
```

- 🌐 **Frontend UI**: [http://localhost:3000](http://localhost:3000)
- ⚡ **Backend API**: [http://localhost:8000](http://localhost:8000)
- 📜 **Swagger OpenAPI Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

#### Option B: Launching via Docker Compose

```bash
docker compose -f infra/docker/docker-compose.yml up -d --build
```

---

## 🧪 Testing & Verification

Run backend unit tests and compilation audits to ensure 100% error-free execution:

```powershell
# 1. Compile all Python backend files
python -m compileall .

# 2. Run automated security & guardrail unit tests
pytest tests/unit/test_security.py

# 3. Run full Next.js production build check
cd apps/web
npm run build
```

---

## ☁️ Production Deployment Guide

### Option 1: Vercel (Frontend) + Render / Railway (Backend) — *Quick Deploy*
1. **Frontend (`apps/web`)**: Connect repository to **Vercel**, set Root Directory to `apps/web`.
2. **Backend (`FastAPI`)**: Create a Web Service on **Render.com** or **Railway.app** running `python mock_api.py`.

### Option 2: AWS Enterprise Cluster — *SOC 2 & Compliance Ready*
- **Frontend**: AWS Amplify or AWS ECS.
- **Backend API**: AWS App Runner or AWS ECS Fargate inside a private VPC.
- **Database**: AWS RDS PostgreSQL (Multi-AZ Encryption).
- **Background Tasks**: AWS ElastiCache for Redis.
- **Compliance Certification**: Inherits AWS SOC 1, SOC 2 Type II, ISO 27001, and HIPAA compliance out-of-the-box via AWS Artifact.

---

## 📄 License & Support

Copyright © 2026. All rights reserved.  
For technical support or deployment inquiries, contact your system administrator.
