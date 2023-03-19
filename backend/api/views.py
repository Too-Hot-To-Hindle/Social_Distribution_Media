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
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema_serializer, extend_schema, OpenApiExample, OpenApiParameter, OpenApiResponse
from pprint import pprint

from .serializers import AuthorSerializer, PostSerializer, CommentSerializer, LikeSerializer, FollowSerializer, UserSerializer, InboxSerializer, InboxPostSerializer
from .models import Author, Post, Comment, Like, Inbox, Follow
from .utils import extract_uuid_if_url

import traceback
import uuid
import json

EXTEND_SCHEMA_PARAM_AUTHOR_ID = OpenApiParameter(
    name="author_id",
    description="The ID of the author",
    required=True,
    type=str,
    location=OpenApiParameter.PATH,
    examples=[
        OpenApiExample(
            "Example 1", 
            value="0f975f4e-9e72-4166-9fd9-e3ce8d85ddc5", 
            summary="Example author_id"
        )
    ],
)

EXTEND_SCHEMA_PARAM_AUTHOR_ID = OpenApiParameter(
    name="author_id",
    description="The ID of the author",
    required=True,
    type=str,
    location=OpenApiParameter.PATH,
    examples=[
        OpenApiExample(
            "Example 1", 
            value="0f975f4e-9e72-4166-9fd9-e3ce8d85ddc5", 
            summary="Example author_id"
        )
    ],
)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    max_page_size = 100

class Authors(APIView):

    pagination_class = StandardResultsSetPagination
    serializer_class = AuthorSerializer

    def get(self, request, format=None):
        """
        Get all authors

        TODO: Query params

        See below for adding new fields (not in model) to response:

        https://stackoverflow.com/questions/37943339/django-rest-framework-how-to-add-a-custom-field-to-the-response-of-the-get-req
        """
        try:
            authors = Author.objects.order_by('displayName') # order by display name so paginator is consistent
            paginator = self.pagination_class()

            # paginate our queryset
            page = paginator.paginate_queryset(authors, request, view=self)

            serializer = AuthorSerializer(page, many=True)  # Must include many=True because it is a list of authors

            return Response(serializer.data)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_404_NOT_FOUND)

