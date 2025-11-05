from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tags', views.TagViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'images', views.ImageViewSet)
router.register(r'replies', views.ReplyViewSet)

urlpatterns = router.urls