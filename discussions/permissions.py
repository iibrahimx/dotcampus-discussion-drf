from rest_framework import permissions


# Custom permission class
class IsAuthorOrRoleBased(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        # SAFE METHODS (GET, HEAD, OPTIONS) are allowed for everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # If user is admin → full access
        if request.user.role == "admin":
            return True

        # If user is mentor → can update any discussion
        if request.user.role == "mentor":
            if request.method in ["PUT", "PATCH"]:
                return True

        # Learner can only modify their own discussions
        return obj.author == request.user


# Comment permission class
class IsCommentAuthorOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        # Admin can delete any comment
        if request.user.role == "admin":
            return True

        # Otherwise only author can modify
        return obj.author == request.user
