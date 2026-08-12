# Agentic ERP Backend

A comprehensive AI-powered ERP backend system with multi-tenancy, advanced security, and extensive AI agent capabilities.

## 🚀 Features

### Core Architecture
- **FastAPI** - Modern, fast web framework with async support
- **PostgreSQL** - Primary database with vector storage for RAG capabilities
- **SQLAlchemy** - ORM with migration support
- **Redis + Celery** - Background task processing and caching
- **JWT Authentication** - Token-based authentication with refresh tokens

### Multi-Tenancy & Security
- Complete tenant isolation with organization/workspace hierarchy
- Role-Based Access Control (RBAC) with 10+ predefined roles
- Comprehensive security framework with middleware
- Audit logging and monitoring

### AI Agent Framework
- Configurable AI agents with model abstraction
- Tool integration and execution capabilities
- Knowledge base management
- Agent performance optimization

### Workflow System
- Visual workflow builder with drag-and-drop interface
- Dynamic workflow execution and monitoring
- Workflow templates and optimization
- Event-driven architecture

### Enterprise Features
- Comprehensive API documentation
- Background task processing
- Real-time monitoring and alerts
- Data analytics and reporting
- Integration capabilities

## Architecture Overview

```
Company Data → Unified Context → AI Agents → Decision/Action → Approval → Execution → Verification → Audit
```

### Key Components

- **Multi-Tenancy**: Enterprise-level organization hierarchy (Organization → Workspaces → Business Units → Users → Teams)
- **Identity & Access Management**: Enterprise-grade IAM with RBAC and fine-grained permissions
- **Zero-Trust Agent Security**: Tool-level, agent-level, user-level, data-level, action-level permissions
- **Agent Runtime**: Reusable agent platform with configurable agents
- **Tool System**: Secure framework for interacting with external systems
- **ERP Connector Framework**: Generic connector architecture supporting multiple ERPs
- **Unified Business Data Model**: Canonical data model normalizing data from different systems
- **Data Synchronization**: Initial sync, incremental sync, webhooks, scheduled sync
- **Company Knowledge/RAG**: Enterprise RAG for SOPs, policies, contracts, documentation
- **Hybrid Retrieval**: Vector search, keyword search, metadata filtering, structured queries
- **Agent Memory**: Session, user, organization, workflow, agent memory with permission awareness
- **Human-in-the-Loop**: Risk-based approval system with configurable thresholds
- **Action Engine**: Action lifecycle management with idempotency
- **Verification**: Post-action verification to confirm results
- **Audit System**: Complete tamper-resistant audit trail
- **Observability**: Production observability with distributed tracing
- **AI Evaluation**: Automated evaluation infrastructure
- **Model Abstraction**: LLM provider abstraction supporting multiple models
- **Prompt Management**: Versioned prompts with rollback support
- **Structured Output**: Typed schemas for agent outputs
- **Workflow Engine**: Visual workflow system with conditions, triggers, actions
- **Enterprise Security**: Encryption, secrets management, RBAC, MFA, SSO
- **Compliance-Ready**: Architecture hooks for SOC 2, GDPR, ISO 27001
- **Database**: PostgreSQL with pgvector
- **Background Processing**: Redis + worker architecture
- **API**: FastAPI with OpenAPI, Pydantic validation
- **Testing**: Unit, integration, E2E, evaluation tests
- **Containerization**: Docker + Docker Compose
- **CI/CD**: Automated pipeline with rollback support

## Quick Start

### Prerequisites

- Python 3.10+
- Docker & Docker Compose
- PostgreSQL 14+
- Redis 6+
- Node.js 18+ (for web application)

### Installation

1. Clone the repository
2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Create environment file:
```bash
cp .env.example .env
```

4. Configure environment variables in `.env`

5. Start services:
```bash
docker-compose up -d
```

6. Run database migrations:
```bash
python -m alembic upgrade head
```

7. Initialize the application:
```bash
python -m app.core.init
```

## Project Structure

