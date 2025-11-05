#!/bin/bash
# 生产环境部署脚本

echo "🚀 开始部署..."

# 1. 拉取最新代码
echo "📥 拉取最新代码..."
git pull origin main

# 2. 后端部署
echo "🔧 部署后端..."
cd backend

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r ../requirements.txt

# 运行迁移
python manage.py migrate

# 收集静态文件
python manage.py collectstatic --noinput

# 重启 Gunicorn
sudo systemctl restart gunicorn

cd ..

# 3. 前端部署
echo "🎨 部署前端..."
cd frontend

# 安装依赖
npm ci

# 构建
npm run build

# 复制到 Nginx 目录
sudo cp -r dist/* /var/www/html/

cd ..

echo "✅ 部署完成!"
echo "🔍 检查服务状态..."
sudo systemctl status gunicorn
sudo systemctl status nginx
