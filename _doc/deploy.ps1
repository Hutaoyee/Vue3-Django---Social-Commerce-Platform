# 生产环境部署脚本 (Windows PowerShell)

Write-Host "🚀 开始部署..." -ForegroundColor Green

# 1. 拉取最新代码
Write-Host "📥 拉取最新代码..." -ForegroundColor Cyan
git pull origin main

# 2. 后端部署
Write-Host "🔧 部署后端..." -ForegroundColor Cyan
Set-Location backend

# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 安装依赖
pip install -r ..\requirements.txt

# 运行迁移
python manage.py migrate

# 收集静态文件
python manage.py collectstatic --noinput

Set-Location ..

# 3. 前端部署
Write-Host "🎨 部署前端..." -ForegroundColor Cyan
Set-Location frontend

# 安装依赖
npm ci

# 构建
npm run build

Set-Location ..

Write-Host "✅ 部署完成!" -ForegroundColor Green
Write-Host "📝 请手动重启 Web 服务器" -ForegroundColor Yellow
