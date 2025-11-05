# 部署指南

## 发布前检查清单

### 1. 后端 Django 配置

#### ✅ 安全设置

- [ ] 修改 `SECRET_KEY` 为随机密钥
- [ ] 设置 `DEBUG = False`
- [ ] 配置 `ALLOWED_HOSTS`
- [ ] 使用环境变量存储敏感信息
- [ ] 启用 HTTPS 相关安全设置

#### ✅ 数据库

- [ ] 备份数据库
- [ ] 配置生产数据库
- [ ] 运行所有迁移
- [ ] 创建必要的初始数据

#### ✅ 静态文件和媒体文件

- [ ] 运行 `python manage.py collectstatic`
- [ ] 配置媒体文件存储（本地或云存储）
- [ ] 设置正确的文件权限

#### ✅ CORS 配置

- [ ] 关闭 `CORS_ALLOW_ALL_ORIGINS`
- [ ] 配置具体的 `CORS_ALLOWED_ORIGINS`

### 2. 前端 Vue 配置

#### ✅ 环境配置

- [ ] 创建 `.env.production` 文件
- [ ] 配置生产环境 API 地址
- [ ] 检查所有 API 端点

#### ✅ 构建优化

- [ ] 运行 `npm run build`
- [ ] 检查构建输出大小
- [ ] 测试构建后的应用

#### ✅ 性能优化

- [ ] 启用代码分割
- [ ] 压缩图片资源
- [ ] 配置 CDN（可选）

### 3. 通用检查

- [ ] 移除所有 console.log 和调试代码
- [ ] 检查错误处理
- [ ] 测试所有功能
- [ ] 准备回滚方案

## 上传到 GitHub

### 1. 初始化 Git 仓库

```bash
git init
git add .
git commit -m "Initial commit"
```

### 2. 创建 GitHub 仓库

在 GitHub 上创建新仓库（不要初始化 README）

### 3. 推送代码

```bash
git remote add origin https://github.com/yourusername/social-commerce.git
git branch -M main
git push -u origin main
```

### 4. 设置 GitHub Actions（可选）

创建 `.github/workflows/ci.yml` 用于自动化测试和部署。

### 5. 保护敏感信息

确保以下文件在 `.gitignore` 中：

- `.env` 文件
- 数据库文件
- `media/` 文件夹（看需求）
- `__pycache__/`
- `node_modules/`
- `dist/`

### 6. 使用 GitHub Secrets

在 GitHub 仓库设置中添加敏感环境变量：

- `SECRET_KEY`
- `DB_PASSWORD`
- 其他 API 密钥

## 生产环境部署

### 方案 1: 传统服务器部署

#### 后端部署（使用 Gunicorn + Nginx）

1. 安装依赖：

```bash
pip install -r requirements.txt
```

2. 使用 Gunicorn 运行：

```bash
gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

3. 配置 Nginx：

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /media/ {
        alias /path/to/backend/media/;
    }

    location /static/ {
        alias /path/to/backend/staticfiles/;
    }

    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
}
```

#### 前端部署

1. 构建：

```bash
cd frontend
npm run build
```

2. 将 `dist/` 目录上传到服务器

### 方案 2: Docker 部署

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: socialCommerce
      MYSQL_ROOT_PASSWORD: ${DB_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql

  backend:
    build: ./backend
    command: gunicorn backend.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - ./backend:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      - db
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=False
      - DB_HOST=db

  frontend:
    build: ./frontend
    volumes:
      - ./frontend/dist:/usr/share/nginx/html

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/static
      - media_volume:/media
    depends_on:
      - backend
      - frontend

volumes:
  mysql_data:
  static_volume:
  media_volume:
```

### 方案 3: 云平台部署

#### Vercel (前端)

```bash
cd frontend
npm run build
vercel --prod
```

#### Railway/Render (后端)

1. 连接 GitHub 仓库
2. 配置环境变量
3. 设置启动命令：`gunicorn backend.wsgi:application`

## 环境变量配置

### 后端 `.env`

```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=socialCommerce
DB_USER=dbuser
DB_PASSWORD=secure-password
DB_HOST=db-server
DB_PORT=3306
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

### 前端 `.env.production`

```env
VITE_API_BASE_URL=https://api.yourdomain.com
VITE_APP_TITLE=Social Commerce
```

## 监控和维护

### 日志管理

配置 Django 日志：

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/path/to/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### 备份策略

1. 数据库定期备份
2. 媒体文件备份
3. 配置文件版本控制

### 性能优化

1. 启用 Django 缓存
2. 使用 CDN 加速静态资源
3. 配置数据库连接池
4. 启用 Gzip 压缩

## 常见问题

### CORS 错误

确保后端 `CORS_ALLOWED_ORIGINS` 包含前端域名。

### 静态文件 404

运行 `python manage.py collectstatic` 并检查 Nginx 配置。

### 数据库连接失败

检查数据库凭据和网络连接。

### JWT Token 过期

前端需要实现 token 刷新机制。

## 回滚计划

1. 保留上一个稳定版本的代码
2. 数据库迁移要可逆
3. 准备回滚脚本
4. 监控部署后的错误率

## 安全最佳实践

1. 定期更新依赖包
2. 使用 HTTPS
3. 实施速率限制
4. 定期安全审计
5. 备份加密
6. 使用强密码策略
7. 启用日志审计

## 性能基准

部署后检查：
- 页面加载时间 < 3秒
- API 响应时间 < 500ms
- 数据库查询优化
- 前端资源大小 < 2MB
