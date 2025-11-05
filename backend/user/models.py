from django.conf import settings

from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    
    # 用户ID (继承自 AbstractUser，自动生成主键 id)
    # 用户名 (继承自 AbstractUser 的 username 字段)
    # 邮箱 (继承自 AbstractUser 的 email 字段)
    # 密码 (继承自 AbstractUser 的 password 字段)

    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
        ('O', '其他'),
    ]

    gender = models.CharField(
    max_length=1,
    choices=GENDER_CHOICES,
    blank=True,
    null=True,
    verbose_name='性别'
    )

    avatar = models.ImageField(
        upload_to='avatars/%Y/%m/%d/',
        null=True,
        blank=True,
        # 路径相对于 MEDIA_ROOT 设置
        default='avatars/default.png',
        verbose_name='头像'
    )

    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='个人简介'
    )


    # 重写继承字段，避免与 auth.User 冲突（user_set）
    groups = models.ManyToManyField(
            'auth.Group',
            verbose_name='groups',
            blank=True,
            help_text='The groups this user belongs to.',
            related_name='custom_user_set',  # 避免与 auth.User.groups 冲突
            related_query_name='custom_user',
        )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',  # 避免与 auth.User.user_permissions 冲突
        related_query_name='custom_user',
    )


    class Meta:
        db_table = 'users'  # 自定义数据库表名
        verbose_name = '用户' # Admin 显示名称
        verbose_name_plural = verbose_name  # 复数显示名称
        ordering = ['-date_joined']  # 自动按时间倒序

    def __str__(self):
        return self.username
    
    # 获取头像完整 URL
    def get_avatar_url(self):
        """获取头像 URL"""
        if self.avatar:
            return self.avatar.url
        return f"{settings.MEDIA_URL}avatars/default.png"

class UserProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_products', verbose_name='用户')
    sku = models.ForeignKey('shopping.ProductSKU', on_delete=models.CASCADE, verbose_name='SKU')
    purchased_at = models.DateTimeField(auto_now_add=True, verbose_name='购买时间')

    class Meta:
        verbose_name = '用户拥有商品'
        verbose_name_plural = '用户拥有商品'
        unique_together = ('user', 'sku')  # 同一用户同一SKU合并数量

    def __str__(self):
        return f"{self.user.username} - {self.sku.title}"

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    name = models.CharField(max_length=100, verbose_name='收货人姓名')
    phone = models.CharField(max_length=20, verbose_name='联系电话')
    province = models.CharField(max_length=50, verbose_name='省份')
    city = models.CharField(max_length=50, verbose_name='城市')
    district = models.CharField(max_length=50, verbose_name='区县')
    address = models.CharField(max_length=200, verbose_name='详细地址')
    is_default = models.BooleanField(default=False, verbose_name='是否默认地址')

    class Meta:
        verbose_name = '地址'
        verbose_name_plural = '地址'
        ordering = ['-is_default', '-id']  # 默认地址优先

    def __str__(self):
        return f"{self.name} - {self.province}{self.city}{self.district}{self.address}"

    def save(self, *args, **kwargs):
        # 确保只有一个默认地址
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items', verbose_name='用户')
    sku = models.ForeignKey('shopping.ProductSKU', on_delete=models.CASCADE, verbose_name='SKU')  # 跨app关联
    quantity = models.PositiveIntegerField(default=1, verbose_name='数量')

    class Meta:
        verbose_name = '购物车项'
        verbose_name_plural = '购物车项'
        unique_together = ('user', 'sku')  # 同一用户同一SKU只能有一条

    def __str__(self):
        return f"{self.user.username} - {self.sku.title} x {self.quantity}"

    # 总金额
    @property
    def total_price(self):
        return self.sku.price * self.quantity

class ProductFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_favorites', verbose_name='用户')
    product = models.ForeignKey('shopping.ProductSPU', on_delete=models.CASCADE, verbose_name='商品SPU')  # 改为SPU
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间', null=True)

    class Meta:
        verbose_name = '商品收藏'
        verbose_name_plural = '商品收藏'
        unique_together = ('user', 'product')  # 防止同一用户重复收藏同一商品
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} 收藏了 {self.product.name}"

class PostFavorite(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='post_favorites', verbose_name="用户")
    post = models.ForeignKey('forum.Post', on_delete=models.CASCADE, verbose_name="收藏的帖子")

    class Meta:
        verbose_name = "帖子收藏"
        verbose_name_plural = "帖子收藏"
        unique_together = ('user', 'post')  # 防止重复收藏

    def __str__(self):
        return f"{self.user} 收藏了 {self.post}"