class AuthorDetail(APIView):
    
    serializer_class = AuthorSerializer

    @extend_schema(
        parameters=[EXTEND_SCHEMA_PARAM_AUTHOR_ID]
    )
    def get(self, request, author_id):
        """
        Get details for an author
        """
        
        # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
        author_id = extract_uuid_if_url('author', author_id)
        if not author_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            author = Author.objects.get(pk=author_id)
            serializer = AuthorSerializer(author)
            return Response(serializer.data)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        parameters=[EXTEND_SCHEMA_PARAM_AUTHOR_ID],
        request=AuthorSerializer,
        examples=[
            OpenApiExample(
                "Example Author",
                summary="An example author",
                value={
                    "type": "author",
                    "host": "https://example.com",
                    "displayName": "John Doe",
                    "github": "https://github.com/johndoe",
                    "profileImage": "https://example.com/media/profile_images/johndoe.png",
                    "followers": [],
                    "following": [],
                },
            ),
        ],
        responses={
            204: OpenApiResponse(
                description="No Response Body.",
            )
        }
    )
    def post(self, request, author_id):
        """
        Update details for an author
        TODO: This must only be useable as a 'local' user
        """

        # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
        author_id = extract_uuid_if_url('author', author_id)
        if not author_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer = AuthorSerializer(data=json.loads(request.body))
            if serializer.is_valid():
                updated = Author.objects.filter(pk=author_id).update(**serializer.data)
                if updated > 0:
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response('author_id does not exist', status=status.HTTP_404_NOT_FOUND)
            else:
                print(serializer.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class Followers(APIView):
    
    @extend_schema(
        parameters=[EXTEND_SCHEMA_PARAM_AUTHOR_ID],
    )
    def get(self, request, author_id):
        """
        Get a list of authors following the user given by author_id

        TODO: Paging? Query params?

        See below for adding new fields (not in model) to response:

        https://stackoverflow.com/questions/37943339/django-rest-framework-how-to-add-a-custom-field-to-the-response-of-the-get-req
        """
        
        # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
        author_id = extract_uuid_if_url('author', author_id)
        if not author_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            author = Author.objects.get(pk=author_id)
            serializer = AuthorSerializer(author.followers, many=True)
            return Response(serializer.data)
        except Author.DoesNotExist:
            return Response(f'The author {author_id} does not exist.', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            traceback.print_exc()
            traceback.print_exc()
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class FollowersDetail(APIView):


    def get(self, request, author_id, foreign_author_id):
        """Check if foreign_author_id is a follower of author_id"""
        
        # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
        author_id = extract_uuid_if_url('author', author_id)
        foreign_author_id = extract_uuid_if_url('author', foreign_author_id)
        if not (author_id and foreign_author_id):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            author = Author.objects.get(pk=author_id)
            response = {'isFollower': author.followers.filter(pk=foreign_author_id).exists()}
            return Response(response, status=status.HTTP_200_OK)
        except ValidationError as e:
            traceback.print_exc()
            return Response('author_id or foreign_author_id is not a valid uuid')
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, author_id, foreign_author_id):
        """
        Remove foreign_author_id as a follower of author_id
        
        NOTE: Might be a better way to do this
        """
        
        # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
        author_id = extract_uuid_if_url('author', author_id)
        foreign_author_id = extract_uuid_if_url('author', foreign_author_id)
        if not (author_id and foreign_author_id):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            author = Author.objects.get(pk=author_id)
            follower = Author.objects.get(pk=foreign_author_id)
            author.followers.remove(follower)
            follower.following.remove(author)  # Can only do this on local authors
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Author.DoesNotExist:
            return Response(f'The author {author_id} or {foreign_author_id} does not exist.', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, author_id, foreign_author_id):
        """Add foreign_author_id as a follower of author_id"""
        
        # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
        author_id = extract_uuid_if_url('author', author_id)
        foreign_author_id = extract_uuid_if_url('author', foreign_author_id)
        if not (author_id and foreign_author_id):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            serializer = AuthorSerializer(data=request.data)
            if serializer.is_valid():
                author = Author.objects.get(pk=author_id)
                follower = Author.objects.get(pk=foreign_author_id)
                author.followers.add(follower)
                follower.following.add(author)  # Can only do this on local authors
                return Response(AuthorSerializer(follower).data, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Posts(APIView):

    pagination_class = StandardResultsSetPagination

    def get(self, request, author_id):
        """
        Get paginated list of posts by author_id, ordered by post date with most recent first
        
        TODO: Query params, paging

        See below for adding new fields (not in model) to response:

        https://stackoverflow.com/questions/37943339/django-rest-framework-how-to-add-a-custom-field-to-the-response-of-the-get-req
        """
        
        # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
        author_id = extract_uuid_if_url('author', author_id)
        if not author_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            posts = Post.objects.filter(author___id=author_id)
            paginator = self.pagination_class()

            page = paginator.paginate_queryset(posts, request, view=self)

            serializer = PostSerializer(page, many=True)

            return Response(serializer.data)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, author_id):
        """Create a post (post object in body) for author_id, but generate the ID (compare to PUT in PostDetail)"""
        
        # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
        author_id = extract_uuid_if_url('author', author_id)
        if not author_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            serializer = PostSerializer(data=json.loads(request.body))
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
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

class PostDetail(APIView):


    def get(self, request, author_id, post_id):
        """Get post_id posted by author_id"""
        
        # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
        author_id = extract_uuid_if_url('author', author_id)
        post_id = extract_uuid_if_url('post', post_id)
        if not (author_id and post_id):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            post = Post.objects.get(pk=post_id)  # NOTE: Should we do anything with author_id?
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, author_id, post_id):
        """Update post_id posted by author_id (post object in body)"""
        
        # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
        author_id = extract_uuid_if_url('author', author_id)
        post_id = extract_uuid_if_url('post', post_id)
        if not (author_id and post_id):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            serializer = PostSerializer(data=json.loads(request.body))
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
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, author_id, post_id):
        """Delete post_id posted by author_id"""
        
        # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
        author_id = extract_uuid_if_url('author', author_id)
        post_id = extract_uuid_if_url('post', post_id)
        if not (author_id and post_id):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            deleted = Post.objects.filter(pk=post_id, author___id=author_id).delete()
            if deleted[0] > 0:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, author_id, post_id):
        """Create a post (post object in body) for author_id with id post_id"""
        
        # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
        author_id = extract_uuid_if_url('author', author_id)
        post_id = extract_uuid_if_url('post', post_id)
        if not (author_id and post_id):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            serializer = PostSerializer(data=json.loads(request.body))
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
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ImagePosts(APIView):


    def get(self, author_id, post_id):
        """Get post_id posted by author_id, converted to an image"""
        # NOTE: Should return 404 if post is not an image
        pass

