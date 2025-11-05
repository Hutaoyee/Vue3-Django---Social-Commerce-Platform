# Social Commerce Platform

一个基于 Vue 3 + Django REST Framework 的社交电商平台。

## 功能特性

- 🛍️ 商品管理（分类、属性、SKU）
- 💬 社区论坛（帖子、回复、点赞）
- 🎵 内容发布（音乐、视频）
- 👤 用户系统（注册、登录、JWT 认证）
- 🛒 购物功能

## 技术栈

### 后端
- Django 5.2.7
- Django REST Framework
- MySQL
- JWT 认证
- Django MPTT（树形分类）

### 前端
- Vue 3
- Vue Router
- Pinia
- Axios
- Vite

## 项目结构

```
├── backend/           # Django 后端
│   ├── backend/      # 项目配置
│   ├── user/         # 用户模块
│   ├── shopping/     # 购物模块
│   ├── forum/        # 论坛模块
│   ├── publish/      # 发布模块
│   └── media/        # 媒体文件
├── frontend/         # Vue 前端
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── router/
│   │   └── stores/
│   └── public/
└── docs/            # 文档
```

## 快速开始

### 环境要求

- Python 3.11+
- Node.js 20.19.0+ 或 22.12.0+
- MySQL 8.0+

### 后端设置

1. 创建虚拟环境并安装依赖：

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

2. 配置环境变量：

复制 `.env.example` 为 `.env` 并填写配置信息。

3. 数据库迁移：

```bash
python manage.py makemigrations
python manage.py migrate
```

4. 创建超级用户：

```bash
python manage.py createsuperuser
```

5. 运行开发服务器：

```bash
python manage.py runserver
```

后端服务运行在：http://localhost:8000

### 前端设置

1. 安装依赖：

```bash
cd frontend
npm install
```

2. 运行开发服务器：

```bash
npm run dev
```

前端服务运行在：http://localhost:5173

3. 构建生产版本：

```bash
npm run build
```

## API 文档

详细 API 文档请查看：
- [API 测试指南](API_TESTING_GUIDE.md)
- [商品管理指南](PRODUCT_MANAGEMENT_GUIDE.md)
- [分类管理指南](CATEGORY_MANAGEMENT_GUIDE.md)

## 开发指南

### 代码规范

前端使用 ESLint 和 Prettier：

```bash
npm run lint    # 检查代码
npm run format  # 格式化代码
```

### 测试

```bash
# 单元测试
npm run test:unit

# E2E 测试
npm run test:e2e
```

## 部署

### 生产环境配置

1. 设置环境变量（`.env` 文件）
2. 收集静态文件：`python manage.py collectstatic`
3. 使用 Gunicorn 运行 Django
4. 配置 Nginx 反向代理
5. 前端构建并部署到静态文件服务器

详细部署步骤请参考 [部署文档](DEPLOYMENT.md)

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 联系方式

如有问题，请提交 Issue。
