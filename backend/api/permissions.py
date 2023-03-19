from rest_framework import permissions

from .models import Author

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