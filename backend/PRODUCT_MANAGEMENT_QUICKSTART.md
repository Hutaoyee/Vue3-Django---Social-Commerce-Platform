# 商品管理系统快速启动指南

## 1. 确保环境准备就绪

### 检查虚拟环境
```bash
# 在 backend 目录下
pipenv shell
```

### 确保所有依赖已安装
```bash
pipenv install
```

## 2. 创建管理员账户（如果还没有）

```bash
# 在 backend 目录下
python manage.py createsuperuser
```

或者将现有用户设置为管理员：

```bash
python manage.py shell
```

然后在Python shell中执行：
```python
from user.models import User
user = User.objects.get(username='你的用户名')
user.is_staff = True
user.is_superuser = True
user.save()
print(f"用户 {user.username} 已设置为管理员")
exit()
```

## 3. 运行数据库迁移（如果还没有）

```bash
python manage.py migrate
```

## 4. 初始化示例数据（可选）

```bash
python init_product_data.py
```

这会创建：
- 2个分类（服装、鞋类）
- 3个属性（颜色、尺码、鞋码）
- 2个SPU及其SKU示例

## 5. 启动Django开发服务器

```bash
python manage.py runserver
```

## 6. 访问商品管理系统

打开浏览器访问：
```
http://localhost:8000/api/shopping/manage/
```

## 访问路径说明

- **商品列表**: http://localhost:8000/api/shopping/manage/
- **新建商品**: http://localhost:8000/api/shopping/manage/spu/create/
- **属性管理**: http://localhost:8000/api/shopping/manage/attributes/
- **SKU管理**: http://localhost:8000/api/shopping/manage/spu/{spu_id}/skus/

## 常用命令

### 创建测试用户
```bash
python create_test_users.py
```

### 查看所有管理员
```bash
python manage.py shell -c "from user.models import User; admins = User.objects.filter(is_staff=True); print('\n'.join([f'{u.username} - {u.email}' for u in admins]))"
```

### 清空商品数据（谨慎使用）
```bash
python manage.py shell -c "from shopping.models import *; ProductSKU.objects.all().delete(); ProductSPU.objects.all().delete(); print('商品数据已清空')"
```

## 功能测试流程

1. ✅ 登录管理员账户
2. ✅ 创建属性（颜色、尺码等）
3. ✅ 为属性添加属性值
4. ✅ 创建SPU（上传图片、填写信息）
5. ✅ 为SPU设置属性
6. ✅ 创建SKU（选择属性值、设置价格库存）
7. ✅ 测试编辑、删除功能
8. ✅ 测试搜索和过滤功能

## 故障排除

### 问题：403 Forbidden / 重定向到登录页
**解决**: 确保当前登录用户的 `is_staff=True`

### 问题：找不到模板文件
**解决**: 检查 `shopping/templates/shopping/` 目录是否存在

### 问题：上传图片失败
**解决**: 
1. 检查 `media/products/` 目录是否有写入权限
2. 检查 `settings.py` 中的 `MEDIA_ROOT` 和 `MEDIA_URL` 配置

### 问题：创建SKU时没有属性可选
**解决**: 
1. 先到"属性管理"创建属性和属性值
2. 然后到"设置商品属性"为SPU选择属性

## 下一步

- 查看前端商品展示页面：`http://localhost:5173/merch`
- 测试购物车功能
- 测试商品评论功能
