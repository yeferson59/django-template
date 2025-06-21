# Deployment Guide

## 🚀 Production Deployment

### Prerequisites
- Docker & Docker Compose
- PostgreSQL database
- Redis (optional, for caching)
- Reverse proxy (Nginx recommended)
- SSL certificate

### Environment Variables

Create a `.env.prod` file with the following variables:

```bash
# Django settings
DEBUG=false
SECRET_KEY=your-very-secure-secret-key-here
DJANGO_SETTINGS_MODULE=app.settings_prod
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgres://user:password@host:port/database

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# Email settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Sentry (optional)
SENTRY_DSN=https://your-sentry-dsn-here

# Static files (AWS S3)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
```

### Docker Production Setup

1. **Build the production image:**
```bash
docker build -t my-django-app:latest .
```

2. **Create docker-compose.prod.yml:**
```yaml
version: '3.8'

services:
  web:
    image: my-django-app:latest
    env_file: .env.prod
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data/

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

3. **Deploy:**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Manual Server Setup

#### 1. Server Preparation (Ubuntu/Debian)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.13 python3.13-venv python3-pip nginx postgresql redis-server

# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 2. Database Setup

```bash
# Create PostgreSQL database and user
sudo -u postgres psql
CREATE DATABASE myapp_prod;
CREATE USER myapp_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE myapp_prod TO myapp_user;
\q
```

#### 3. Application Setup

```bash
# Clone repository
git clone https://github.com/your-username/your-repo.git
cd your-repo

# Create production environment
uv sync --group prod

# Create .env file
cp .env.example .env
# Edit .env with production values

# Run migrations
uv run python manage.py migrate

# Collect static files
uv run python manage.py collectstatic --noinput

# Create superuser
uv run python manage.py createsuperuser
```

#### 4. Gunicorn Setup

Create `/etc/systemd/system/gunicorn.service`:

```ini
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
RuntimeDirectory=gunicorn
WorkingDirectory=/path/to/your/app
ExecStart=/path/to/your/app/.venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn/gunicorn.sock \
          app.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Create `/etc/systemd/system/gunicorn.socket`:

```ini
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn/gunicorn.sock
SocketUser=www-data
SocketGroup=www-data

[Install]
WantedBy=sockets.target
```

Enable and start services:

```bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```

#### 5. Nginx Configuration

Create `/etc/nginx/sites-available/myapp`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/ssl/certs/yourdomain.com.crt;
    ssl_certificate_key /etc/ssl/private/yourdomain.com.key;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root /path/to/your/app;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        root /path/to/your/app;
        expires 7d;
        add_header Cache-Control "public";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn/gunicorn.sock;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Platform-Specific Deployments

#### Heroku

1. **Create Procfile:**
```
web: gunicorn app.wsgi:application
release: python manage.py migrate
```

2. **Add buildpacks:**
```bash
heroku buildpacks:set heroku/python
```

3. **Set environment variables:**
```bash
heroku config:set DEBUG=false
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DJANGO_SETTINGS_MODULE=app.settings_prod
```

#### DigitalOcean App Platform

Create `app.yaml`:

```yaml
name: my-django-app
services:
- name: web
  source_dir: /
  github:
    repo: your-username/your-repo
    branch: main
  run_command: gunicorn app.wsgi:application
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  env:
  - key: DEBUG
    value: "false"
  - key: SECRET_KEY
    value: your-secret-key
    type: SECRET
databases:
- name: db
  engine: PG
  version: "15"
```

#### Railway

1. **Connect GitHub repository**
2. **Set environment variables in Railway dashboard**
3. **Deploy automatically on push**

### Health Checks

Add health check endpoints to your Django app:

```python
# app/views.py
from django.http import JsonResponse
from django.db import connections
from django.core.cache import cache

def health_check(request):
    """Health check endpoint for load balancers."""
    try:
        # Check database
        db_conn = connections['default']
        db_conn.cursor()

        # Check cache
        cache.set('health_check', 'ok', 30)
        cache.get('health_check')

        return JsonResponse({'status': 'healthy'})
    except Exception as e:
        return JsonResponse({'status': 'unhealthy', 'error': str(e)}, status=500)
```

Add to urls.py:
```python
urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    # ... other patterns
]
```

### Monitoring

#### 1. Application Monitoring with Sentry

Add to settings:
```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

if not DEBUG and os.getenv('SENTRY_DSN'):
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True
    )
```

#### 2. Server Monitoring

Install monitoring tools:
```bash
# Install htop, netstat, etc.
sudo apt install -y htop net-tools

# Install log rotation
sudo apt install -y logrotate
```

### Backup Strategy

#### 1. Database Backup

Create backup script `/opt/backup/db_backup.sh`:
```bash
#!/bin/bash
BACKUP_DIR="/opt/backups/db"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="myapp_prod"

mkdir -p $BACKUP_DIR

pg_dump $DB_NAME > $BACKUP_DIR/backup_$DATE.sql

# Keep only last 7 days
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete
```

Add to crontab:
```bash
0 2 * * * /opt/backup/db_backup.sh
```

#### 2. Media Files Backup

```bash
#!/bin/bash
rsync -av /path/to/media/ user@backup-server:/backups/media/
```

### Security Checklist

- [ ] Use HTTPS everywhere
- [ ] Set secure environment variables
- [ ] Enable Django security middleware
- [ ] Configure CORS properly
- [ ] Set up fail2ban
- [ ] Regular security updates
- [ ] Monitor access logs
- [ ] Use strong passwords
- [ ] Enable two-factor authentication
- [ ] Regular backups

### Performance Optimization

1. **Enable Gzip compression in Nginx**
2. **Set up CDN for static files**
3. **Configure Redis caching**
4. **Optimize database queries**
5. **Use database connection pooling**
6. **Monitor with APM tools**

### Troubleshooting

#### Common Issues

1. **Static files not loading:**
   ```bash
   # Collect static files
   python manage.py collectstatic --noinput

   # Check Nginx configuration
   sudo nginx -t
   ```

2. **Database connection errors:**
   ```bash
   # Check PostgreSQL status
   sudo systemctl status postgresql

   # Check database connectivity
   python manage.py dbshell
   ```

3. **Gunicorn not starting:**
   ```bash
   # Check logs
   sudo journalctl -u gunicorn

   # Check socket
   sudo systemctl status gunicorn.socket
   ```

#### Log Locations

- **Django logs:** `/path/to/app/logs/django.log`
- **Nginx logs:** `/var/log/nginx/access.log`, `/var/log/nginx/error.log`
- **Gunicorn logs:** `sudo journalctl -u gunicorn`
- **PostgreSQL logs:** `/var/log/postgresql/postgresql-15-main.log`

For more detailed troubleshooting, check the respective service logs and ensure all environment variables are properly set.
