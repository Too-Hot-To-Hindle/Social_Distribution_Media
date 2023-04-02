from .models import Author
from .models import Follow

class FriendCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # author = Author.objects.filter(user=request.user).first()
        print(f"MIDDLEWARE AUTHOR: {request.user}")
        # if author:
        #     request.is_friend = author.is_friend
        # else:
        #     request.is_friend = None
        response = self.get_response(request)
        return response