# Deployment Guide (T242)

## Prerequisites

- Linux server (Ubuntu 20.04+ recommended)
- Docker and Docker Compose
- PostgreSQL 15+
- Node.js 18+ and Python 3.11+
- Domain name with DNS access
- SSL certificate (Let's Encrypt recommended)

## Quick Start (Docker Deployment)

### 1. Clone Repository

```bash
git clone https://github.com/yourorg/multi-school-platform.git
cd multi-school-platform
```

### 2. Configure Environment Variables

**Backend** (`.env`):
```bash
# Database
DATABASE_URL=postgresql://user:password@postgres:5432/multi_school_db

# JWT
JWT_SECRET_KEY=your-super-secret-key-change-this
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Redis (optional, for caching)
REDIS_URL=redis://redis:6379/0

# File Storage
STORAGE_PATH=/data/schools
MAX_STORAGE_PER_SCHOOL_GB=10

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# CAPTCHA (optional)
HCAPTCHA_SECRET_KEY=your-hcaptcha-secret-key

# Environment
ENVIRONMENT=production
```

**Frontend** (`.env.local`):
```bash
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_HCAPTCHA_SITE_KEY=your-hcaptcha-site-key
```

### 3. Build and Deploy with Docker Compose

```bash
docker-compose up -d
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: multi_school_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backend/scripts/init_db.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://postgres:${DB_PASSWORD}@postgres:5432/multi_school_db
      REDIS_URL: redis://redis:6379/0
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}
    volumes:
      - school_data:/data/schools
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis

  frontend:
    build: ./frontend
    environment:
      NEXT_PUBLIC_API_URL: ${API_URL}
    ports:
      - "3000:3000"
    depends_on:
      - backend

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - frontend
      - backend

volumes:
  postgres_data:
  redis_data:
  school_data:
```

### 4. Run Database Migrations

```bash
docker-compose exec backend alembic upgrade head
```

### 5. Create Super Admin User

```bash
docker-compose exec backend python scripts/create_superadmin.py \
  --email admin@platform.com \
  --password SuperSecurePassword123
```

## Manual Deployment (Production)

### Backend Deployment

1. **Install dependencies**:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Set up database**:
```bash
psql -U postgres -c "CREATE DATABASE multi_school_db;"
alembic upgrade head
```

3. **Run with Gunicorn**:
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app \
  --bind 0.0.0.0:8000 \
  --access-logfile /var/log/backend/access.log \
  --error-logfile /var/log/backend/error.log
```

4. **Create systemd service** (`/etc/systemd/system/backend.service`):
```ini
[Unit]
Description=Multi-School Backend
After=network.target postgresql.service

[Service]
User=www-data
WorkingDirectory=/var/www/backend
Environment="PATH=/var/www/backend/venv/bin"
ExecStart=/var/www/backend/venv/bin/gunicorn -c gunicorn.conf.py main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable backend
sudo systemctl start backend
```

### Frontend Deployment

1. **Build production bundle**:
```bash
cd frontend
npm install
npm run build
```

2. **Run with PM2**:
```bash
npm install -g pm2
pm2 start npm --name "frontend" -- start
pm2 save
pm2 startup
```

### NGINX Configuration

**nginx.conf**:
```nginx
# Rate limiting
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=100r/m;
limit_req_zone $binary_remote_addr zone=auth_limit:10m rate=5r/m;

server {
    listen 80;
    server_name *.yourdomain.com yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name *.yourdomain.com yourdomain.com;

    # SSL
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # API endpoints
    location /api/ {
        limit_req zone=api_limit burst=20 nodelay;
        proxy_pass http://localhost:8000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Auth endpoints (stricter rate limit)
    location /api/auth/ {
        limit_req zone=auth_limit burst=3 nodelay;
        proxy_pass http://localhost:8000/auth/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Static files (cache aggressively)
    location /_next/static/ {
        proxy_pass http://localhost:3000;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## SSL Certificate Setup (Let's Encrypt)

```bash
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com -d *.yourdomain.com

# Auto-renew
sudo certbot renew --dry-run
```

Add to crontab:
```cron
0 0 * * 0 certbot renew --quiet
```

## Monitoring & Logging

### Application Logs

**Backend**:
```bash
tail -f /var/log/backend/access.log
tail -f /var/log/backend/error.log
```

**Frontend**:
```bash
pm2 logs frontend
```

### Database Monitoring

```sql
-- Active queries
SELECT pid, query, state
FROM pg_stat_activity
WHERE state != 'idle';

-- Slow queries
SELECT * FROM pg_stat_statements
ORDER BY mean_exec_time DESC LIMIT 10;
```

### Health Checks

```bash
# API health
curl https://api.yourdomain.com/health

# Database health
curl https://api.yourdomain.com/health/db
```

## Backup & Recovery

### Automated Backups

Create `/scripts/backup.sh`:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U postgres multi_school_db | gzip > /backups/db_$DATE.sql.gz
aws s3 cp /backups/db_$DATE.sql.gz s3://your-bucket/backups/
find /backups -name "db_*.sql.gz" -mtime +30 -delete
```

Schedule daily:
```cron
0 2 * * * /scripts/backup.sh >> /var/log/backup.log 2>&1
```

### Restore from Backup

```bash
gunzip < /backups/db_20260131_020000.sql.gz | psql -U postgres multi_school_db
```

## Scaling

### Horizontal Scaling

1. **Load Balancer**: Add NGINX load balancer
2. **Multiple Backend Instances**: Run multiple Gunicorn instances
3. **Database Replication**: Set up PostgreSQL read replicas
4. **CDN**: Use Cloudflare for static assets

### Vertical Scaling

- Increase database connection pool size
- Add more CPU/RAM to servers
- Enable Redis caching

## Troubleshooting

### Backend not starting
```bash
# Check logs
journalctl -u backend -f

# Verify database connection
psql -U postgres -h localhost -d multi_school_db
```

### Frontend not loading
```bash
# Check PM2 status
pm2 status

# Restart frontend
pm2 restart frontend
```

### Database connection errors
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Verify credentials
cat /var/www/backend/.env | grep DATABASE_URL
```

## Security Checklist

- [ ] Change default passwords
- [ ] Enable firewall (ufw)
- [ ] Configure fail2ban
- [ ] Enable automatic security updates
- [ ] Set up monitoring (Datadog, New Relic, etc.)
- [ ] Configure log rotation
- [ ] Regular security audits

## Post-Deployment

1. Create first school via Super Admin panel
2. Test tenant isolation
3. Run E2E tests against production
4. Monitor error rates
5. Set up alerting

## Support

For deployment issues:
- GitHub Issues: https://github.com/yourorg/multi-school-platform/issues
- Email: devops@yourdomain.com
