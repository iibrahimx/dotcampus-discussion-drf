from rest_framework.routers import DefaultRouter
from .views import DiscussionViewSet, CommentViewSet

router = DefaultRouter()
router.register(r"discussions", DiscussionViewSet, basename="discussion")

router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = router.urls
