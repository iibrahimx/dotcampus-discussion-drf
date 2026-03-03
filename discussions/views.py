from rest_framework import viewsets, permissions
from .models import Discussion, Comment
from .permissions import IsAuthorOrRoleBased, IsCommentAuthorOrAdmin
from .serializers import DiscussionSerializer, CommentSerializer


# Create your views here.


class DiscussionViewSet(viewsets.ModelViewSet):
    queryset = Discussion.objects.all().order_by("-created_at")
    serializer_class = DiscussionSerializer
    permission_classes = [IsAuthorOrRoleBased]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [IsCommentAuthorOrAdmin]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
