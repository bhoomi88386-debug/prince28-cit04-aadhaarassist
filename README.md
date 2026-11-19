# AadhaarAssist

AadhaarAssist helps service-centre operators understand Aadhaar enrolment and update rules, including valid documents, update limits, fees and procedures, in Tamil and English.

## Who it's for

Common Service Centre operators who help residents update Aadhaar details.

## The problem

Valid documents differ for proof of identity, address, date of birth and relationship. Some fields can only be updated a limited number of times. Rules also change through official circulars.

## Data sources

- UIDAI FAQs
- Aadhaar Enrolment and Update Regulations
- Supporting documents list
- UIDAI circulars
- Aadhaar Act 2016

Official website: https://uidai.gov.in/

**Important:** Never store real Aadhaar numbers.

## Signature feature

**Counter checklist:** Select an update type and receive the valid documents, fees and limits as a Tamil printout.

## Target metric

Correct documents and limits for 95%+ of 40 scenarios.

---

## Run locally in one command (Docker Compose)

### Prerequisites

- Docker Desktop
- Docker Compose

### Start the application

```powershell
docker compose up --build -d
```

This starts:

- **PostgreSQL:** Database with pgvector support
- **Redis:** Caching and job queue service
- **Migrate:** Applies database migrations and loads seed data
- **API:** Starts the FastAPI application after dependencies are ready

### Check running services

```powershell
docker compose ps -a
```

The expected state is:

- Database: healthy
- Redis: healthy
- Migrate: exited with code 0
- API: healthy

### Access the application

| Resource | URL |
|---|---|
| API | http://localhost:8000 |
| Swagger documentation | http://localhost:8000/docs |
| Health check | http://localhost:8000/health |
| Readiness check | http://localhost:8000/ready |
| Documents API | http://localhost:8000/v1/documents |

### View application logs

```powershell
docker compose logs -f api
```

### Stop the application

```powershell
docker compose down
```

To remove containers and the PostgreSQL data volume:

```powershell
docker compose down -v
```

**Warning:** `down -v` deletes the stored database volume.

---

## Develop and test

The project uses `uv` for dependency management and Poe the Poet for task execution.

Install dependencies:

```powershell
uv sync --locked
```

| Task | Command |
|---|---|
| Start development server | `uv run poe dev` |
| Run unit tests | `uv run poe test` |
| Run integration tests | `uv run poe test-integration` |
| Run coverage report | `uv run poe cov` |
| Run lint checks | `uv run poe lint` |
| Apply migrations | `uv run poe migrate` |
| Load seed data | `uv run poe seed` |

**Integration tests:** Start the Docker Compose database before running integration tests. They create a separate temporary PostgreSQL database, apply migrations, run tests and clean up afterwards.

## Project structure

```text
aadhaarassist/
├── docker/
│   └── initdb/
│       └── 01-create-test-db.sql
├── migrations/
├── scripts/
├── src/
│   └── aadhaarassist/
│       ├── api/
│       └── db/
├── tests/
│   ├── unit/
│   └── integration/
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── Makefile
├── pyproject.toml
└── README.md
```

## Quality checks

The project includes:

- Multi-stage Docker image build
- Non-root application container
- PostgreSQL and Redis health checks
- Automatic database migrations
- Idempotent seed-data loading
- Unit and real-PostgreSQL integration tests
- Code coverage reporting
- Ruff lint and formatting checks
