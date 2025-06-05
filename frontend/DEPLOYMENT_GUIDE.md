# NOSS Frontend Deployment Guide

## 🚀 Production Deployment

### 1. Build for Production

```bash
cd /home/wjadmin/Dev/wj_noss/frontend
npm run build
```

The build output will be in the `dist/` directory.

### 2. Environment Configuration

Create production environment file:

```bash
# .env.production
VUE_APP_API_BASE_URL=https://your-api-domain.com/api
VUE_APP_WS_URL=wss://your-api-domain.com/ws
VUE_APP_ENABLE_CHAT=true
VUE_APP_ENABLE_ANALYTICS=true
VUE_APP_DEBUG=false
```

### 3. Docker Deployment

Create `Dockerfile` in frontend directory:

```dockerfile
# Multi-stage build
FROM node:18-alpine as build-stage

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Create `nginx.conf`:

```nginx
user nginx;
worker_processes auto;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    server {
        listen 80;
        server_name localhost;
        root /usr/share/nginx/html;
        index index.html;

        # Handle Vue.js routing
        location / {
            try_files $uri $uri/ /index.html;
        }

        # API proxy (if needed)
        location /api/ {
            proxy_pass http://backend:8000/api/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # WebSocket proxy
        location /ws {
            proxy_pass http://backend:8000/ws;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
        }
    }
}
```

### 4. Docker Compose Integration

Update your main `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/noss
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    environment:
      - VUE_APP_API_BASE_URL=http://localhost:8000/api

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=noss
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### 5. CI/CD Pipeline

Example GitHub Actions workflow (`.github/workflows/deploy.yml`):

```yaml
name: Deploy NOSS Frontend

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
        cache-dependency-path: frontend/package-lock.json
    
    - name: Install dependencies
      run: |
        cd frontend
        npm ci
    
    - name: Build application
      run: |
        cd frontend
        npm run build
      env:
        VUE_APP_API_BASE_URL: ${{ secrets.API_BASE_URL }}
    
    - name: Deploy to server
      uses: appleboy/scp-action@v0.1.4
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        source: "frontend/dist/*"
        target: "/var/www/noss"
```

## 🔧 Server Configuration

### Nginx (Direct deployment)

```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /var/www/noss/dist;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml text/javascript;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Handle Vue.js routing
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### SSL Configuration (with Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 📊 Performance Optimization

### 1. Bundle Analysis

```bash
# Install bundle analyzer
npm install --save-dev rollup-plugin-visualizer

# Add to vite.config.js
import { visualizer } from 'rollup-plugin-visualizer'

export default {
  plugins: [
    vue(),
    visualizer({
      filename: 'dist/stats.html',
      open: true
    })
  ]
}
```

### 2. Code Splitting

Already implemented in the current setup with dynamic imports for admin routes.

### 3. Progressive Web App (PWA)

```bash
# Install PWA plugin
npm install --save-dev vite-plugin-pwa

# Add to vite.config.js
import { VitePWA } from 'vite-plugin-pwa'

export default {
  plugins: [
    vue(),
    VitePWA({
      registerType: 'autoUpdate',
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg}']
      },
      manifest: {
        name: 'NOSS Education System',
        short_name: 'NOSS',
        description: 'National Occupational Skills Standard Education System',
        theme_color: '#2563eb',
        icons: [
          {
            src: 'pwa-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          }
        ]
      }
    })
  ]
}
```

## 🔍 Monitoring & Analytics

### 1. Error Tracking (Sentry)

```bash
npm install @sentry/vue @sentry/tracing
```

```javascript
// main.js
import * as Sentry from "@sentry/vue"

Sentry.init({
  app,
  dsn: "YOUR_SENTRY_DSN",
  integrations: [
    new Sentry.BrowserTracing(),
  ],
  tracesSampleRate: 1.0,
})
```

### 2. Analytics (Google Analytics)

```bash
npm install vue-gtag
```

```javascript
// main.js
import VueGtag from "vue-gtag"

app.use(VueGtag, {
  config: {
    id: "GA_MEASUREMENT_ID"
  }
})
```

## 🧪 Testing in Production

### Health Check Endpoint

Create a simple health check:

```javascript
// public/health.json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-06-05T05:40:00Z"
}
```

### Monitoring Script

```bash
#!/bin/bash
# health-check.sh

URL="https://your-domain.com/health.json"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" $URL)

if [ $STATUS -eq 200 ]; then
    echo "✅ Frontend is healthy"
else
    echo "❌ Frontend is down (Status: $STATUS)"
    # Send alert
fi
```

## 📱 Mobile App Deployment (Optional)

### Capacitor Integration

```bash
npm install @capacitor/core @capacitor/cli
npx cap init
npm install @capacitor/android @capacitor/ios

# Build and sync
npm run build
npx cap sync

# Open in native IDE
npx cap open android
npx cap open ios
```

---

## ✅ Deployment Checklist

- [ ] Environment variables configured
- [ ] API endpoints tested
- [ ] SSL certificate installed
- [ ] Gzip compression enabled
- [ ] Security headers configured
- [ ] Error tracking setup
- [ ] Analytics configured
- [ ] Health checks implemented
- [ ] Backup strategy defined
- [ ] Monitoring alerts configured

**Production URL**: Ready to deploy at your domain
**Status**: ✅ Production Ready
**Performance**: Optimized for production use
