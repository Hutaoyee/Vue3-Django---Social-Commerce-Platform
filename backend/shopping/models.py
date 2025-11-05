from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# 动态图片上传路径函数
def product_image_upload_path(instance, filename):
    """
    动态生成图片上传路径，基于SPU的品牌和系列。
    """
    if instance.spu:
        brand = (instance.spu.brand or 'no_brand').replace(' ', '_')  # 替换空格为下划线
        series = (instance.spu.series or 'no_series').replace(' ', '_')
        return f'products/{brand}/{series}/{filename}'
    else:
        return f'products/other/{filename}'  # 默认路径

# Create your models here.
# 商品分类表
class Category(MPTTModel):
    name = models.CharField(max_length=100, verbose_name="分类名称")
    parent = TreeForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, verbose_name="父级分类"
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类"
        indexes = [
            models.Index(fields=['parent']),  # 优化树查询
        ]

    def __str__(self):
        return self.name

# SPU表
class ProductSPU(models.Model):
    name = models.CharField(max_length=200, verbose_name="商品名称")
    description = models.TextField(blank=True, verbose_name="商品描述")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="所属分类")
    brand = models.CharField(max_length=100, blank=True, verbose_name="品牌")  
    series = models.CharField(max_length=100, blank=True, verbose_name="系列")  
    is_active = models.BooleanField(default=True, verbose_name="是否上架")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "SPU"
        verbose_name_plural = "SPU"
        indexes = [
            models.Index(fields=['category', 'is_active']),  # 优化按分类和状态查询
            models.Index(fields=['brand']),  
            models.Index(fields=['series']),  
        ]

    def __str__(self):
        return self.name

# SKU表
class ProductSKU(models.Model):

    sku_code = models.CharField(max_length=100, primary_key=True, editable=False,verbose_name="SKU编码")
    spu = models.ForeignKey(ProductSPU, on_delete=models.CASCADE, related_name='skus', verbose_name="所属SPU")
    title = models.CharField(max_length=200, verbose_name="SKU标题")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")

    is_active = models.BooleanField(default=True, verbose_name="是否上架")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "SKU"
        verbose_name_plural = "SKU"
        indexes = [
            models.Index(fields=['spu', 'is_active']),  # 优化按SPU和状态查询SKU
            models.Index(fields=['price']),  # 优化价格排序
        ]

    def save(self, *args, **kwargs):
        if not self.sku_code:
            # 获取当前 SPU 下已存在的 SKU 数量
            count = ProductSKU.objects.filter(spu=self.spu).count() + 1
            self.sku_code = f"{self.spu.id}-{count}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
# SKU属性表： 总共有哪些属性
class Attribute(models.Model):
    name = models.CharField(max_length=100, verbose_name="属性名称")

    class Meta:
        verbose_name = "属性"
        verbose_name_plural = "属性"

    def __str__(self):
        return self.name

# SKU属性值表： 每个属性有哪些值
class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='values', verbose_name="所属属性")
    value = models.CharField(max_length=100, verbose_name="属性值")

    class Meta:
        verbose_name = "属性值"
        verbose_name_plural = "属性值"
        unique_together = ('attribute', 'value')

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"

# 属性所有表：一个SPU有哪些属性
class ProductSPUAttribute(models.Model):
    spu = models.ForeignKey(ProductSPU, on_delete=models.CASCADE, related_name='attributes', verbose_name="所属SPU")
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, verbose_name="属性")

    class Meta:
        verbose_name = "SPU属性"
        verbose_name_plural = "SPU属性"
        # 确保同一个 SPU（商品）不能重复关联同一个属性。
        unique_together = ('spu', 'attribute')
        indexes = [
            models.Index(fields=['spu']),  # 优化反查SPU属性
        ]

    def __str__(self):
        return f"{self.spu.name} - {self.attribute.name}"
    
# 属性值所有表：一个SKU有哪些属性值
class ProductSKUAttributeValue(models.Model):
    sku = models.ForeignKey(ProductSKU, on_delete=models.CASCADE, related_name='attribute_values', verbose_name="所属SKU")
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, verbose_name="属性")  
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE, verbose_name="属性值")

    class Meta:
        verbose_name = "SKU属性值"
        verbose_name_plural = "SKU属性值"
        unique_together = ('sku', 'attribute')  # 修改为确保每个SKU对每个属性只有一个值
        indexes = [
            models.Index(fields=['sku']),  # 优化反查SKU属性值
            models.Index(fields=['attribute']),  # 优化按属性查询
        ]

    def __str__(self):
        return f"{self.sku.title} - {self.attribute_value}"

    def save(self, *args, **kwargs):
        # 确保attribute_value属于指定的attribute
        if self.attribute_value.attribute != self.attribute:
            raise ValueError("属性值必须属于指定的属性")
        
        # 确保attribute在SPU的属性中
        if not ProductSPUAttribute.objects.filter(spu=self.sku.spu, attribute=self.attribute).exists():
            raise ValueError("SKU 的属性必须在所属 SPU 的属性列表中")
        super().save(*args, **kwargs)

# 库存表
class Inventory(models.Model):
    sku = models.OneToOneField(ProductSKU, on_delete=models.CASCADE, related_name='inventory', verbose_name="SKU")
    quantity = models.PositiveIntegerField(default=0, verbose_name="库存数量")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "库存"
        verbose_name_plural = "库存"
        indexes = [
            models.Index(fields=['quantity']),  # 优化库存查询
        ]

    def __str__(self):
        return f"{self.sku.title} - {self.quantity}"

# 商品图片表
class ProductImage(models.Model):
    spu = models.ForeignKey(ProductSPU, on_delete=models.CASCADE, related_name='images', verbose_name="SPU", null=True, blank=True)
    sku = models.ForeignKey(ProductSKU, on_delete=models.CASCADE, related_name='images', verbose_name="SKU", null=True, blank=True)
    image = models.ImageField(upload_to=product_image_upload_path, verbose_name="图片")
    is_main = models.BooleanField(default=False, verbose_name="是否主图")

    class Meta:
        verbose_name = "商品图片"
        verbose_name_plural = "商品图片"
        indexes = [
            models.Index(fields=['spu', 'is_main']),  # 优化SPU主图查询
            models.Index(fields=['sku', 'is_main']),  # 优化SKU主图查询
        ]

    def __str__(self):
        return f"{self.spu.name if self.spu else self.sku.title} - {self.image.name}"

# 商品评论表
class ProductReview(models.Model):
    spu = models.ForeignKey(ProductSPU, on_delete=models.CASCADE, related_name='reviews', verbose_name="所属SPU")
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='product_reviews', verbose_name="评论用户")
    content = models.TextField(verbose_name="评论内容")
    rating = models.PositiveSmallIntegerField(default=5, verbose_name="评分")  # 1-5星
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "商品评论"
        verbose_name_plural = "商品评论"
        indexes = [
            models.Index(fields=['spu', 'created_at']),
            models.Index(fields=['user']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} 评论 {self.spu.name}"