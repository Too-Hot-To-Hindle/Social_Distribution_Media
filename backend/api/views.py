from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.http import JsonResponse
# from django.contrib.auth import authenticate, login

from .serializers import UserSerializer, AuthorSerializer, PostSerializer
from .models import Author, Post

import traceback
import uuid

class Authors(APIView):

    def get(self, request, format=None):
        """
        Get all authors

        TODO: Query params, paging

        See below for adding new fields (not in model) to response:

        https://stackoverflow.com/questions/37943339/django-rest-framework-how-to-add-a-custom-field-to-the-response-of-the-get-req
        """
        try:
            authors = Author.objects.all()
            serializer = AuthorSerializer(authors, many=True)  # Must include many=True because it is a list of authors
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """
        register a new user
        """
        try:
            # create our user and an author, and link it with the author.
            serializer = UserSerializer(data=request.POST.dict())
            print(request.POST.dict())
            if serializer.is_valid():
                user = serializer.data
                user = User.objects.create_user(user['username'], password=user['password'])
                # TODO: Need to figure out if we want display name to be unique, or have another unique identifier from the registration page
                # to use for creating authors...
                Author.objects.create(user=user, displayName=user.username)
                return Response(user.username, status=status.HTTP_201_CREATED)
            else:
                print(serializer.error_messages)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AuthorDetail(APIView):

    def get(self, request, author_id):
        """
        Get details for an author
        """
        try:
            author = Author.objects.get(pk=author_id)
            serializer = AuthorSerializer(author)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, author_id):
        """
        Update details for an author
        TODO: This must only be useable as a 'local' user
        """
        try:
            serializer = AuthorSerializer(data=request.POST.dict())
            if serializer.is_valid():
                updated = Author.objects.filter(pk=author_id).update(**serializer.data)
                if updated > 0:
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response('author_id does not exist', status=status.HTTP_404_NOT_FOUND)
            else:
                print(serializer.error_messages)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class Followers(APIView):

    def get(self, request, author_id):
        """
        Get a list of authors following the user given by author_id

        TODO: Paging? Query params?

        See below for adding new fields (not in model) to response:

        https://stackoverflow.com/questions/37943339/django-rest-framework-how-to-add-a-custom-field-to-the-response-of-the-get-req
        """
        try:
            author = Author.objects.get(pk=author_id)
            serializer = AuthorSerializer(author.followers, many=True)
            return Response(serializer.data)
        except Author.DoesNotExist:
            return Response(f'The author {author_id} does not exist.', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            traceback.print_exc()
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class FollowersDetail(APIView):

    def get(self, request, author_id, foreign_author_id):
        """Check if foreign_author_id is a follower of author_id"""
        try:
            author = Author.objects.get(pk=author_id)
            response = {'isFollower': author.followers.filter(pk=foreign_author_id).exists()}
            return Response(response, status=status.HTTP_200_OK)
        except ValidationError as e:
            print(e)
            return Response('author_id or foreign_author_id is not a valid uuid')
        except Exception as e:
            print(e)
            print(traceback.print_exc())
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, author_id, foreign_author_id):
        """
        Remove foreign_author_id as a follower of author_id
        
        NOTE: Might be a better way to do this
        """
        try:
            author = Author.objects.get(pk=author_id)
            follower = Author.objects.get(id=foreign_author_id)
            author.followers.remove(follower)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Author.DoesNotExist:
            return Response(f'The author {author_id} or {foreign_author_id} does not exist.', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, author_id, foreign_author_id):
        """Add foreign_author_id as a follower of author_id"""
        try:
            serializer = AuthorSerializer(data=request.POST.dict())
            if serializer.is_valid():
                author = Author.objects.get(pk=author_id)
                author.followers.add(**serializer.data)
            else:
                print(serializer.error_messages)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Posts(APIView):

    def get(self, request, author_id):
        """
        Get paginated list of posts by author_id, ordered by post date with most recent first
        
        TODO: Query params, paging

        See below for adding new fields (not in model) to response:

        https://stackoverflow.com/questions/37943339/django-rest-framework-how-to-add-a-custom-field-to-the-response-of-the-get-req
        """
        try:
            posts = Post.objects.filter(author___id=author_id).all()
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, author_id):
        """Create a post (post object in body) for author_id, but generate the ID (compare to PUT in PostDetail)"""
        try:
            serializer = PostSerializer(data=request.POST.dict())
            if serializer.is_valid():
                post = Post.objects.create(**serializer.data, author_id=author_id)
                serializer = PostSerializer(post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Author.DoesNotExist:
            return Response(f'The author {author_id} does not exist.', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

class PostDetail(APIView):

    def get(self, request, author_id, post_id):
        """Get post_id posted by author_id"""
        try:
            post = Post.objects.get(pk=post_id)  # NOTE: Should we do anything with author_id?
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, author_id, post_id):
        """Update post_id posted by author_id (post object in body)"""
        try:
            serializer = PostSerializer(data=request.POST.dict())
            if serializer.is_valid():
                updated = Post.objects.filter(pk=post_id, author___id=author_id).update(**serializer.data)
                if updated > 0:
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response('post_id or author_id does not exist', status=status.HTTP_404_NOT_FOUND)
            else:
                print(serializer.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, author_id, post_id):
        """Delete post_id posted by author_id"""
        try:
            deleted = Post.objects.filter(pk=post_id, author___id=author_id).delete()
            if deleted[0] > 0:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, author_id, post_id):
        """Create a post (post object in body) for author_id with id post_id"""
        try:
            serializer = PostSerializer(data=request.POST.dict())
            if serializer.is_valid():
                post = Post.objects.create(**serializer.data, pk=post_id, author_id=author_id)
                serializer = PostSerializer(post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Author.DoesNotExist:
            return Response(f'The author {author_id} does not exist.', status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response(f'post_id {post_id} already exists.', status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ImagePosts(APIView):

    def get(self, author_id, post_id):
        """Get post_id posted by author_id, converted to an image"""
        # NOTE: Should return 404 if post is not an image
        pass

class Comments(APIView):

    def get(self, author_id, post_id):
        """Get all comments on post_id posted by author_id"""
        pass

    def post(self, author_id, post_id):
        """Add a comment (comment object in body) to post_id posted by author_id"""
        pass

class PostLikes(APIView):

    def get(self, request, author_id, post_id):
        """Get a list of likes on post_id posted by author_id"""
        pass

class CommentLikes(APIView):

    def get(self, request_id, author_id, post_id, comment_id):
        """Get a list of likes on comment_id for post_id posted by author_id"""
        pass

class LikedPosts(APIView):

    def get(self, request, author_id):
        """Get list of posts author_id has liked"""
        pass

class Inbox(APIView):

    def get(self, request, author_id):
        """Get list of posts sent to author_id"""
        pass

    def post(self, request, author_id):
        """Send a post to author_id"""
        # NOTE: 4 different cases based on type field in post request body
        # See https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#inbox
        pass

    def delete(self, request, author_id):
        """Clear author_id's inbox"""
        pass

# not yet fully tested nor working... but we worry about csrf later
class Csrf(APIView):
    @method_decorator(ensure_csrf_cookie, name='dispatch')
    def get(self, request):
        return JsonResponse({})
    
class Auth(APIView):
    def post(self, request):
        """
        login a user with a username and password
        """
        try:
            data = request.POST.dict()
            user = authenticate(request, username=data['username'], password=data['password'])
            if user:
                login(request, user)
                user_author = Author.objects.get(displayName=user.username)
                auth_response = {"username": user.username, "id": user_author._id}
                return Response(auth_response, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)