```
apps/
  web/              # React/Next.js frontend
  api/              # FastAPI backend
  worker/           # Background workers

packages/
  agents/           # Agent implementations
  ai/               # AI model abstractions
  rag/              # RAG implementation
  connectors/       # ERP connectors
  tools/            # Tool definitions
  auth/             # Authentication & authorization
  policy/           # Policy engine
  workflows/        # Workflow engine
  actions/          # Action engine
  database/         # Database models & migrations
  observability/    # Logging, monitoring, tracing
  security/         # Security utilities
  shared/           # Shared utilities

infra/
  docker/           # Docker configurations
  terraform/        # Infrastructure as Code
  kubernetes/       # Kubernetes manifests

tests/
  unit/             # Unit tests
  integration/      # Integration tests
  e2e/              # End-to-end tests
  evaluation/       # Evaluation tests
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Token refresh

### Organizations
- `GET /api/v1/organizations` - List organizations
- `POST /api/v1/organizations` - Create organization
- `GET /api/v1/organizations/{id}` - Get organization details
- `PUT /api/v1/organizations/{id}` - Update organization

### Users
- `GET /api/v1/users` - List users
- `POST /api/v1/users` - Create user
- `GET /api/v1/users/{id}` - Get user details
- `PUT /api/v1/users/{id}` - Update user

### Roles
- `GET /api/v1/roles` - List roles
- `POST /api/v1/roles` - Create role
- `GET /api/v1/roles/{id}` - Get role details
- `PUT /api/v1/roles/{id}` - Update role

### Agents
- `GET /api/v1/agents` - List agents
- `POST /api/v1/agents` - Create agent
- `GET /api/v1/agents/{id}` - Get agent details
- `PUT /api/v1/agents/{id}` - Update agent
- `DELETE /api/v1/agents/{id}` - Delete agent

### Tools
- `GET /api/v1/tools` - List tools
- `GET /api/v1/tools/{id}` - Get tool details

### Integrations
- `GET /api/v1/integrations` - List integrations
- `POST /api/v1/integrations` - Create integration
- `GET /api/v1/integrations/{id}` - Get integration details
- `PUT /api/v1/integrations/{id}` - Update integration
- `DELETE /api/v1/integrations/{id}` - Delete integration

### Connectors
- `GET /api/v1/connectors` - List connectors
- `POST /api/v1/connectors` - Create connector
- `POST /api/v1/connectors/{id}/test` - Test connector
- `POST /api/v1/connectors/{id}/sync` - Sync data
- `GET /api/v1/connectors/{id}/sync-status` - Get sync status

### Data Sources
- `GET /api/v1/data-sources` - List data sources
- `POST /api/v1/data-sources` - Create data source
- `GET /api/v1/data-sources/{id}` - Get data source details
- `PUT /api/v1/data-sources/{id}` - Update data source
- `DELETE /api/v1/data-sources/{id}` - Delete data source

### Documents
- `POST /api/v1/documents` - Upload document
- `GET /api/v1/documents` - List documents
- `GET /api/v1/documents/{id}` - Get document details
- `DELETE /api/v1/documents/{id}` - Delete document
- `GET /api/v1/documents/{id}/download` - Download document

### Knowledge
- `POST /api/v1/knowledge/search` - Search knowledge base
- `GET /api/v1/knowledge/sources` - List knowledge sources

### Workflows
- `GET /api/v1/workflows` - List workflows
- `POST /api/v1/workflows` - Create workflow
- `GET /api/v1/workflows/{id}` - Get workflow details
- `POST /api/v1/workflows/{id}/execute` - Execute workflow
- `DELETE /api/v1/workflows/{id}` - Delete workflow

### Actions
- `GET /api/v1/actions` - List actions
- `POST /api/v1/actions` - Create action
- `GET /api/v1/actions/{id}` - Get action details
- `PUT /api/v1/actions/{id}` - Update action
- `DELETE /api/v1/actions/{id}` - Delete action
- `GET /api/v1/actions/{id}/approve` - Approve action
- `GET /api/v1/actions/{id}/reject` - Reject action

### Approvals
- `GET /api/v1/approvals` - List pending approvals
- `GET /api/v1/approvals/{id}` - Get approval details
- `POST /api/v1/approvals/{id}/approve` - Approve action
- `POST /api/v1/approvals/{id}/reject` - Reject action

### Audit
- `GET /api/v1/audit` - List audit logs
- `GET /api/v1/audit/{id}` - Get audit log details
- `GET /api/v1/audit/search` - Search audit logs

### Analytics
- `GET /api/v1/analytics/health` - Business health overview
- `GET /api/v1/analytics/agents` - Agent performance
- `GET /api/v1/analytics/usage` - AI usage metrics
- `GET /api/v1/analytics/cost` - Cost breakdown

### Billing
- `GET /api/v1/billing/organizations/{id}` - Get organization billing
- `GET /api/v1/billing/usage/{id}` - Get usage details
- `PUT /api/v1/billing/organizations/{id}` - Update billing plan

## Development

### Running the Application

**Development mode:**
```bash
cd apps/api
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Worker mode:**
```bash
cd apps/worker
python -m app.worker
```

