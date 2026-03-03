from rest_framework import serializers
from .models import Discussion, Comment


class DiscussionSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Discussion
        fields = [
            "id",
            "author",
            "title",
            "content",
            "created_at",
            "updated_at",
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "discussion",
            "content",
            "created_at",
        ]