class Comments(APIView):

    pagination_class = StandardResultsSetPagination

    def get(self, request, author_id, post_id):
        """Get all comments on post_id posted by author_id"""
        # TODO: Paging
        # TODO: Format response according to spec
        # TODO: Properly 404 if author_id or post_id doesn't exist, could check post_count
        
        # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
        author_id = extract_uuid_if_url('author', author_id)
        post_id = extract_uuid_if_url('post', post_id)
        if not (author_id and post_id):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            comments = Comment.objects.filter(_post_author_id=author_id, _post_id=post_id)
            paginator = self.pagination_class()

            page = paginator.paginate_queryset(comments, request, view=self)

            serializer = CommentSerializer(page, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, author_id, post_id):
        """Add a comment (comment object in body) to post_id posted by author_id"""
        
        # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
        author_id = extract_uuid_if_url('author', author_id)
        post_id = extract_uuid_if_url('post', post_id)
        if not (author_id and post_id):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            request.data['_post_author_id'] = author_id
            request.data['_post_id'] = post_id
            serializer = CommentSerializer(data=request.data)  # request.data parses all request bodies, not just form data
            if serializer.is_valid():
                comment = serializer.create(serializer.data)
                return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostLikes(APIView):


    def get(self, request, author_id, post_id):
        """Get a list of likes on post_id posted by author_id"""
        
        # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
        author_id = extract_uuid_if_url('author', author_id)
        post_id = extract_uuid_if_url('post', post_id)
        if not (author_id and post_id):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if not (Author.objects.filter(pk=author_id).exists() and Post.objects.filter(pk=post_id).exists()):
                return Response('Author or post id does not exist', status=status.HTTP_404_NOT_FOUND)
            likes = Like.objects.filter(object__endswith=f'authors/{author_id}/posts/{post_id}')
            return Response(LikeSerializer(likes, many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CommentLikes(APIView):


    def get(self, request_id, author_id, post_id, comment_id):
        """Get a list of likes on comment_id for post_id posted by author_id"""
        
        # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
        author_id = extract_uuid_if_url('author', author_id)
        post_id = extract_uuid_if_url('post', post_id)
        comment_id = extract_uuid_if_url('comment', comment_id)
        if not (author_id and post_id and comment_id):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if not (Author.objects.filter(pk=author_id).exists() and Post.objects.filter(pk=post_id).exists() and Comment.objects.filter(pk=comment_id).exists()):
                return Response('Author, post, or comment id does not exist', status=status.HTTP_404_NOT_FOUND)
            # likes = Like.objects.filter(author___id=author_id, object__endswith=f'/posts/{post_id}/comments/{comment_id}')
            likes = Like.objects.filter(object__endswith=f'authors/{author_id}/posts/{post_id}/comments/{comment_id}')
            return Response(LikeSerializer(likes, many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LikedPosts(APIView):


    def get(self, request, author_id):
        """Get list of posts author_id has liked"""
        
        # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
        author_id = extract_uuid_if_url('author', author_id)
        if not author_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if not (Author.objects.filter(pk=author_id).exists()):
                return Response('Author id does not exist', status=status.HTTP_404_NOT_FOUND)
            likes = Like.objects.filter(author___id=author_id)
            return Response(LikeSerializer(likes, many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InboxDetail(APIView):

    pagination_class = StandardResultsSetPagination

    def get(self, request, author_id):
        """Get list of posts sent to author_id"""
        
        author_id = extract_uuid_if_url('author', author_id)
        if not author_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            inbox = Inbox.objects.get(author___id=author_id)
            inbox_items = inbox.items.all()
            paginator = self.pagination_class()

            # paginate just the inbox items
            page = paginator.paginate_queryset(inbox_items, request, view=self)

            # serialize paginated inbox items and inbox
            inbox_posts_serializer = InboxPostSerializer(page, many=True)
            serializer = InboxSerializer(inbox)

            # update the inbox data with the serialized inbox items
            inbox_data = serializer.data
            inbox_data['items'] = inbox_posts_serializer.data

            return Response(inbox_data, status=status.HTTP_200_OK)
        except Inbox.DoesNotExist:
            return Response('That author id does not exist',status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, author_id):
        """Send a post to author_id"""
        # NOTE: 4 different cases based on type field in post request body
        # See https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#inbox
        
        author_id = extract_uuid_if_url('author', author_id)
        if not author_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        object = request.data
        match object['type']:
            case 'post':
                serializer = InboxPostSerializer(data=object)
                if serializer.is_valid():
                    # Create post and post author if they don't exist (foreign case)
                    if Post.objects.filter(id=serializer.validated_data['id']).exists():
                        post = Post.objects.get(id=serializer.validated_data['id'])  # Will only work for local posts
                    else:
                        post = serializer.create(serializer.validated_data)
                    inbox = Inbox.objects.get(author___id=author_id)
                    inbox.items.add(post)
                    return Response(InboxPostSerializer(post).data, status=status.HTTP_200_OK)
                else:
                    print(serializer.errors)
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            case 'follow':
                serializer = FollowSerializer(data=object)
                if serializer.is_valid():
                    follow = serializer.create(serializer.data)
                    return Response(FollowSerializer(follow).data, status=status.HTTP_201_CREATED)
                else:
                    print(serializer.errors)
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            case 'like':
                serializer = LikeSerializer(data=object)
                if serializer.is_valid():
                    like = serializer.create(serializer.data)
                    return Response(LikeSerializer(like).data, status=status.HTTP_201_CREATED)
                else:
                    print(serializer.errors)
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            case 'comment':
                serializer = CommentSerializer(data=object)
                if serializer.is_valid():
                    pass
                else:
                    print(serializer.errors)
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            case _:
                return Response("Object type must be one of 'post', 'follow', 'like', or 'comment'", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, author_id):
        """Clear author_id's inbox"""
        
        author_id = extract_uuid_if_url('author', author_id)
        if not author_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            inbox = Inbox.objects.get(author___id=author_id)
            inbox.items.clear()  # Use clear() because we don't want to delete related posts, just remove the relation
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FollowRequests(APIView):


    def get(self, request, author_id):
        """Get requests to follow author_id"""
        
        author_id = extract_uuid_if_url('author', author_id)
        if not author_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if not Author.objects.filter(pk=author_id).exists():
                return Response('That author id does not exist', status=status.HTTP_404_NOT_FOUND)
            requests = Follow.objects.filter(object___id=author_id)
            return Response(FollowSerializer(requests, many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# not yet fully tested nor working... but we worry about csrf later
# class Csrf(APIView):
#     @method_decorator(ensure_csrf_cookie, name='dispatch')
#     def get(self, request):
#         return JsonResponse({})
    
class Auth(APIView):
    # make it so users logging in do not have to authenticate
    authentication_classes = []
    permission_classes = []
    serializer_class = UserSerializer

    @extend_schema(
        request={
            "application/json": {
                "description": "Form data.",
                "schema": {
                    "type": "object",
                    "properties": {
                        "username": {"type": "string"},
                        "password": {"type": "string", "format": "password"},
                    },
                    "required": ["username", "password"],
                },
                "example": {
                    "username": "steven",
                    "password": "pwd",
                },
            }
        }
    )
    def post(self, request):
        """
        login a user with a username and password
        """
        try:
            data = json.loads(request.body)
            user = authenticate(request, username=data['username'], password=data['password'])
            if user:
                login(request, user)
                user_author = Author.objects.get(displayName=user.username)
                auth_response = {"username": user.username, "id": user_author._id}
                return Response(auth_response, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AuthRegister(APIView):
    # make it so users registering do not have to login
    authentication_classes = []
    permission_classes = []
    serializer_class = UserSerializer

    @extend_schema(
        request={
            "application/json": {
                "description": "Form data.",
                "schema": {
                    "type": "object",
                    "properties": {
                        "username": {"type": "string"},
                        "password": {"type": "string", "format": "password"},
                    },
                    "required": ["username", "password"],
                },
                "example": {
                    "username": "john.doe",
                    "password": "my_password",
                },
            }
        }
    )
    def post(self, request):
        """
        register a new user
        """
        try:
            # create our user and an author, and link it with the author.
            serializer = UserSerializer(data=json.loads(request.body))
            if serializer.is_valid():
                user = serializer.data
                user = User.objects.create_user(user['username'], password=user['password'])
                # TODO: Need to figure out if we want display name to be unique, or have another unique identifier from the registration page
                # to use for creating authors...
                Author.objects.create(user=user, displayName=user.username)
                return Response(user.username, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)