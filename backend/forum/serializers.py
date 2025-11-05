from rest_framework import serializers
from .models import Tag, Post, Image, Reply

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class ReplySerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = '__all__'

    def get_author(self, obj):
        request = self.context.get('request')
        avatar_url = obj.author.avatar.url if obj.author.avatar else None

        if avatar_url and request:
            avatar_url = request.build_absolute_uri(avatar_url)

        return {
            'id': obj.author.id,
            'name': obj.author.username,
            'avatar': avatar_url
        }

    def get_children(self, obj):
        children = obj.children.all()
        return ReplySerializer(children, many=True, context=self.context).data

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)
    products = serializers.SerializerMethodField()
    images = ImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    replies = ReplySerializer(many=True, read_only=True)

    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Tag.objects.all(), 
        write_only=True, 
        required=False,
        source='tags'
    )

    image_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Image.objects.all(), 
        write_only=True, 
        required=False,
        source='images'
    )

    class Meta:
        model = Post
        fields = '__all__'

    def get_author(self, obj):
        request = self.context.get('request')
        avatar_url = obj.author.avatar.url if obj.author.avatar else None

        if avatar_url and request:
            avatar_url = request.build_absolute_uri(avatar_url)

        return {
            'id': obj.author.id,
            'name': obj.author.username,
            'avatar': avatar_url
        }
    
    def get_products(self, obj):
        
        products = obj.products.all()
        return [{'id': product.id, 'name': product.name} for product in products]