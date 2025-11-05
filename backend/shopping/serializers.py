from rest_framework import serializers
from .models import ProductSPU, ProductSKU, ProductReview, Category

class CategorySerializer(serializers.ModelSerializer):
    """分类序列化器，支持层级显示"""
    level = serializers.IntegerField(read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'level', 'full_name']
    
    def get_full_name(self, obj):
        """获取完整的分类路径，如：服装 > 上衣 > T恤"""
        names = [obj.name]
        parent = obj.parent
        while parent:
            names.insert(0, parent.name)
            parent = parent.parent
        return ' > '.join(names)


class ProductSPUSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()  # 从ProductImage获取主图
    is_favorited = serializers.SerializerMethodField()  # 是否已收藏
    review_count = serializers.SerializerMethodField()  # 评论数
    average_rating = serializers.SerializerMethodField()  # 平均评分

    class Meta:
        model = ProductSPU
        fields = ['id', 'name', 'description', 'category', 'brand', 'series', 'is_active', 
                  'created_at', 'updated_at', 'image', 'is_favorited', 'review_count', 'average_rating']

    def get_image(self, obj):
        """返回主图完整 URL"""
        request = self.context.get('request')
        image = obj.images.filter(is_main=True).first()
        if image:
            if request:
                return request.build_absolute_uri(image.image.url)
            return image.image.url
        return None
    
    def get_is_favorited(self, obj):
        """检查当前用户是否已收藏"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from user.models import ProductFavorite
            return ProductFavorite.objects.filter(user=request.user, product=obj).exists()
        return False
    
    def get_review_count(self, obj):
        """获取评论数量"""
        return obj.reviews.count()
    
    def get_average_rating(self, obj):
        """获取平均评分"""
        reviews = obj.reviews.all()
        if reviews:
            total = sum(review.rating for review in reviews)
            return round(total / len(reviews), 1)
        return 0


class ProductSKUSerializer(serializers.ModelSerializer):
    spu_name = serializers.CharField(source='spu.name', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductSKU
        fields = ['sku_code', 'spu', 'spu_name', 'title', 'price', 'is_active', 'image']

    def get_image(self, obj):
        """返回SKU主图完整 URL"""
        request = self.context.get('request')
        image = obj.spu.images.filter(is_main=True).first()
        if image:
            if request:
                return request.build_absolute_uri(image.image.url)
            return image.image.url
        return None


class SKUDetailSerializer(serializers.ModelSerializer):
    """SKU详细信息序列化器，包含库存"""
    stock = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductSKU
        fields = ['sku_code', 'title', 'price', 'stock', 'is_active']
    
    def get_stock(self, obj):
        """获取库存数量"""
        inventory = getattr(obj, 'inventory', None)
        return inventory.quantity if inventory else 0


class ProductReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_avatar = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductReview
        fields = ['id', 'spu', 'user', 'username', 'user_avatar', 'content', 'rating', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def get_user_avatar(self, obj):
        """获取用户头像URL"""
        request = self.context.get('request')
        if obj.user.avatar:
            if request:
                return request.build_absolute_uri(obj.user.avatar.url)
            return obj.user.avatar.url
        return None