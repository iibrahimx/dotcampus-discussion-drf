from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
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

    # add nested comments endpoint
    @action(
        detail=True,
        methods=["get", "post"],
        permission_classes=[permissions.IsAuthenticatedOrReadOnly],
    )
    def comments(self, request, pk=None):
        discussion = self.get_object()

        if request.method == "GET":
            qs = discussion.comments.all().order_by("-created_at")
            serializer = CommentSerializer(qs, many=True)
            return Response(serializer.data)

        # POST
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, discussion=discussion)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [IsCommentAuthorOrAdmin]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
