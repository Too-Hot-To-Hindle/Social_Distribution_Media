from rest_framework import permissions

from .models import AllowedRemoteNode, AllowedLocalNode

from pprint import pprint

LOCAL_HOSTS = ['127.0.0.1:8000', '127.0.0.1:3000', 'localhost:8000', 'localhost:3000', 'https://social-distribution-media.herokuapp.com/']

REMOTE_GET_ALLOWED_VIEWS = ['Authors', 'Author Detail', 'Followers', 'Followers Detail', 'Posts', 'Post Detail', 'Image Posts', 'Comments', 'Post Likes', 'Comment Likes', 'Liked Posts']
REMOTE_POST_ALLOWED_VIEWS = ['Inbox Detail']

class LocalAndRemote(permissions.BasePermission):
    """
    Permission class allowing remote nodes from certain hosts
    """
    
    def has_permission(self, request, view):
        host = request.META['HTTP_HOST']
        print(host)
        remoteOperationAllowed = request.method == 'GET' and view.get_view_name() in REMOTE_GET_ALLOWED_VIEWS \
            or request.method == 'POST' and view.get_view_name() in REMOTE_POST_ALLOWED_VIEWS
        remoteNodeAllowed = AllowedRemoteNode.objects.filter(host=host).exists()
        localNodeAllowed = AllowedLocalNode.objects.filter(host=host).exists()
        return localNodeAllowed or (remoteOperationAllowed and remoteNodeAllowed)

class Local(permissions.BasePermission):
    """
    Permission class allowing local access only
    """
    
    def has_permission(self, request, view):
        host = request.META['HTTP_HOST']
        allowed = AllowedLocalNode.objects.filter(host=host).exists()
        return allowed