# Deployment Guide

Complete guide for deploying Outcomist to production.

## Table of Contents

- [Docker Deployment](#docker-deployment)
- [Environment Configuration](#environment-configuration)
- [Data Persistence](#data-persistence)
- [Cloud Deployment](#cloud-deployment)
- [Scaling Considerations](#scaling-considerations)
- [Monitoring](#monitoring)
- [Backup and Recovery](#backup-and-recovery)

## Docker Deployment

### Quick Start

1. **Prepare environment file:**
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

2. **Build and start services:**
   ```bash
   docker-compose up -d
   ```

3. **Verify services are running:**
   ```bash
   docker-compose ps
   ```

4. **Check logs:**
   ```bash
   docker-compose logs -f
   ```

5. **Stop services:**
   ```bash
   docker-compose down
   ```

### Production Configuration

For production, create a `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    container_name: outcomist-backend-prod
    ports:
      - "8000:8000"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - DATABASE_URL=sqlite:///./data/database.sqlite
      - DATA_DIR=./data/projects
      - LOG_LEVEL=warning
    volumes:
      - ./data:/app/data
    restart: always
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G

  frontend:
    build: ./frontend
    container_name: outcomist-frontend-prod
    ports:
      - "80:80"
    depends_on:
      backend:
        condition: service_healthy
    restart: always
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M

volumes:
  data:
```

Run with:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Environment Configuration

### Required Variables

- `ANTHROPIC_API_KEY` - Your Claude API key from [Anthropic Console](https://console.anthropic.com/)

### Optional Variables

- `DATABASE_URL` - Database connection string
  - Default: `sqlite:///./data/database.sqlite`
  - For PostgreSQL: `postgresql://user:password@host:port/database`

- `DATA_DIR` - Directory for generated project files
  - Default: `./data/projects`

- `LOG_LEVEL` - Application logging level
  - Options: `debug`, `info`, `warning`, `error`
  - Default: `info`

### Security Considerations

1. **Never commit `.env` file** - Add to `.gitignore`
2. **Rotate API keys regularly** - Update in Anthropic Console
3. **Use secrets management** - Consider AWS Secrets Manager, HashiCorp Vault, etc.
4. **Restrict file permissions** - `chmod 600 .env`

## Data Persistence

### Volume Mapping

The `./data` directory is mounted to the backend container:
- `database.sqlite` - All application data
- `projects/` - Generated files organized by project ID

### Backup Strategy

**Automated Backup Script:**

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DATA_DIR="./data"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
sqlite3 $DATA_DIR/database.sqlite ".backup '$BACKUP_DIR/database_$DATE.sqlite'"

# Backup project files
tar -czf $BACKUP_DIR/projects_$DATE.tar.gz $DATA_DIR/projects/

# Keep only last 7 days of backups
find $BACKUP_DIR -name "database_*.sqlite" -mtime +7 -delete
find $BACKUP_DIR -name "projects_*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

**Schedule with cron:**
```bash
# Run daily at 2 AM
0 2 * * * /path/to/backup.sh
```

### Restore from Backup

```bash
# Stop the application
docker-compose down

# Restore database
cp /backups/database_YYYYMMDD_HHMMSS.sqlite ./data/database.sqlite

# Restore project files
tar -xzf /backups/projects_YYYYMMDD_HHMMSS.tar.gz -C ./data/

# Restart application
docker-compose up -d
```

## Cloud Deployment

### Railway

Railway provides the simplest deployment experience.

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login:**
   ```bash
   railway login
   ```

3. **Initialize project:**
   ```bash
   railway init
   ```

4. **Deploy backend:**
   ```bash
   cd backend
   railway up
   railway variables set ANTHROPIC_API_KEY=your_key_here
   ```

5. **Deploy frontend:**
   ```bash
   cd frontend
   railway up
   ```

6. **Link services:**
   - Update frontend `VITE_API_URL` to backend Railway URL
   - Redeploy frontend

### Fly.io

Fly.io offers global edge deployment.

1. **Install flyctl:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login:**
   ```bash
   fly auth login
   ```

3. **Deploy backend:**
   ```bash
   cd backend
   fly launch --name outcomist-backend
   fly secrets set ANTHROPIC_API_KEY=your_key_here
   fly deploy
   ```

4. **Deploy frontend:**
   ```bash
   cd frontend
   fly launch --name outcomist-frontend
   fly deploy
   ```

5. **Configure networking:**
   - Update frontend environment to point to backend URL
   - Redeploy frontend

### Vercel + Backend Hosting

Deploy frontend to Vercel, backend to Railway/Fly.io.

**Frontend on Vercel:**
```bash
cd frontend
npm install -g vercel
vercel
```

**Backend on Railway:**
```bash
cd backend
railway up
railway variables set ANTHROPIC_API_KEY=your_key_here
```

**Update frontend environment:**
- Add `VITE_API_URL` environment variable in Vercel dashboard
- Point to Railway backend URL

### AWS Deployment

#### Using ECS (Elastic Container Service)

1. **Push images to ECR:**
   ```bash
   # Backend
   aws ecr create-repository --repository-name outcomist-backend
   docker tag outcomist-backend:latest <account>.dkr.ecr.<region>.amazonaws.com/outcomist-backend:latest
   docker push <account>.dkr.ecr.<region>.amazonaws.com/outcomist-backend:latest

   # Frontend
   aws ecr create-repository --repository-name outcomist-frontend
   docker tag outcomist-frontend:latest <account>.dkr.ecr.<region>.amazonaws.com/outcomist-frontend:latest
   docker push <account>.dkr.ecr.<region>.amazonaws.com/outcomist-frontend:latest
   ```

2. **Create ECS task definitions** for backend and frontend

3. **Create ECS services** with Application Load Balancer

4. **Configure environment variables** in task definitions

5. **Set up RDS for PostgreSQL** (recommended over SQLite for production)

#### Using Elastic Beanstalk

1. **Install EB CLI:**
   ```bash
   pip install awsebcli
   ```

2. **Initialize:**
   ```bash
   eb init -p docker outcomist
   ```

3. **Create environment:**
   ```bash
   eb create outcomist-prod
   ```

4. **Deploy:**
   ```bash
   eb deploy
   ```

## Scaling Considerations

### Current Architecture (MVP)

- SQLite database (single file)
- File system storage
- Single backend instance
- Single frontend instance

**Limitations:**
- SQLite doesn't scale to multiple writers
- File system doesn't work with multiple instances
- No session management across instances

### Scaling Recommendations

#### 1. Database Migration

**Move from SQLite to PostgreSQL:**

```python
# Update DATABASE_URL in .env
DATABASE_URL=postgresql://user:password@host:port/database
```

**Benefits:**
- Multiple concurrent connections
- Better performance at scale
- ACID compliance
- Mature ecosystem

**Managed Options:**
- AWS RDS
- Google Cloud SQL
- Azure Database for PostgreSQL
- Railway PostgreSQL
- Supabase

#### 2. File Storage Migration

**Move from file system to S3:**

```python
# backend/src/services/storage.py
import boto3

s3_client = boto3.client('s3')

def save_file(project_id: str, filename: str, content: str):
    key = f"projects/{project_id}/{filename}"
    s3_client.put_object(
        Bucket='outcomist-files',
        Key=key,
        Body=content.encode('utf-8')
    )
```

**Benefits:**
- Unlimited storage
- No disk management
- Built-in redundancy
- CDN integration

**Options:**
- AWS S3
- Google Cloud Storage
- Azure Blob Storage
- Cloudflare R2 (S3-compatible, no egress fees)

#### 3. Add Caching

**Redis for session management and caching:**

```python
# backend/requirements.txt
redis==5.0.0

# backend/src/cache.py
import redis

cache = redis.Redis(host='localhost', port=6379, decode_responses=True)

def cache_project(project_id: str, data: dict):
    cache.setex(f"project:{project_id}", 3600, json.dumps(data))
```

**Use cases:**
- Session management
- Rate limiting
- API response caching
- Streaming message buffering

#### 4. Load Balancing

**Nginx as reverse proxy:**

```nginx
upstream backend {
    server backend-1:8000;
    server backend-2:8000;
    server backend-3:8000;
}

server {
    listen 80;
    location /api/ {
        proxy_pass http://backend;
    }
}
```

**Managed Options:**
- AWS Application Load Balancer
- Google Cloud Load Balancing
- Cloudflare Load Balancing

#### 5. Horizontal Scaling

**Docker Compose with replicas:**

```yaml
services:
  backend:
    build: ./backend
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1'
          memory: 1G
```

**Kubernetes for orchestration:**
- Amazon EKS
- Google GKE
- Azure AKS
- Self-hosted K8s

## Monitoring

### Health Checks

**Backend health endpoint:**
```bash
curl http://localhost:8000/health
```

**Frontend health check:**
```bash
curl http://localhost:3000/
```

### Logging

**View Docker logs:**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Last 100 lines
docker-compose logs --tail=100 backend
```

**Log aggregation options:**
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Grafana Loki
- CloudWatch Logs (AWS)
- Google Cloud Logging
- Azure Monitor

### Metrics and Alerting

**Prometheus + Grafana:**

```yaml
# docker-compose.monitoring.yml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

**Key metrics to track:**
- Request rate (requests/second)
- Error rate (errors/second)
- Response time (p50, p95, p99)
- Database connection pool usage
- Memory and CPU usage
- Disk space utilization

**Alerting tools:**
- PagerDuty
- Opsgenie
- Slack webhooks
- Email alerts

### Application Performance Monitoring (APM)

**Options:**
- Sentry (error tracking)
- New Relic
- Datadog
- Honeycomb

**Example Sentry integration:**

```python
# backend/requirements.txt
sentry-sdk==1.40.0

# backend/src/main.py
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0,
)
```

## Backup and Recovery

### Automated Backups

**AWS RDS automated backups:**
- Retention period: 7-35 days
- Point-in-time recovery
- Cross-region snapshots

**S3 versioning:**
```bash
aws s3api put-bucket-versioning \
  --bucket outcomist-files \
  --versioning-configuration Status=Enabled
```

### Disaster Recovery Plan

1. **Regular Testing**
   - Test restore procedure monthly
   - Document recovery time objective (RTO)
   - Document recovery point objective (RPO)

2. **Multi-Region Setup**
   - Primary region: US East
   - Backup region: US West
   - Automatic failover with Route 53

3. **Incident Response**
   - Document runbook
   - Define escalation procedures
   - Maintain contact list

## Security Checklist

- [ ] Use HTTPS in production
- [ ] Rotate API keys regularly
- [ ] Implement rate limiting
- [ ] Add authentication/authorization
- [ ] Enable CORS properly
- [ ] Use secrets management
- [ ] Regular security updates
- [ ] Database encryption at rest
- [ ] Network security groups/firewall
- [ ] DDoS protection (Cloudflare)

## Performance Optimization

### Backend

- [ ] Add database indexes
- [ ] Implement connection pooling
- [ ] Use async/await for I/O
- [ ] Cache frequently accessed data
- [ ] Optimize database queries

### Frontend

- [ ] Enable gzip compression
- [ ] Minify and bundle assets
- [ ] Use CDN for static files
- [ ] Implement code splitting
- [ ] Add service worker for caching

### Network

- [ ] Use HTTP/2
- [ ] Enable CDN
- [ ] Optimize image sizes
- [ ] Implement lazy loading
- [ ] Add browser caching headers

## Cost Optimization

### Development
- Use free tiers (Railway, Fly.io)
- SQLite for database
- File system storage
- Single instance

### Small Scale (< 100 users)
- Shared hosting or PaaS
- Small database instance
- Minimal S3 storage
- ~$20-50/month

### Medium Scale (100-1000 users)
- Dedicated instances
- PostgreSQL managed service
- S3 with CloudFront
- Redis cache
- ~$100-300/month

### Large Scale (1000+ users)
- Multiple instances with load balancer
- High-availability database
- S3 + CDN
- Redis cluster
- ~$500-1000+/month

## Troubleshooting

### Common Issues

**Backend won't start:**
```bash
# Check logs
docker-compose logs backend

# Common fixes:
# - Verify ANTHROPIC_API_KEY is set
# - Check database file permissions
# - Ensure port 8000 is available
```

**Frontend can't connect to backend:**
```bash
# Check network connectivity
docker-compose exec frontend curl http://backend:8000/health

# Common fixes:
# - Update API URL in frontend environment
# - Check CORS configuration
# - Verify backend is running
```

**Database locked errors:**
```bash
# SQLite doesn't support multiple writers
# Solution: Migrate to PostgreSQL
```

**Out of disk space:**
```bash
# Check disk usage
df -h

# Clean up Docker
docker system prune -a
```

## Next Steps

After successful deployment:

1. [ ] Set up monitoring and alerting
2. [ ] Configure automated backups
3. [ ] Implement CI/CD pipeline
4. [ ] Add authentication
5. [ ] Enable HTTPS
6. [ ] Plan scaling strategy
7. [ ] Document runbooks
8. [ ] Test disaster recovery

## Support

For deployment issues:
- Check [GitHub Issues](https://github.com/your-repo/issues)
- Review [API Documentation](API.md)
- Consult [User Guide](USER_GUIDE.md)
