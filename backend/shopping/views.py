from django.shortcuts import render, get_object_or_404

from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from .models import ProductSPU, ProductSKU, Attribute, AttributeValue, ProductSKUAttributeValue, ProductSPUAttribute, ProductReview, Category
from .serializers import ProductSPUSerializer, ProductSKUSerializer, ProductReviewSerializer, SKUDetailSerializer, CategorySerializer
from .pagination import ProductPagination

# Create your views here.

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    分类视图集，只读
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    pagination_class = None  # 禁用分页，返回所有分类
    
    def get_queryset(self):
        """返回所有分类，按树形结构排序"""
        return Category.objects.all().order_by('tree_id', 'lft')


class ProductSPUViewSet(viewsets.ModelViewSet):
    """
    SPU视图集，支持分页、搜索、过滤
    """
    queryset = ProductSPU.objects.filter(is_active=True)
    serializer_class = ProductSPUSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = ProductPagination
    
    def get_queryset(self):
        queryset = ProductSPU.objects.filter(is_active=True)
        
        # 按分类过滤（包含子分类）
        category_id = self.request.query_params.get('category')
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                # 获取该分类及其所有子分类
                categories = category.get_descendants(include_self=True)
                queryset = queryset.filter(category__in=categories)
            except Category.DoesNotExist:
                pass
        
        # 按品牌过滤
        brand = self.request.query_params.get('brand')
        if brand:
            queryset = queryset.filter(brand__icontains=brand)
        
        # 搜索
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        return queryset
    
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def skus(self, request, pk=None):
        """
        获取SPU的所有SKU信息，包括属性、库存、价格
        """
        spu = self.get_object()
        
        # 获取SPU的所有属性
        spu_attributes = ProductSPUAttribute.objects.filter(spu=spu).select_related('attribute')
        
        # 构建属性和属性值的数据结构
        attributes_data = []
        for spu_attr in spu_attributes:
            attribute = spu_attr.attribute
            # 获取该SPU下所有SKU使用的属性值
            attribute_values = AttributeValue.objects.filter(
                productskuattributevalue__sku__spu=spu,
                attribute=attribute
            ).distinct()
            
            attributes_data.append({
                'id': attribute.id,
                'name': attribute.name,
                'values': [{'id': av.id, 'value': av.value} for av in attribute_values]
            })
        
        # 获取所有SKU及其属性值
        skus = ProductSKU.objects.filter(spu=spu, is_active=True).prefetch_related(
            'attribute_values__attribute',
            'attribute_values__attribute_value',
            'inventory',
            'images'  # 预加载SKU图片
        )
        
        # 获取SPU主图
        spu_main_image = spu.images.filter(is_main=True).first()
        spu_image_url = request.build_absolute_uri(spu_main_image.image.url) if spu_main_image else None
        
        skus_data = []
        for sku in skus:
            sku_attrs = {}
            for sku_attr_value in sku.attribute_values.all():
                sku_attrs[sku_attr_value.attribute.id] = sku_attr_value.attribute_value.id
            
            # 获取SKU图片，如果没有则使用SPU主图
            sku_image = sku.images.first()
            image_url = request.build_absolute_uri(sku_image.image.url) if sku_image else spu_image_url
            
            inventory = getattr(sku, 'inventory', None)
            skus_data.append({
                'sku_code': sku.sku_code,
                'title': sku.title,
                'price': str(sku.price),
                'stock': inventory.quantity if inventory else 0,
                'attributes': sku_attrs,
                'image': image_url  # 添加图片URL
            })
        
        return Response({
            'attributes': attributes_data,
            'skus': skus_data
        })
    
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def reviews(self, request, pk=None):
        """
        获取SPU的所有评论
        """
        spu = self.get_object()
        reviews = ProductReview.objects.filter(spu=spu).order_by('-created_at')
        serializer = ProductReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data)


class ProductReviewViewSet(viewsets.ModelViewSet):
    """
    商品评论视图集
    """
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = ProductReview.objects.all()
        
        # 按SPU过滤
        spu_id = self.request.query_params.get('spu')
        if spu_id:
            queryset = queryset.filter(spu_id=spu_id)
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)