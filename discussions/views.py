from rest_framework import viewsets, permissions
from .models import Discussion
from .serializers import DiscussionSerializer


# Create your views here.
class DiscussionViewSet(viewsets.ModelViewSet):
    queryset = Discussion.objects.all().order_by("-created_at")
    serializer_class = DiscussionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
