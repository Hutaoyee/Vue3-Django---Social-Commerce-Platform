from django.urls import path, include
from rest_framework.routers import DefaultRouter

# 类视图
from .admin import AttributeValueAutocomplete

# ViewSets
from .views import ProductSPUViewSet, ProductReviewViewSet, CategoryViewSet

# 管理视图
from . import admin_views

# 创建路由器
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'spu', ProductSPUViewSet, basename='spu')
router.register(r'reviews', ProductReviewViewSet, basename='review')

app_name = 'shopping'

urlpatterns = [
    path('', include(router.urls)),
    # 商品属性值根据属性过滤后的视图
    path('attribute-value-autocomplete/', AttributeValueAutocomplete.as_view(), name='attribute-value-autocomplete'),
    
    # ==================== 商品管理页面 ====================
    # SPU管理
    path('manage/', admin_views.product_management, name='product_management'),
    path('manage/spu/create/', admin_views.spu_create, name='spu_create'),
    path('manage/spu/<int:spu_id>/edit/', admin_views.spu_edit, name='spu_edit'),
    path('manage/spu/<int:spu_id>/delete/', admin_views.spu_delete, name='spu_delete'),
    path('manage/image/<int:image_id>/delete/', admin_views.image_delete, name='image_delete'),
    
    # SKU管理
    path('manage/spu/<int:spu_id>/skus/', admin_views.sku_management, name='sku_management'),
    path('manage/spu/<int:spu_id>/sku/create/', admin_views.sku_create, name='sku_create'),
    path('manage/sku/<str:sku_code>/edit/', admin_views.sku_edit, name='sku_edit'),
    path('manage/sku/<str:sku_code>/delete/', admin_views.sku_delete, name='sku_delete'),
    
    # 属性管理
    path('manage/attributes/', admin_views.attribute_management, name='attribute_management'),
    path('manage/attribute/create/', admin_views.attribute_create, name='attribute_create'),
    path('manage/attribute/<int:attr_id>/delete/', admin_views.attribute_delete, name='attribute_delete'),
    path('manage/attribute/<int:attr_id>/value/create/', admin_views.attribute_value_create, name='attribute_value_create'),
    path('manage/attribute/value/<int:value_id>/delete/', admin_views.attribute_value_delete, name='attribute_value_delete'),
    
    # SPU属性关联
    path('manage/spu/<int:spu_id>/attributes/', admin_views.spu_attribute_management, name='spu_attribute_management'),
    
    # 分类管理
    path('manage/categories/', admin_views.category_management, name='category_management'),
    path('manage/category/create/', admin_views.category_create, name='category_create'),
    path('manage/category/<int:category_id>/edit/', admin_views.category_edit, name='category_edit'),
    path('manage/category/<int:category_id>/delete/', admin_views.category_delete, name='category_delete'),
]