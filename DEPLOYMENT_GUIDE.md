# 🚀 TradeFlow AI - Complete Deployment Guide

## 📋 Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Production Deployment](#production-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Database Setup](#database-setup)
6. [Troubleshooting](#troubleshooting)

---

## 🖥️ Local Development

### Prerequisites
- Python 3.11+
- PostgreSQL 15+ (or use Supabase)
- Redis (optional, for background tasks)
- Tesseract OCR
- Poppler (for PDF processing)

### Step 1: Install System Dependencies

**Windows (using Chocolatey):**
```powershell
choco install tesseract poppler
```

**macOS:**
```bash
brew install tesseract poppler
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr poppler-utils
```

### Step 2: Install Python Dependencies
```bash
cd "c:\Users\sridh\OneDrive\Desktop\Track Eye\trade-flow-ai"
python -m pip install -r requirements.txt
```

### Step 3: Configure Environment
```bash
# Copy example env file
cp .env.example .env

# Edit .env with your credentials
# Required: SUPABASE_URL, SUPABASE_KEY, GEMINI_API_KEY, DATABASE_URL, JWT_SECRET_KEY
```

### Step 4: Create Database Tables
```bash
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"
```

### Step 5: Run the Application
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Step 6: Access the Application
- **API Docs:** http://localhost:8000/api/docs
- **ReDoc:** http://localhost:8000/api/redoc
- **Health Check:** http://localhost:8000/health

---

## 🐳 Docker Deployment

### Quick Start
```bash
# Build and run all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f
```

### Services Included
- **PostgreSQL** - Database (port 5432)
- **Redis** - Cache & queue (port 6379)
- **FastAPI App** - Main application (port 8000)
- **Celery Worker** - Background tasks
- **Celery Beat** - Scheduled tasks

### Stop Services
```bash
# Stop all
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Access Container Shell
```bash
docker-compose exec app bash
```

---

## 🌐 Production Deployment

### Option 1: Deploy to Cloud (Recommended)

#### **Vercel/Netlify (Frontend) + Railway/Render (Backend)**

**1. Deploy Backend to Railway:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

**2. Set Environment Variables in Railway:**
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `GEMINI_API_KEY`
- `DATABASE_URL` (use Railway PostgreSQL)
- `JWT_SECRET_KEY`

**3. Deploy Frontend:**
```bash
# Build frontend
npm run build

# Deploy to Vercel
vercel deploy --prod
```

#### **Deploy to AWS/GCP/Azure**

**Using Docker:**
```bash
# Build image
docker build -t tradeflow-ai .

# Tag for registry
docker tag tradeflow-ai your-registry/tradeflow-ai:latest

# Push to registry
docker push your-registry/tradeflow-ai:latest

# Deploy to cloud service
# (AWS ECS, GCP Cloud Run, Azure Container Instances)
```

### Option 2: VPS Deployment (DigitalOcean, Linode, etc.)

**1. SSH into server:**
```bash
ssh user@your-server-ip
```

**2. Install Docker:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**3. Clone repository:**
```bash
git clone https://github.com/your-repo/tradeflow-ai.git
cd tradeflow-ai
```

**4. Configure environment:**
```bash
cp .env.example .env
nano .env  # Edit with your credentials
```

**5. Deploy with Docker Compose:**
```bash
docker-compose up -d
```

**6. Setup Nginx reverse proxy:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**7. Setup SSL with Let's Encrypt:**
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## ⚙️ Environment Configuration

### Required Variables
```env
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# JWT
JWT_SECRET_KEY=your-secret-key-min-32-chars

# AI
GEMINI_API_KEY=your-gemini-api-key
```

### Optional Variables
```env
# Redis
REDIS_URL=redis://localhost:6379/0

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Security
ENCRYPTION_KEY=your-encryption-key
RATE_LIMIT_PER_MINUTE=100

# Features
ENABLE_AI_EXTRACTION=true
ENABLE_EMAIL_NOTIFICATIONS=true
```

### Generate Secrets
```bash
# JWT Secret
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Encryption Key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 🗄️ Database Setup

### Using Supabase (Recommended)

**1. Create Supabase Project:**
- Go to https://supabase.com
- Create new project
- Wait for database to initialize

**2. Get Connection String:**
- Go to Settings > Database
- Copy connection string
- Update `DATABASE_URL` in `.env`

**3. Create Tables:**
```bash
# Tables are created automatically on first run
# Or manually:
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"
```

**4. Create Storage Bucket:**
- Go to Storage in Supabase dashboard
- Create bucket named `shipments`
- Set to public or private based on needs

### Using Local PostgreSQL

**1. Install PostgreSQL:**
```bash
# Windows
choco install postgresql

# macOS
brew install postgresql

# Linux
sudo apt-get install postgresql
```

**2. Create Database:**
```bash
psql -U postgres
CREATE DATABASE tradeflow;
\q
```

**3. Update `.env`:**
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/tradeflow
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. **Module Not Found Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### 2. **Database Connection Failed**
```bash
# Check if PostgreSQL is running
# Windows
sc query postgresql

# Linux/macOS
sudo systemctl status postgresql

# Test connection
psql -h localhost -U postgres -d tradeflow
```

#### 3. **Tesseract Not Found**
```bash
# Windows - Add to PATH
setx PATH "%PATH%;C:\Program Files\Tesseract-OCR"

# Verify installation
tesseract --version
```

#### 4. **Port Already in Use**
```bash
# Find process using port 8000
# Windows
netstat -ano | findstr :8000

# Linux/macOS
lsof -i :8000

# Kill process
# Windows
taskkill /PID <pid> /F

# Linux/macOS
kill -9 <pid>
```

#### 5. **Docker Build Fails**
```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

#### 6. **Supabase Connection Issues**
```bash
# Check if URL and keys are correct
# Verify in Supabase dashboard: Settings > API

# Test connection
python -c "import httpx; print(httpx.get('YOUR_SUPABASE_URL/rest/v1/').status_code)"
```

### Logs and Debugging

**View Application Logs:**
```bash
# Local
tail -f logs/tradeflow.log

# Docker
docker-compose logs -f app
```

**Enable Debug Mode:**
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

**Test Endpoints:**
```bash
# Health check
curl http://localhost:8000/health

# API docs
curl http://localhost:8000/api/docs
```

---

## 📊 Performance Optimization

### 1. **Database Optimization**
```sql
-- Create indexes
CREATE INDEX idx_shipments_supplier ON shipments(supplier_id);
CREATE INDEX idx_shipments_status ON shipments(status);
CREATE INDEX idx_quotes_shipment ON quotes(shipment_id);
```

### 2. **Caching with Redis**
```python
# Enable Redis caching in production
REDIS_URL=redis://your-redis-url:6379/0
```

### 3. **Use Production Server**
```bash
# Use Gunicorn instead of Uvicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### 4. **Enable Compression**
```python
# Add to main.py
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

---

## 🔐 Security Checklist

- [ ] Change default `JWT_SECRET_KEY`
- [ ] Use strong database passwords
- [ ] Enable HTTPS/SSL in production
- [ ] Set `DEBUG=False` in production
- [ ] Configure CORS properly
- [ ] Use environment variables for secrets
- [ ] Enable rate limiting
- [ ] Regular security updates
- [ ] Backup database regularly
- [ ] Monitor logs for suspicious activity

---

## 📈 Monitoring

### Setup Logging
```python
# Already configured in config.py
LOG_LEVEL=INFO
LOG_FILE=logs/tradeflow.log
```

### Health Checks
```bash
# Endpoint
GET /health

# Response
{
  "status": "healthy",
  "service": "tradeflow-ai"
}
```

### Metrics (Optional)
```bash
# Add Prometheus metrics
pip install prometheus-fastapi-instrumentator

# In main.py
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)
```

---

## 🎯 Quick Commands Reference

| Task | Command |
|------|---------|
| **Install deps** | `pip install -r requirements.txt` |
| **Run locally** | `uvicorn main:app --reload` |
| **Run with Docker** | `docker-compose up` |
| **Create tables** | `python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"` |
| **View logs** | `docker-compose logs -f` |
| **Stop Docker** | `docker-compose down` |
| **Access shell** | `docker-compose exec app bash` |
| **Run tests** | `pytest` |
| **Format code** | `black .` |
| **Lint code** | `flake8 .` |

---

## 🆘 Support

- **Documentation:** See `README.md`, `PROJECT_COMPLETE.md`
- **API Docs:** http://localhost:8000/api/docs
- **Docker Guide:** See `DOCKER_GUIDE.md`

---

**Ready to deploy!** 🚀

Choose your deployment method and follow the steps above. Good luck!
