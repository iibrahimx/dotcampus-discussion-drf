from rest_framework.routers import DefaultRouter
from .views import DiscussionViewSet

router = DefaultRouter()
router.register(r"discussions", DiscussionViewSet, basename="discussion")

urlpatterns = router.urls
