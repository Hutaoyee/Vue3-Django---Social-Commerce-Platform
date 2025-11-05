# 🚀 发布和上传 GitHub 快速检查清单

## 📋 发布前必做事项

### 🔐 后端安全配置

- [ ] 修改 `backend/backend/settings.py` 中的 `SECRET_KEY`
  ```python
  # 生成新密钥: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
- [ ] 设置 `DEBUG = False`
- [ ] 配置 `ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']`
- [ ] 创建 `.env` 文件（从 `.env.example` 复制）
- [ ] 数据库密码改为强密码
- [ ] 关闭 `CORS_ALLOW_ALL_ORIGINS`，设置具体域名
- [ ] 运行配置检查: `python backend/check_production.py`

### 🎨 前端配置

- [ ] 创建 `.env.production` 文件
- [ ] 配置正确的 API 地址 `VITE_API_BASE_URL`
- [ ] 移除所有 `console.log()`
- [ ] 运行构建测试: `npm run build`
- [ ] 检查构建产物大小（dist 文件夹）

### 🗄️ 数据库

- [ ] 备份当前数据库
- [ ] 确保所有迁移已应用: `python manage.py migrate`
- [ ] 测试数据库连接

### 📦 依赖管理

- [ ] 生成/更新 `requirements.txt`: `pip freeze > requirements.txt`
- [ ] 确保 `package.json` 版本正确
- [ ] 移除不需要的开发依赖

### 🧪 测试

- [ ] 运行后端测试: `python manage.py test`
- [ ] 运行前端测试: `npm run test:unit`
- [ ] 手动测试主要功能
- [ ] 测试用户登录/注册流程
- [ ] 测试商品展示和搜索
- [ ] 测试图片上传功能

### 📁 文件清理

- [ ] 删除测试数据和临时文件
- [ ] 清理 `media/` 文件夹中的测试图片
- [ ] 移除未使用的代码和注释
- [ ] 检查是否有硬编码的测试数据

## 📤 上传到 GitHub

### 🔧 准备工作

- [ ] 确保 `.gitignore` 文件完整
- [ ] 检查没有提交敏感信息:
  - [ ] `.env` 文件
  - [ ] 数据库密码
  - [ ] API 密钥
  - [ ] `media/` 文件夹（可选）
  - [ ] `__pycache__/`
  - [ ] `node_modules/`

### 📝 Git 操作

```bash
# 1. 初始化仓库（如果还没有）
git init

# 2. 添加所有文件
git add .

# 3. 查看状态，确认没有敏感文件
git status

# 4. 提交
git commit -m "Initial commit: Social Commerce Platform"

# 5. 在 GitHub 创建仓库后
git remote add origin https://github.com/yourusername/social-commerce.git

# 6. 推送
git branch -M main
git push -u origin main
```

### 🔒 GitHub 仓库设置

- [ ] 创建 GitHub 仓库（Private 或 Public）
- [ ] 添加 README.md 说明
- [ ] 设置 GitHub Secrets（Settings > Secrets and variables > Actions）:
  - [ ] `SECRET_KEY`
  - [ ] `DB_PASSWORD`
  - [ ] 其他敏感环境变量
- [ ] 启用 GitHub Actions（可选）
- [ ] 添加 License 文件（可选）

## 📊 部署准备

### 🖥️ 服务器环境

- [ ] Python 3.11+ 已安装
- [ ] Node.js 20+ 已安装
- [ ] MySQL 8.0+ 已安装并运行
- [ ] Nginx 或 Apache 已安装
- [ ] 配置防火墙规则

### 🔄 部署流程

#### 后端部署

```bash
# 1. 克隆代码
git clone https://github.com/yourusername/social-commerce.git
cd social-commerce

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp backend/.env.example backend/.env
# 编辑 .env 文件

# 5. 数据库迁移
cd backend
python manage.py migrate

# 6. 收集静态文件
python manage.py collectstatic --noinput

# 7. 创建超级用户
python manage.py createsuperuser

# 8. 运行（开发）
python manage.py runserver

# 或使用 Gunicorn（生产）
gunicorn backend.wsgi:application --bind 0.0.0.0:8000
```

#### 前端部署

```bash
# 1. 安装依赖
cd frontend
npm install

# 2. 创建生产环境配置
cp .env.example .env.production
# 编辑 .env.production

# 3. 构建
npm run build

# 4. 部署 dist 文件夹到 Web 服务器
```

## ✅ 部署后检查

- [ ] 网站可以访问
- [ ] API 端点正常响应
- [ ] 静态文件加载正常
- [ ] 图片上传功能正常
- [ ] 用户登录/注册正常
- [ ] HTTPS 正常工作（如果配置了）
- [ ] 跨域请求正常
- [ ] 数据库连接正常
- [ ] 日志记录正常

## 🚨 注意事项

### ⚠️ 绝对不要提交到 Git

- ❌ `.env` 文件
- ❌ `db.sqlite3` 数据库文件
- ❌ 真实的数据库密码
- ❌ `SECRET_KEY`
- ❌ API 密钥和 token
- ❌ 用户上传的真实图片（`media/` 文件夹）
- ❌ `__pycache__/` 和 `.pyc` 文件
- ❌ `node_modules/`
- ❌ `dist/` 构建产物
- ❌ 个人开发配置（`.vscode/`, `.idea/`）

### ✅ 应该提交到 Git

- ✅ `.env.example` 示例文件
- ✅ `.gitignore` 文件
- ✅ `requirements.txt`
- ✅ `package.json` 和 `package-lock.json`
- ✅ 所有源代码
- ✅ 文档文件
- ✅ 配置文件示例

## 🔧 快速命令参考

```bash
# 生成新的 SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 检查生产环境配置
python backend/check_production.py

# 查看 Git 状态
git status

# 查看将要提交的文件
git diff --cached

# 查看忽略的文件是否正确
git status --ignored

# 生成 requirements.txt
pip freeze > requirements.txt

# Django 检查
python manage.py check --deploy

# 收集静态文件
python manage.py collectstatic --noinput

# 前端构建
npm run build

# 前端代码检查
npm run lint
```

## 📚 相关文档

- [README.md](README.md) - 项目说明
- [DEPLOYMENT.md](DEPLOYMENT.md) - 详细部署指南
- [API_TESTING_GUIDE.md](API_TESTING_GUIDE.md) - API 测试文档
- [PRODUCT_MANAGEMENT_GUIDE.md](PRODUCT_MANAGEMENT_GUIDE.md) - 商品管理文档

## 🆘 问题排查

### 常见错误

1. **CORS 错误**: 检查 `CORS_ALLOWED_ORIGINS` 配置
2. **静态文件 404**: 运行 `collectstatic` 并检查 Nginx 配置
3. **数据库连接失败**: 检查数据库凭据和防火墙
4. **500 错误**: 查看 Django 日志，检查 `DEBUG` 设置

### 获取帮助

- 查看日志文件
- 运行 `python manage.py check --deploy`
- 检查环境变量是否正确加载
- 验证数据库迁移是否完整

---

## 🎉 完成后

恭喜！你的项目已经准备好发布了！

记得定期：
- 🔄 更新依赖包
- 💾 备份数据库
- 📊 监控服务器性能
- 🔒 审查安全日志
