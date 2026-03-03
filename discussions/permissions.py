from rest_framework import permissions


# Custom permission class
class IsAuthorOrRoleBased(permissions.BasePermission):
    def has_permission(self, request, view):
        # Read-only requests are allowed for everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # All write requests require login
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read-only requests are allowed for everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # If not authenticated, deny (prevents AnonymousUser.role crash)
        if not request.user or not request.user.is_authenticated:
            return False

        # Admin → full access
        if request.user.role == "admin":
            return True

        # Mentor → can update any discussion but not delete
        if request.user.role == "mentor" and request.method in ["PUT", "PATCH"]:
            return True

        # Learner → only their own
        return obj.author == request.user


# Comment permission class
class IsCommentAuthorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "admin":
            return True

        return obj.author == request.user
