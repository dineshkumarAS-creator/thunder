# 🐳 Docker Deployment Guide

## Quick Start with Docker Compose

### 1. Build and Run All Services
```bash
docker-compose up --build
```

This will start:
- **PostgreSQL** database on port 5432
- **Redis** on port 6379
- **FastAPI app** on port 8000
- **Celery worker** for background tasks
- **Celery beat** for scheduled tasks

### 2. Access the Application
- **API Docs:** http://localhost:8000/api/docs
- **Health Check:** http://localhost:8000/health

### 3. Stop All Services
```bash
docker-compose down
```

### 4. Stop and Remove Volumes
```bash
docker-compose down -v
```

---

## Individual Service Commands

### Run Only the App (without Celery)
```bash
docker-compose up app
```

### Run Only Database Services
```bash
docker-compose up postgres redis
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f app
docker-compose logs -f postgres
docker-compose logs -f celery-worker
```

---

## Production Deployment

### 1. Update Environment Variables
Create a `.env.prod` file:
```env
DATABASE_URL=postgresql://user:password@postgres:5432/tradeflow
REDIS_URL=redis://redis:6379/0
DEBUG=False
SUPABASE_URL=your-production-url
SUPABASE_KEY=your-production-key
GEMINI_API_KEY=your-api-key
JWT_SECRET_KEY=your-production-secret
```

### 2. Use Production Compose File
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 3. Scale Workers
```bash
docker-compose up --scale celery-worker=3
```

---

## Docker Commands Reference

### Build Image
```bash
docker build -t tradeflow-ai .
```

### Run Container
```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  -e GEMINI_API_KEY=... \
  tradeflow-ai
```

### Execute Commands in Container
```bash
# Access shell
docker-compose exec app bash

# Run migrations
docker-compose exec app python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"

# Create admin user
docker-compose exec app python scripts/create_admin.py
```

---

## Troubleshooting

### Database Connection Issues
```bash
# Check if PostgreSQL is ready
docker-compose exec postgres pg_isready

# View database logs
docker-compose logs postgres
```

### Redis Connection Issues
```bash
# Test Redis connection
docker-compose exec redis redis-cli ping
```

### App Not Starting
```bash
# Check app logs
docker-compose logs app

# Rebuild without cache
docker-compose build --no-cache app
docker-compose up app
```

### Clean Everything
```bash
# Remove all containers, networks, and volumes
docker-compose down -v
docker system prune -a
```

---

## Health Checks

All services have health checks configured:
- **PostgreSQL:** `pg_isready`
- **Redis:** `redis-cli ping`
- **App:** Waits for healthy database and Redis

---

## Volume Management

### Backup Database
```bash
docker-compose exec postgres pg_dump -U postgres tradeflow > backup.sql
```

### Restore Database
```bash
cat backup.sql | docker-compose exec -T postgres psql -U postgres tradeflow
```

### View Volume Data
```bash
docker volume ls
docker volume inspect trade-flow-ai_postgres_data
```

---

## Environment Variables in Docker

The app reads from `.env` file automatically. For Docker Compose, you can:

1. Use `.env` file (default)
2. Set in `docker-compose.yml` under `environment`
3. Use `env_file` directive

Example:
```yaml
services:
  app:
    env_file:
      - .env
      - .env.prod
```

---

## Performance Optimization

### Use Multi-Stage Build
```dockerfile
FROM python:3.11-slim as builder
# Build dependencies
...

FROM python:3.11-slim
# Copy only necessary files
COPY --from=builder /app /app
```

### Optimize Image Size
```bash
# Check image size
docker images tradeflow-ai

# Use alpine base
FROM python:3.11-alpine
```

---

## CI/CD Integration

### GitHub Actions Example
```yaml
- name: Build Docker Image
  run: docker build -t tradeflow-ai .

- name: Run Tests
  run: docker-compose run app pytest

- name: Push to Registry
  run: |
    docker tag tradeflow-ai registry/tradeflow-ai:latest
    docker push registry/tradeflow-ai:latest
```

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `docker-compose up` | Start all services |
| `docker-compose up -d` | Start in background |
| `docker-compose down` | Stop all services |
| `docker-compose logs -f` | View logs |
| `docker-compose ps` | List services |
| `docker-compose restart app` | Restart app |
| `docker-compose exec app bash` | Access shell |

---

**Ready to deploy!** 🚀
