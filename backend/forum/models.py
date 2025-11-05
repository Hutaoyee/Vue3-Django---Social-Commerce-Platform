from django.db import models

from django.db.models.signals import pre_delete
from django.dispatch import receiver

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="标签名")

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="帖子标题")
    content = models.TextField(verbose_name="帖子内容")
    images = models.ManyToManyField('Image', blank=True, related_name='posts', verbose_name="插入图片")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="标签")
    products = models.ManyToManyField('shopping.ProductSPU', blank=True, verbose_name="关联产品")
    author = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='posts', verbose_name="作者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "帖子"
        verbose_name_plural = "帖子"
        indexes = [
            models.Index(fields=['author']),
            models.Index(fields=['created_at']),
        ]

        ordering = ['-created_at']

    def __str__(self):
        return self.title

# 在删除帖子时，删除不再被任何帖子使用的图片文件：
@receiver(pre_delete, sender=Post)
def delete_unused_images(sender, instance, **kwargs):
    images_to_delete = []
    for image in instance.images.all():
        if image.posts.count() == 1:  # 只有当前帖子使用（删除后为 0）
            images_to_delete.append(image)

    for image in images_to_delete:
        image.file.delete(save=False)
        image.delete()


class Image(models.Model):
    file = models.ImageField(upload_to='posts/images/%Y/%m/%d/', verbose_name="图片文件")

    class Meta:
        verbose_name = "插入图片"
        verbose_name_plural = "插入图片"
        indexes = [
            models.Index(fields=['file']),
        ]

    def __str__(self):
        return getattr(self.file, 'name', '')

class Reply(models.Model):
    content = models.TextField(verbose_name="回复内容")
    author = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='replies', verbose_name="作者")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies', verbose_name="所属帖子")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name="父回复")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "回复"
        verbose_name_plural = "回复"
        indexes = [
            models.Index(fields=['author']),
            models.Index(fields=['post']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['created_at']

    def __str__(self):
        return f"Reply {self.id} by {self.author_id} on Post {self.post_id}"