**Frontend:**
```bash
cd apps/web
npm run dev
```

### Running Tests

```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/unit

# Run integration tests only
pytest tests/integration

# Run E2E tests
pytest tests/e2e

# Run with coverage
pytest --cov=app --cov-report=html
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Show current version
alembic current
```

### Docker

```bash
# Build and start all services
docker-compose up -d

# Build specific service
docker-compose build api

# Run a specific service
docker-compose up api

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

## Environment Variables

### Required Variables

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/agentic_platform

# Redis
REDIS_URL=redis://localhost:6379/0

# Secret Keys
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email (if using email authentication)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# LLM Provider (OpenAI, Google, Claude)
LLM_PROVIDER=openai
OPENAI_API_KEY=your-openai-api-key

# Application
APP_NAME=Agentic Business Operating Platform
APP_VERSION=1.0.0
DEBUG=True

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# File Upload
MAX_UPLOAD_SIZE=10485760  # 10MB
UPLOAD_DIR=/tmp/uploads
```

## Technology Stack

### Backend
- Python 3.10+
- FastAPI - Web framework
- SQLAlchemy - ORM
- Alembic - Database migrations
- Redis - Background tasks & caching
- PostgreSQL - Primary database
- pgvector - Vector similarity search

### Frontend
- React 18+ / Next.js 14+
- TypeScript
- Tailwind CSS
- React Query
- Zustand
- Vercel AI SDK

### Infrastructure
- Docker & Docker Compose
- Kubernetes (production)
- Terraform (IaC)
- Nginx (reverse proxy)
- Traefik (optional, for dynamic routing)

### Testing
- pytest
- pytest-asyncio
- pytest-cov
- httpx
- Playwright
- RAGAS (for evaluation)

### Development Tools
- Black (code formatting)
- flake8 (linting)
- mypy (type checking)
- pre-commit (hooks)

## Deployment

### Prerequisites

- Docker
- Kubernetes cluster
- PostgreSQL cluster
- Redis cluster
- Domain name with SSL certificate
- Environment variables configured

### Deployment Options

1. **Docker Compose**: For local development and small deployments
2. **Kubernetes**: For production deployments with auto-scaling
3. **AWS ECS/EKS**: For cloud deployments
4. **Azure AKS**: For Azure deployments
5. **Google GKE**: For Google Cloud deployments

### Production Deployment

```bash
# Build Docker images
docker-compose build

# Tag and push images
docker tag agentic-api:latest your-registry/agentic-api:v1.0.0
docker push your-registry/agentic-api:v1.0.0

# Deploy to Kubernetes
kubectl apply -f infra/kubernetes/

# Update deployment
kubectl set image deployment/agentic-api \
  agentic-api=your-registry/agentic-api:v1.0.0
```

## Monitoring & Observability

### Logging
- Structured JSON logging
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Request correlation IDs

### Metrics
- Prometheus metrics
- Custom metrics for agents, tools, actions
- Cost tracking

### Tracing
- OpenTelemetry integration
- Distributed tracing across services
- Agent execution tracing

### Alerts
- Error rate alerts
- Performance degradation alerts
- Integration failure alerts

## Security

- Encryption in transit (TLS 1.3)
- Encryption at rest (PostgreSQL encryption, Redis encryption)
- Secrets management (HashiCorp Vault or similar)
- Key rotation (automatic and manual)
- RBAC with fine-grained permissions
- MFA support
- SSO (SAML 2.0, OIDC)
- API rate limiting
- Input validation
- SSRF protection
- Prompt injection defenses
- Rate limiting
- WAF compatibility

## Compliance

Architecture is designed for:
- SOC 2 Type II
- GDPR compliance
- ISO 27001
- UAE data privacy requirements
- Indian data privacy requirements

Data retention policies, data deletion, export, legal hold, and audit log retention are supported through architecture hooks.

## Documentation

- [Architecture Documentation](docs/architecture/)
- [API Documentation](docs/api/)
- [Security Documentation](docs/security/)
- [Runbooks](docs/runbooks/)
- [Deployment Guide](docs/deployment.md)

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

Copyright © 2026. All rights reserved.

## Support

For support, please contact support@agenticplatform.com
