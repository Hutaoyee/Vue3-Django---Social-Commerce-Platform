# 📋 Vue + Django 项目发布和 GitHub 上传指南

## 🎯 概述

本指南帮助你完成 Social Commerce 项目的发布准备和 GitHub 上传工作。

---

## ✅ 快速开始

### 第一步：运行配置检查

```bash
# 检查生产环境配置
python backend/check_production.py
```

### 第二步：生成新的密钥

```bash
# 生成新的 SECRET_KEY
python backend/generate_secret_key.py
```

### 第三步：配置环境变量

1. 后端配置：
```bash
cd backend
cp .env.example .env
# 编辑 .env 文件，填写实际值
```

2. 前端配置：
```bash
cd frontend
cp .env.example .env.production
# 编辑 .env.production，设置生产环境 API 地址
```

### 第四步：上传到 GitHub

```bash
# 1. 检查 .gitignore 是否完整
git status

# 2. 添加所有文件
git add .

# 3. 提交
git commit -m "Initial commit: Social Commerce Platform"

# 4. 推送到 GitHub
git remote add origin https://github.com/yourusername/social-commerce.git
git push -u origin main
```

---

## 📁 项目文件说明

### 已创建的重要文件

| 文件 | 说明 |
|------|------|
| `PRE_RELEASE_CHECKLIST.md` | 📋 **发布前完整检查清单** - 最重要！ |
| `DEPLOYMENT.md` | 📚 详细部署指南 |
| `README.md` | 📖 项目说明文档 |
| `.gitignore` | 🚫 Git 忽略文件配置 |
| `requirements.txt` | 📦 Python 依赖列表 |
| `backend/.env.example` | 🔧 后端环境变量示例 |
| `backend/.gitignore` | 🚫 后端 Git 忽略配置 |
| `backend/generate_secret_key.py` | 🔑 密钥生成脚本 |
| `backend/check_production.py` | ✅ 生产配置检查脚本 |
| `backend/backend/settings_prod.py` | ⚙️ 生产环境配置 |
| `frontend/.env.development` | 🔧 前端开发环境配置 |
| `frontend/.env.production` | 🔧 前端生产环境配置 |
| `frontend/.env.example` | 🔧 前端环境变量示例 |
| `.github/workflows/ci.yml` | 🔄 GitHub Actions CI/CD |
| `deploy.sh` | 🚀 Linux 部署脚本 |
| `deploy.ps1` | 🚀 Windows 部署脚本 |

---

## 🔧 关键配置变更

### 1. Django settings.py 已更新

现在支持从环境变量读取配置：

```python
# 从 .env 文件读取
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-value')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.mysql'),
        'NAME': os.environ.get('DB_NAME', 'socialCommerce'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}
```

### 2. 已添加依赖

- `python-dotenv` - 环境变量加载
- `gunicorn` - 生产服务器

---

## 🚨 重要安全提醒

### ❌ 绝对不要提交到 Git：

1. **`.env` 文件** - 包含真实密码和密钥
2. **`db.sqlite3`** - 数据库文件（如果使用 SQLite）
3. **`media/`** - 用户上传的真实图片
4. **`__pycache__/`** - Python 缓存
5. **`node_modules/`** - Node 依赖
6. **`dist/`** - 前端构建产物

### ✅ 应该提交：

1. **`.env.example`** - 环境变量示例（无真实密码）
2. **`.gitignore`** - Git 忽略配置
3. **所有源代码**
4. **`requirements.txt`** 和 `package.json`
5. **文档文件**

---

## 📊 发布前检查清单（精简版）

### 后端 Django

- [ ] 生成新的 `SECRET_KEY`
- [ ] 设置 `DEBUG = False`（在 .env 中）
- [ ] 配置 `ALLOWED_HOSTS`
- [ ] 修改数据库密码
- [ ] 关闭 `CORS_ALLOW_ALL_ORIGINS`
- [ ] 运行: `python backend/check_production.py`
- [ ] 运行: `python manage.py check --deploy`

### 前端 Vue

- [ ] 创建 `.env.production` 文件
- [ ] 设置正确的 `VITE_API_BASE_URL`
- [ ] 移除所有 `console.log()`
- [ ] 运行: `npm run build`
- [ ] 测试构建产物

### Git 准备

- [ ] 确认 `.gitignore` 完整
- [ ] 运行 `git status` 检查
- [ ] 确认没有敏感文件在提交列表中

---

## 🚀 部署流程

### 开发环境 → 生产环境

1. **本地测试**
   ```bash
   # 后端
   python manage.py runserver
   
   # 前端
   npm run dev
   ```

2. **构建生产版本**
   ```bash
   # 前端构建
   cd frontend
   npm run build
   
   # 后端收集静态文件
   cd backend
   python manage.py collectstatic
   ```

3. **部署到服务器**
   ```bash
   # 使用部署脚本
   ./deploy.sh  # Linux/Mac
   # 或
   .\deploy.ps1  # Windows
   ```

---

## 📞 命令速查表

```bash
# 生成新密钥
python backend/generate_secret_key.py

# 检查生产配置
python backend/check_production.py

# Django 部署检查
python manage.py check --deploy

# 数据库迁移
python manage.py migrate

# 收集静态文件
python manage.py collectstatic --noinput

# 创建超级用户
python manage.py createsuperuser

# 前端构建
npm run build

# Git 操作
git status
git add .
git commit -m "message"
git push
```

---

## 📚 延伸阅读

1. **[PRE_RELEASE_CHECKLIST.md](PRE_RELEASE_CHECKLIST.md)** ⭐ 最详细的检查清单
2. **[DEPLOYMENT.md](DEPLOYMENT.md)** - 完整部署指南
3. **[README.md](README.md)** - 项目说明
4. **Django 官方部署文档**: https://docs.djangoproject.com/en/stable/howto/deployment/

---

## 🆘 常见问题

### Q1: 如何生成新的 SECRET_KEY？

```bash
python backend/generate_secret_key.py
```

或者：

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Q2: 如何知道配置是否安全？

```bash
python backend/check_production.py
python manage.py check --deploy
```

### Q3: CORS 错误怎么办？

检查 `backend/.env` 文件中的 `CORS_ALLOWED_ORIGINS` 是否包含你的前端域名。

### Q4: 如何备份数据库？

```bash
# MySQL
mysqldump -u root -p socialCommerce > backup.sql

# 恢复
mysql -u root -p socialCommerce < backup.sql
```

### Q5: 前端构建后如何预览？

```bash
cd frontend
npm run preview
```

---

## ✨ 下一步

1. ✅ 完成 [PRE_RELEASE_CHECKLIST.md](PRE_RELEASE_CHECKLIST.md) 中的所有项目
2. 🚀 使用 [DEPLOYMENT.md](DEPLOYMENT.md) 部署到服务器
3. 📊 设置监控和日志
4. 🔄 配置自动备份
5. 🔒 定期安全审计

---

## 🎉 完成！

如果你已经完成了上述步骤，你的项目就可以安全地上传到 GitHub 并部署到生产环境了！

**记住**：安全第一，永远不要将敏感信息提交到 Git！

---

📝 **更新日期**: 2025年11月5日
