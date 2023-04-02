from functools import wraps
from .models import Author
# from rest_framework.response import Response
# from rest_framework import status

def friend_check(view_func):

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # author = Author.objects.filter(user=request.user).first()
        print(f"MIDDLEWARE AUTHOR: {request.user}")
        # if author:
        #     request.is_friend = author.is_friend
        # else:
        #     request.is_friend = None
        return view_func(request, *args, **kwargs)

    return _wrapped_view