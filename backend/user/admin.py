from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from .models import User, UserProduct, Address, CartItem, ProductFavorite, PostFavorite

# Django 框架中的一个装饰器，用于注册模型（Model）
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """自定义用户管理"""
    
    # 控制列表页显示哪些字段，可以是模型字段或自定义方法
    list_display = [
        'id',
        'username', 
        'email',
        'avatar_preview',  # 自定义方法：显示头像缩略图
        'gender_display',  # 自定义方法：显示性别

        # 未声明的继承字段
        'is_staff', 
        'is_active',
        'date_joined'
    ]
    
    # 右侧过滤器
    list_filter = [
        'gender',
        'is_staff',
        'is_active',
        'date_joined',
    ]
    
    # 顶部搜索框可搜索的字段
    search_fields = ['username', 'email', 'id']
    
    # 排序
    ordering = ['-date_joined']  # 按注册时间倒序
    
    # 每页显示数量
    list_per_page = 20
    
    # 列表页可直接编辑的字段
    list_editable = ['is_active']
    
    # 点击跳转到详情页的字段
    list_display_links = ['id', 'username']
    
    # 详情页字段分组
    fieldsets = BaseUserAdmin.fieldsets + (
        ('个人信息', {
            'fields': ('avatar', 'gender', 'bio')
        }),
    )
    
    # 添加用户页面的字段
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('个人信息', {
            'fields': ('avatar', 'gender', 'bio')
        }),
    )
    
    # 只读字段
    readonly_fields = ['date_joined', 'last_login', 'avatar_preview']
    
    # 自定义方法：显示头像缩略图
    def avatar_preview(self, obj):
        """显示头像缩略图"""
        if obj.avatar:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%;" />',
                obj.avatar.url
            )
        return '-'
    avatar_preview.short_description = '头像预览'
    
    # 自定义方法：显示性别
    def gender_display(self, obj):
        """显示性别（带颜色）"""
        gender_map = {
            'M': ('男', 'blue'),
            'F': ('女', 'pink'),
            'O': ('其他', 'gray')
        }
        if obj.gender in gender_map:
            text, color = gender_map[obj.gender]
            return format_html(
                '<span style="color: {};">{}</span>',
                color, text
            )
        return '-'
    gender_display.short_description = '性别'
    
    # 自定义操作：默认拥有“删除所选的 用户”
    actions = ['activate_users', 'deactivate_users']
    
    def activate_users(self, request, queryset):
        """批量激活用户"""
        count = queryset.update(is_active=True)
        self.message_user(request, f'成功激活 {count} 个用户')
    activate_users.short_description = '激活所选的 用户'
    
    def deactivate_users(self, request, queryset):
        """批量停用用户"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'成功停用 {count} 个用户')
    deactivate_users.short_description = '停用所选的 用户'

@admin.register(UserProduct)
class UserProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'sku', 'purchased_at')
    search_fields = ('user__username', 'sku__title')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone', 'province', 'city', 'district', 'is_default')
    list_filter = ('province', 'city', 'is_default')
    search_fields = ('user__username', 'name', 'phone')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'sku', 'quantity', 'total_price')
    search_fields = ('user__username', 'sku__title')


@admin.register(ProductFavorite)
class ProductFavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    search_fields = ('user__username', 'product__title')


@admin.register(PostFavorite)
class PostFavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'post']
    search_fields = ['user__username', 'post__title']