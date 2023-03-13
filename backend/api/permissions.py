from rest_framework import permissions

from .models import AllowedNode

LOCAL_IPS = []
LOCAL_URLS = []
REMOTE_GET_ALLOWED_VIEWS = ['Authors', 'AuthorDetail', 'Followers', 'FollowersDetail', 'Post', 'PostDetail', 'ImagePosts', 'Comments', 'PostLikes', 'CommentLikes', 'LikedPosts']
REMOTE_POST_ALLOWED_VIEWS = ['InboxDetail']

class LocalAndRemote(permissions.BasePermission):
    """
    Permission class allowing remote nodes from certain IPs
    """
    
    def has_permission(self, request, view):
        ip = request.META['REMOTE_ADDR']
        host = request.META['REMOTE_HOST']
        print(ip, host, request, view)
        print(view.get_view_name())
        print(request.method)
        operationAllowed = request.method == 'GET' and view.get_view_name() in REMOTE_GET_ALLOWED_VIEWS \
            or request.method == 'POST' and view.get_view_name() in REMOTE_POST_ALLOWED_VIEWS
        nodeAllowed = (AllowedNode.objects.filter(ip=ip) | AllowedNode.objects.filter(host=host)).exists()
        return operationAllowed and nodeAllowed

class Local(permissions.BasePermission):
    """
    Permission class allowing remote nodes from certain IPs
    """
    
    def has_permission(self, request, view):
        ip = request.META['REMOTE_ADDR']
        host = request.META['REMOTE_HOST']
        allowed = True  # TODO: Update this to check for local IPs/URLs
        return allowed