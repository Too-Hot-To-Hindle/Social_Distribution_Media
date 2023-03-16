from rest_framework import permissions

from .models import AllowedNode

from pprint import pprint

REMOTE_GET_ALLOWED_VIEWS = ['Authors', 'Author Detail', 'Followers', 'Followers Detail', 'Post', 'Post Detail', 'Image Posts', 'Comments', 'Post Likes', 'Comment Likes', 'Liked Posts']
REMOTE_POST_ALLOWED_VIEWS = ['Inbox Detail']

class LocalAndRemote(permissions.BasePermission):
    """
    Permission class allowing remote nodes from certain hosts
    """
    
    def has_permission(self, request, view):
        host = request.META['HTTP_HOST']
        operationAllowed = request.method == 'GET' and view.get_view_name() in REMOTE_GET_ALLOWED_VIEWS \
            or request.method == 'POST' and view.get_view_name() in REMOTE_POST_ALLOWED_VIEWS
        nodeAllowed = AllowedNode.objects.filter(host=host).exists()
        return operationAllowed and nodeAllowed

class Local(permissions.BasePermission):
    """
    Permission class allowing remote nodes from certain hosts
    """
    
    def has_permission(self, request, view):
        ip = request.META['REMOTE_ADDR']
        host = request.META['REMOTE_HOST']
        allowed = True  # TODO: Update this to check for local IPs/URLs
        return allowed