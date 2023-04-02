from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from .models import Author

from .models import Post

from pprint import pprint

LOCAL_HOSTS = ['127.0.0.1:8000', '127.0.0.1:3000', 'localhost:8000', 'localhost:3000', 'https://social-distribution-media.herokuapp.com/']

REMOTE_GET_ALLOWED_VIEWS = ['Authors', 'Author Detail', 'Followers', 'Followers Detail', 'Posts', 'Post Detail', 'Image Posts', 'Comments', 'Post Likes', 'Comment Likes', 'Liked Posts']
REMOTE_POST_ALLOWED_VIEWS = ['Inbox Detail']

class AllowedRemote(permissions.BasePermission):

    def has_permission(self, request, view):
        """Only allow remote users to hit certain endpoints"""
        is_remote_node = Author.objects.get(user__username=request.user).remote
        is_remote_endpoint = request.method == 'GET' and view.get_view_name() in REMOTE_GET_ALLOWED_VIEWS \
            or request.method == 'POST' and view.get_view_name() in REMOTE_POST_ALLOWED_VIEWS
        return not is_remote_node or (is_remote_node and is_remote_endpoint)
    
class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj: Post):
        requestor = Author.objects.filter(displayName=request.user).first()
        # object access is only allowed to owner
        return obj.author == requestor
    
class IsOwnerOrFriend(permissions.BasePermission):
    """
    Custom permission to only allow owners or followers of an object to view it.
    """

    def has_object_permission(self, request, view, obj: Author):
        # object access is allowed to owner or friends
        requestor = Author.objects.filter(displayName=request.user).first()

        # set the is_friend flag so we can use to filter GET requests in the view
        request.is_friend = obj == requestor or obj.followers.filter(pk=requestor._id).exists()

        # return true so we don't block the request
        return True