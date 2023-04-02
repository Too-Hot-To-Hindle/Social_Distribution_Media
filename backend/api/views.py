from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse, OpenApiTypes
from pprint import pprint
import docs.docs as docs
import urllib.parse
import base64

from .serializers import AuthorSerializer, AuthorsSerializer, FollowersSerializer, PostSerializer, PostsSerializer, CommentSerializer, CommentsSerializer, LikeRequestSerializer, LikeResponseSerializer, LikedSerializer, LikesSerializer, FollowSerializer, FollowsSerializer, UserSerializer, InboxSerializer, InboxPostSerializer
from .models import Author, Post, Comment, Like, Inbox, Follow
from .utils import extract_uuid_if_url
from .utils import is_remote_url
from .utils import get_remote_url
from .utils import extract_id_if_url_group_6
from .utils import extract_id_if_url_group_10
from .connections import RemoteConnection, RemoteServerError, Remote404
from .decorators import friend_check
from .permissions import IsOwnerOrFriend

import traceback
import uuid
import json


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    max_page_size = 100


class Authors(APIView):

    pagination_class = StandardResultsSetPagination
    serializer_class = AuthorSerializer

    @extend_schema(
        parameters=[docs.EXTEND_SCHEMA_PARAM_PAGE,
                    docs.EXTEND_SCHEMA_PARAM_SIZE],
        tags=['Authors', 'Remote API'],
        responses={
            200: docs.EXTEND_SCHEMA_RESP_LIST_AUTHORS
        },
    )
    def get(self, request, format=None):
        """Gets all local authors from our database. To make proxied requests to an external server to retrieve all their authors, use /api/remote/authors/{remote_url}."""
        try:
            authors = Author.objects.order_by('displayName').filter(
                remote=False)  # order by display name so paginator is consistent
            paginator = self.pagination_class()

            # # paginate our queryset
            page = paginator.paginate_queryset(authors, request, view=self)

            serializer = AuthorsSerializer({'items': page})

            return Response(serializer.data)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_404_NOT_FOUND)


class AuthorDetail(APIView):

    serializer_class = AuthorSerializer

    @extend_schema(
        parameters=[docs.EXTEND_SCHEMA_PARAM_AUTHOR_ID],
        tags=['Authors', 'Remote API'],
        responses={
        200: docs.EXTEND_SCHEMA_RESP_AUTHOR,
        404: OpenApiResponse(
                description="The author does not exist",
            ),
        }
    )
    def get(self, request, author_id):
        """Get details for an author from our database. Supports remote authors; to make proxied requests to an external server, provide the full ID of the external author URL encoded in place of {author_id}."""

        if is_remote_url(author_id):
            remote_url = get_remote_url(author_id)
            remote = RemoteConnection(remote_url)

            # Group 6 does not use UUID's for their object IDs
            # Nor does Group 10
            # So we need to extract those specially
            if (author_id.startswith("https://cmput404-group6-instatonne.herokuapp.com/")):
                author_id = extract_id_if_url_group_6('author', author_id)
            elif (author_id.startswith("https://socialdistcmput404.herokuapp.com/")):
                author_id = extract_id_if_url_group_10('author', author_id)
            else:
                author_id = extract_uuid_if_url('author', author_id)

            try:
                response = remote.connection.get_single_author(author_id)
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

            except Remote404 as e:
                return Response(e.args, status=status.HTTP_404_NOT_FOUND)

            except RemoteServerError as e:
                return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
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
        parameters=[docs.EXTEND_SCHEMA_PARAM_AUTHOR_ID],
        tags=['Authors'],
        request=AuthorSerializer,
        examples=[
            OpenApiExample(
                "Example Author",
                summary="An example author",
                value={
                    "id": "https://social-media-distribution.herokuapp.com/api/author/1170f51f-6dc2-4616-a71a-ff78dcef7212",
                    "type": "author",
                    "host": "https://social-media-distribution.herokuapp.com/api",
                    "displayName": "John Doe",
                    "github": "https://github.com/johndoe",
                    "profileImage": "https://example.com/media/profile_images/johndoe.png"
                },
            ),
        ],
        responses={
            204: OpenApiResponse(
                description="No Response Body.",
            ),
            404: OpenApiResponse(
                description="The author does not exist",
            ),
        }
    )
    def post(self, request, author_id):
        """Update details for an author."""

        # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
        author_id = extract_uuid_if_url('author', author_id)
        if not author_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer = AuthorSerializer(data=json.loads(request.body))
            if serializer.is_valid():
                updated = Author.objects.filter(
                    pk=author_id).update(**serializer.data)
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
        parameters=[docs.EXTEND_SCHEMA_PARAM_AUTHOR_ID],
        responses={
            200: docs.EXTEND_SCHEMA_RESP_LIST_FOLLOWERS,
            404: OpenApiResponse(
                description="The author does not exist",
            ),
        },
        tags=['Followers', 'Remote API']
    )
    def get(self, request, author_id):
        """Gets a list of authors that follow the user given by {author_id}. Supports remote authors; to make proxied requests to an external server, provide the full ID of the external author URL encoded in place of {author_id}."""
        if is_remote_url(author_id):
            remote_url = get_remote_url(author_id)
            remote = RemoteConnection(remote_url)

            # Group 6 does not use UUID's for their object IDs
            # Nor does Group 10
            # So we need to extract those specially
            if (author_id.startswith("https://cmput404-group6-instatonne.herokuapp.com/")):
                author_id = extract_id_if_url_group_6('author', author_id)
            elif (author_id.startswith("https://socialdistcmput404.herokuapp.com/")):
                author_id = extract_id_if_url_group_10('author', author_id)
            else:
                author_id = extract_uuid_if_url('author', author_id)

            try:
                response = remote.connection.get_author_followers(author_id)
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

            except Remote404 as e:
                return Response(e.args, status=status.HTTP_404_NOT_FOUND)

            except RemoteServerError as e:
                return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
            author_id = extract_uuid_if_url('author', author_id)
            if not author_id:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                author = Author.objects.get(pk=author_id)
                # serializer = AuthorSerializer(author.followers, many=True)
                serializer = FollowersSerializer({'items': author.followers})
                return Response(serializer.data)
            except Author.DoesNotExist:
                return Response(f'The author {author_id} does not exist.', status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                traceback.print_exc()
                traceback.print_exc()
                return Response(status=status.HTTP_404_NOT_FOUND)


class FollowersDetail(APIView):

    @extend_schema(
        parameters=[
            docs.EXTEND_SCHEMA_PARAM_AUTHOR_ID,
            docs.EXTEND_SCHEMA_PARAM_FOREIGN_AUTHOR_ID
        ],
        responses={
            200: docs.EXTEND_SCHEMA_RESP_IS_FOLLOWER,
            404: OpenApiResponse(
                description="The author does not exist",
            ),
        },
        tags=['Followers', 'Remote API']
    )
    def get(self, request, author_id, foreign_author_id):
        """Check if {foreign_author_id} is a follower of {author_id}. Supports remote authors; to make proxied requests to an external server, provide the full ID of the external author URL encoded in place of {author_id}, and the full ID of the external foreign author URL encoded in place of {foreign_author_id}."""

        # case 1: author_id and foreign_author_id are both remote
        if is_remote_url(author_id) and is_remote_url(foreign_author_id):
            remote_url = get_remote_url(author_id)
            remote = RemoteConnection(remote_url)
            
            # Group 6 does not use UUID's for their object IDs
            # Nor does Group 10
            # So we need to extract those specially
            if (author_id.startswith("https://cmput404-group6-instatonne.herokuapp.com/")):
                author_id = extract_id_if_url_group_6('author', author_id)
            elif (author_id.startswith("https://socialdistcmput404.herokuapp.com/")):
                author_id = extract_id_if_url_group_10('author', author_id)
            else:
                author_id = extract_uuid_if_url('author', author_id)


            # Group 6 does not use UUID's for their object IDs
            # Nor does Group 10
            # So we need to extract those specially
            if (foreign_author_id.startswith("https://cmput404-group6-instatonne.herokuapp.com/")):
                foreign_author_id = extract_id_if_url_group_6('author', foreign_author_id)
            elif (foreign_author_id.startswith("https://socialdistcmput404.herokuapp.com/")):
                foreign_author_id = extract_id_if_url_group_10('author', foreign_author_id)
            else:
                foreign_author_id = extract_uuid_if_url('author', foreign_author_id)

            try:
                response = remote.connection.check_if_follower(
                    author_id, foreign_author_id)
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

            except Exception as e:
                return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # case 2: author_id is remote, foreign_author_id is local
        if is_remote_url(author_id) and not is_remote_url(foreign_author_id):
            remote_url = get_remote_url(author_id)
            remote = RemoteConnection(remote_url)
            
            # Group 6 does not use UUID's for their object IDs
            # Nor does Group 10
            # So we need to extract those specially
            if (author_id.startswith("https://cmput404-group6-instatonne.herokuapp.com/")):
                author_id = extract_id_if_url_group_6('author', author_id)
            elif (author_id.startswith("https://socialdistcmput404.herokuapp.com/")):
                author_id = extract_id_if_url_group_10('author', author_id)
            else:
                author_id = extract_uuid_if_url('author', author_id)


            # Group 6 does not use UUID's for their object IDs
            # Nor does Group 10
            # So we need to extract those specially
            if (foreign_author_id.startswith("https://cmput404-group6-instatonne.herokuapp.com/")):
                foreign_author_id = extract_id_if_url_group_6('author', foreign_author_id)
            elif (foreign_author_id.startswith("https://socialdistcmput404.herokuapp.com/")):
                foreign_author_id = extract_id_if_url_group_10('author', foreign_author_id)
            else:
                foreign_author_id = extract_uuid_if_url('author', foreign_author_id)

            try:
                response = remote.connection.check_if_follower(
                    author_id, foreign_author_id)
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

            except Exception as e:
                return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # case 3: author_id is local, foreign_author_id is remote
        if not is_remote_url(author_id) and is_remote_url(foreign_author_id):
            # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
            
            # Group 6 does not use UUID's for their object IDs
            # Nor does Group 10
            # So we need to extract those specially
            if (author_id.startswith("https://cmput404-group6-instatonne.herokuapp.com/")):
                author_id = extract_id_if_url_group_6('author', author_id)
            elif (author_id.startswith("https://socialdistcmput404.herokuapp.com/")):
                author_id = extract_id_if_url_group_10('author', author_id)
            else:
                author_id = extract_uuid_if_url('author', author_id)


            # Group 6 does not use UUID's for their object IDs
            # Nor does Group 10
            # So we need to extract those specially
            if (foreign_author_id.startswith("https://cmput404-group6-instatonne.herokuapp.com/")):
                foreign_author_id = extract_id_if_url_group_6('author', foreign_author_id)
            elif (foreign_author_id.startswith("https://socialdistcmput404.herokuapp.com/")):
                foreign_author_id = extract_id_if_url_group_10('author', foreign_author_id)
            else:
                foreign_author_id = extract_uuid_if_url('author', foreign_author_id)

            if not (author_id and foreign_author_id):
                return Response(status=status.HTTP_404_NOT_FOUND)

            try:
                author = Author.objects.get(pk=author_id)
                response = {'isFollower': author.followers.filter(
                    pk=foreign_author_id).exists()}
                if (author.followers.filter(pk=foreign_author_id).exists()):
                    return Response(response, status=status.HTTP_200_OK)

                else:
                    return Response(response, status=status.HTTP_404_NOT_FOUND)
            except ValidationError as e:
                traceback.print_exc()
                return Response('author_id or foreign_author_id is not a valid uuid', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                traceback.print_exc()
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # case 4: author_id and foreign_author_id are both local
        if not is_remote_url(author_id) and not is_remote_url(foreign_author_id):
            # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
            
            # Group 6 does not use UUID's for their object IDs
            # Nor does Group 10
            # So we need to extract those specially
            if (author_id.startswith("https://cmput404-group6-instatonne.herokuapp.com/")):
                author_id = extract_id_if_url_group_6('author', author_id)
            elif (author_id.startswith("https://socialdistcmput404.herokuapp.com/")):
                author_id = extract_id_if_url_group_10('author', author_id)
            else:
                author_id = extract_uuid_if_url('author', author_id)


            # Group 6 does not use UUID's for their object IDs
            # Nor does Group 10
            # So we need to extract those specially
            if (foreign_author_id.startswith("https://cmput404-group6-instatonne.herokuapp.com/")):
                foreign_author_id = extract_id_if_url_group_6('author', foreign_author_id)
            elif (foreign_author_id.startswith("https://socialdistcmput404.herokuapp.com/")):
                foreign_author_id = extract_id_if_url_group_10('author', foreign_author_id)
            else:
                foreign_author_id = extract_uuid_if_url('author', foreign_author_id)

            if not (author_id and foreign_author_id):
                return Response(status=status.HTTP_404_NOT_FOUND)

            try:
                author = Author.objects.get(pk=author_id)
                response = {'isFollower': author.followers.filter(
                    pk=foreign_author_id).exists()}
                if (author.followers.filter(pk=foreign_author_id).exists()):
                    return Response(response, status=status.HTTP_200_OK)

                else:
                    return Response(response, status=status.HTTP_404_NOT_FOUND)
            except ValidationError as e:
                traceback.print_exc()
                return Response('author_id or foreign_author_id is not a valid uuid', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                traceback.print_exc()
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        tags=['Followers'],
        responses={
            200: None,
            404: OpenApiResponse(
                description="The author does not exist",
            ),
        }
    )
    def delete(self, request, author_id, foreign_author_id):
        """Remove {foreign_author_id} as a follower of {author_id}."""

        # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
        author_id = extract_uuid_if_url('author', author_id)
        foreign_author_id = extract_uuid_if_url('author', foreign_author_id)
        if not (author_id and foreign_author_id):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            author = Author.objects.get(pk=author_id)
            follower = Author.objects.get(pk=foreign_author_id)
            author.followers.remove(follower)
            # Can only do this on local authors
            follower.following.remove(author)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Author.DoesNotExist:
            return Response(f'The author {author_id} or {foreign_author_id} does not exist.', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        tags=['Followers'],
        responses={
            200: None,
            404: OpenApiResponse(
                description="The author does not exist",
            ),
        }
    )
    def put(self, request, author_id, foreign_author_id):
        """Add {foreign_author_id} as a follower of {author_id}."""

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
                # Can only do this on local authors
                follower.following.add(author)
                return Response(AuthorSerializer(follower).data, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Posts(APIView):

    pagination_class = StandardResultsSetPagination

    # sets custom flag (request.is_friend) to true if requesting user is friend of author or is the author 
    permission_classes = [IsOwnerOrFriend]

    # @friend_check
    @extend_schema(
        parameters=[docs.EXTEND_SCHEMA_PARAM_AUTHOR_ID,
                    docs.EXTEND_SCHEMA_PARAM_PAGE, docs.EXTEND_SCHEMA_PARAM_SIZE],
        responses={
            200: docs.EXTEND_SCHEMA_RESP_LIST_POSTS,
            404: OpenApiResponse(
                description="The author does not exist",
            ),
        },
        tags=['Posts', 'Remote API']
    )
    def get(self, request, author_id):
        """Get paginated list of posts by {author_id}, ordered by post date with most recent first. Supports remote authors; to make proxied requests to an external server, provide the full ID of the external author URL encoded in place of {author_id}."""

        if is_remote_url(author_id):
            remote_url = get_remote_url(author_id)
            remote = RemoteConnection(remote_url)
                
            # Group 6 does not use UUID's for their object IDs
            # Nor does Group 10
            # So we need to extract those specially
            if (author_id.startswith("https://cmput404-group6-instatonne.herokuapp.com/")):
                author_id = extract_id_if_url_group_6('author', author_id)
            elif (author_id.startswith("https://socialdistcmput404.herokuapp.com/")):
                author_id = extract_id_if_url_group_10('author', author_id)
            else:
                author_id = extract_uuid_if_url('author', author_id)

            try:
                response = remote.connection.get_recent_posts(author_id)
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

            except Exception as e:
                return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
            author_id = extract_uuid_if_url('author', author_id)
            if not author_id:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            # first, check if the author exists
            author = Author.objects.filter(pk=author_id).first()
            if not author:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            # check if requestor is owner or friend of owner
            self.check_object_permissions(request, author)

            try:
                # get all posts if the requestor is a friend, otherwise only get public posts
                posts = Post.objects.filter(author_id=author_id) if request.is_friend else Post.objects.filter(author_id=author_id, visibility="PUBLIC")

                paginator = self.pagination_class()

                page = paginator.paginate_queryset(posts, request, view=self)

                serializer = PostsSerializer({'items': page})

                return Response(serializer.data)

            except Exception as e:
                traceback.print_exc()
                return Response(status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        parameters=[docs.EXTEND_SCHEMA_PARAM_AUTHOR_ID],
        tags=['Posts'],
        request=InboxPostSerializer,
        examples=[docs.EXTEND_SCHEMA_EXAMPLE_INBOX_SEND_POST],
        responses={
            200: OpenApiResponse(
                description="The post that was posted",
                examples=[docs.EXTEND_SCHEMA_EXAMPLE_INBOX_SEND_POST],
                response=OpenApiTypes.OBJECT,
            ),
            404: OpenApiResponse(
                description="The author does not exist",
            ),
        },
    )
    def post(self, request, author_id):
        """Create a post (post object in body) for {author_id}, but generate the ID (compared to PUT endpoint, where you need to know the ID ahead of time)."""

        # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
        author_id = extract_uuid_if_url('author', author_id)
        if not author_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        # check if requestor is author
        post_author = get_object_or_404(Author, pk=author_id)
        self.check_object_permissions(request, post_author)
        if not request.is_owner:
            return Response(status=status.HTTP_403_FORBIDDEN)

        try:
            serializer = PostSerializer(data=json.loads(request.body))
            if serializer.is_valid():
                post = Post.objects.create(
                    **serializer.data, author_id=author_id)
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

    # will checks if 
    permission_classes = [IsOwnerOrFriend]

    @extend_schema(
        parameters=[
            docs.EXTEND_SCHEMA_PARAM_AUTHOR_ID,
            docs.EXTEND_SCHEMA_PARAM_POST_ID
        ],
        responses={
            200: docs.EXTEND_SCHEMA_RESP_POST,
            404: OpenApiResponse(
                description="The author or post does not exist",
            ),
        },
        tags=['Posts', 'Remote API']
    )
    def get(self, request, author_id, post_id):
        """Get post_id posted by {author_id}. Supports remote authors; to make proxied requests to an external server, provide the full ID of the external author URL encoded in place of {author_id}, whereas {post_id} needs to remain the UUID/identifier only (non-url)."""

        if is_remote_url(author_id):
            remote_url = get_remote_url(author_id)
            remote = RemoteConnection(remote_url)
            
            # Group 6 does not use UUID's for their object IDs
            # Nor does Group 10
            # So we need to extract those specially
            if (author_id.startswith("https://cmput404-group6-instatonne.herokuapp.com/")):
                author_id = extract_id_if_url_group_6('author', author_id)
            elif (author_id.startswith("https://socialdistcmput404.herokuapp.com/")):
                author_id = extract_id_if_url_group_10('author', author_id)
            else:
                author_id = extract_uuid_if_url('author', author_id)

            try:
                response = remote.connection.get_single_post(
                    author_id, post_id)
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

            except Remote404 as e:
                return Response(e.args, status=status.HTTP_404_NOT_FOUND)

            except RemoteServerError as e:
                return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
            author_id = extract_uuid_if_url('author', author_id)
            post_id = extract_uuid_if_url('post', post_id)
            if not (author_id and post_id):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            author = get_object_or_404(Author, pk=author_id)
            # check if requestor is owner or friend of owner
            self.check_object_permissions(request, author)

            try:
                post = Post.objects.get(pk=post_id)

                # if requestor is not a friend and the post visibility is set to friends, return 403
                if not request.is_friend and post.visibility == "FRIENDS":
                    return Response(status=status.HTTP_403_FORBIDDEN)
                
                serializer = PostSerializer(post)
                return Response(serializer.data)
            except Exception as e:
                traceback.print_exc()
                return Response(status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        parameters=[
            docs.EXTEND_SCHEMA_PARAM_AUTHOR_ID,
            docs.EXTEND_SCHEMA_PARAM_POST_ID
        ],
        tags=['Posts'],
        request=InboxPostSerializer,
        examples=[docs.EXTEND_SCHEMA_EXAMPLE_INBOX_SEND_POST],
        responses={
            200: OpenApiResponse(
                description="The post that was posted",
                examples=[docs.EXTEND_SCHEMA_EXAMPLE_INBOX_SEND_POST],
                response=OpenApiTypes.OBJECT,
            ),
            404: OpenApiResponse(
                description="The author or post does not exist",
            ),
        },
    )
    def post(self, request, author_id, post_id):
        """Update post_id posted by {author_id} (post object in body)."""

        # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
        author_id = extract_uuid_if_url('author', author_id)
        post_id = extract_uuid_if_url('post', post_id)
        if not (author_id and post_id):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer = PostSerializer(data=json.loads(request.body))
            if serializer.is_valid():
                req_post = get_object_or_404(Post, pk=post_id, author___id=author_id)
                # check if requesting user is author of post
                self.check_object_permissions(request, req_post.author)
                if not request.is_owner:
                    return Response(status=status.HTTP_403_FORBIDDEN)

                updated = Post.objects.filter(
                    pk=post_id, author___id=author_id).update(**serializer.data)
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

    @extend_schema(
        parameters=[
            docs.EXTEND_SCHEMA_PARAM_AUTHOR_ID,
            docs.EXTEND_SCHEMA_PARAM_POST_ID
        ],
        tags=['Posts'],
        responses={
            200: None,
            404: OpenApiResponse(
                description="The author or post does not exist",
            ),
        },
    )
    def delete(self, request, author_id, post_id):
        """Delete {post_id} posted by {author_id}."""

        # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
        author_id = extract_uuid_if_url('author', author_id)
        post_id = extract_uuid_if_url('post', post_id)
        if not (author_id and post_id):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            req_post = get_object_or_404(Post, pk=post_id, author___id=author_id)
            # check if requesting user is author of post
            self.check_object_permissions(request, req_post.author)
            if not request.is_owner:
                return Response(status=status.HTTP_403_FORBIDDEN)

            deleted = Post.objects.filter(
                pk=post_id, author___id=author_id).delete()
            if deleted[0] > 0:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        parameters=[
            docs.EXTEND_SCHEMA_PARAM_AUTHOR_ID,
            docs.EXTEND_SCHEMA_PARAM_POST_ID
        ],
        tags=['Posts'],
        request=InboxPostSerializer,
        examples=[docs.EXTEND_SCHEMA_EXAMPLE_INBOX_SEND_POST],
        responses={
            200: OpenApiResponse(
                description="The post that was posted",
                examples=[docs.EXTEND_SCHEMA_EXAMPLE_INBOX_SEND_POST],
                response=OpenApiTypes.OBJECT,
            ),
            404: OpenApiResponse(
                description="The author or post does not exist",
            ),
        },
    )
    def put(self, request, author_id, post_id):
        """Create a post (post object in body) for {author_id} with id {post_id}."""

        # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
        author_id = extract_uuid_if_url('author', author_id)
        post_id = extract_uuid_if_url('post', post_id)
        if not (author_id and post_id):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        # can't create a post on behalf of another author
        post_author = get_object_or_404(Author, pk=author_id)
        self.check_object_permissions(request, post_author)
        if not request.is_owner:
            return Response(status=status.HTTP_403_FORBIDDEN)

        try:
            serializer = PostSerializer(data=json.loads(request.body))
            if serializer.is_valid():

                post = Post.objects.create(
                    **serializer.data, pk=post_id, author_id=author_id)
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

    @extend_schema(
        tags=['Posts', 'Remote API'],
        responses={
            200: OpenApiResponse(
                description="The image post in binary",
            ),
            404: OpenApiResponse(
                description="The post is not an image or does not exist",
            ),
        },
    )
    def get(self, request, author_id, post_id):
        """Get post_id posted by {author_id}, converted to an image. Supports remote authors; to make proxied requests to an external server, provide the full ID of the external author URL encoded in place of {author_id}, whereas {post_id} needs to remain the UUID/identifier only (non-url)."""
        # NOTE: Should return 404 if post is not an image

        if is_remote_url(author_id):
            remote_url = get_remote_url(author_id)
            remote = RemoteConnection(remote_url)

            # Group 6 does not use UUID's for their object IDs
            # Nor does Group 10
            # So we need to extract those specially
            if (author_id.startswith("https://cmput404-group6-instatonne.herokuapp.com/")):
                author_id = extract_id_if_url_group_6('author', author_id)
            elif (author_id.startswith("https://socialdistcmput404.herokuapp.com/")):
                author_id = extract_id_if_url_group_10('author', author_id)
            else:
                author_id = extract_uuid_if_url('author', author_id)

            try:
                response = remote.connection.get_image_post(author_id, post_id)

                binary = response[0]
                content_type = response[1]
                return HttpResponse(binary, content_type=content_type)
            
            except Remote404:
                return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
            author_id = extract_uuid_if_url('author', author_id)
            post_id = extract_uuid_if_url('post', post_id)

            if not (author_id and post_id):
                return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                # NOTE: Should we do anything with author_id?
                post = Post.objects.get(pk=post_id)
                serializer = PostSerializer(post)

                if (serializer.data["contentType"] == "image/png;base64" or serializer.data["contentType"] == "image/jpeg;base64"):
                    image_data = serializer.data["content"].partition('base64,')[2]
                    binary = base64.b64decode(image_data)
                    return HttpResponse(binary, content_type=serializer.data["contentType"])

                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                traceback.print_exc()
                return Response(status=status.HTTP_404_NOT_FOUND)


class Comments(APIView):

    pagination_class = StandardResultsSetPagination

    @extend_schema(
        parameters=[
            docs.EXTEND_SCHEMA_PARAM_AUTHOR_ID,
            docs.EXTEND_SCHEMA_PARAM_POST_ID,
            docs.EXTEND_SCHEMA_PARAM_PAGE,
            docs.EXTEND_SCHEMA_PARAM_SIZE
        ],
        responses={
            200: docs.EXTEND_SCHEMA_RESP_LIST_COMMENTS,
            404: OpenApiResponse(
                description="The author or post does not exist",
            ),
        },
        tags=["Comments", "Remote API"],
    )
    def get(self, request, author_id, post_id):
        """Get all comments on {post_id} posted by {author_id}. Supports remote authors; to make proxied requests to an external server, provide the full ID of the external author URL encoded in place of {author_id}, whereas {post_id} needs to remain the UUID/identifier only (non-url)."""
        # TODO: Format response according to spec
        # TODO: Properly 404 if author_id or post_id doesn't exist, could check post_count

        if is_remote_url(author_id):
            remote_url = get_remote_url(author_id)
            remote = RemoteConnection(remote_url)

            # Group 6 does not use UUID's for their object IDs
            # Nor does Group 10
            # So we need to extract those specially
            if (author_id.startswith("https://cmput404-group6-instatonne.herokuapp.com/")):
                author_id = extract_id_if_url_group_6('author', author_id)
            elif (author_id.startswith("https://socialdistcmput404.herokuapp.com/")):
                author_id = extract_id_if_url_group_10('author', author_id)
            else:
                author_id = extract_uuid_if_url('author', author_id)

            try:
                response = remote.connection.get_comments(author_id, post_id)
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

            except Exception as e:
                return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
            author_id = extract_uuid_if_url('author', author_id)
            post_id = extract_uuid_if_url('post', post_id)
            if not (author_id and post_id):
                return Response(status=status.HTTP_404_NOT_FOUND)

            try:
                # comments = Comment.objects.filter(_post_author_id=author_id, _post_id=post_id)
                comments = Comment.objects.filter(
                    id__contains=f'{author_id}/posts/{post_id}')
                paginator = self.pagination_class()

                page = paginator.paginate_queryset(
                    comments, request, view=self)

                serializer = CommentsSerializer({'items': page})
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Exception as e:
                traceback.print_exc()
                return Response(status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        parameters=[
            docs.EXTEND_SCHEMA_PARAM_AUTHOR_ID,
            docs.EXTEND_SCHEMA_PARAM_POST_ID
        ],
        request=InboxPostSerializer,
        tags=["Comments"],
        examples=[docs.EXTEND_SCHEMA_EXAMPLE_INBOX_SEND_COMMENT],
        responses={
            200: OpenApiResponse(
                description="The comment that was posted",
                examples=[docs.EXTEND_SCHEMA_EXAMPLE_INBOX_SEND_COMMENT],
                response=OpenApiTypes.OBJECT,
            ),
            404: OpenApiResponse(
                description="The author or post does not exist",
            ),
        },
    )
    def post(self, request, author_id, post_id):
        """Add a comment (comment object in body) to {post_id} posted by {author_id}."""

        try:
            # TODO: Fix get comments above now that these are gone
            # request.data parses all request bodies, not just form data
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                comment = serializer.create(serializer.data)
                return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response('Bad request, maybe a comment with this ID already exists?', status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostLikes(APIView):

    @extend_schema(
        parameters=[
            docs.EXTEND_SCHEMA_PARAM_AUTHOR_ID,
            docs.EXTEND_SCHEMA_PARAM_POST_ID
        ],
        responses={
            200: docs.EXTEND_SCHEMA_RESP_LIST_POST_LIKES,
            404: OpenApiResponse(
                description="The author or post does not exist",
            ),
        },
        tags=['Likes', 'Remote API'],
    )
    def get(self, request, author_id, post_id):
        """Get a list of likes on {post_id} posted by {author_id}. Supports remote authors; to make proxied requests to an external server, provide the full ID of the external author URL encoded in place of {author_id}, whereas {post_id} needs to remain the UUID/identifier only (non-url)."""

        if is_remote_url(author_id):
            remote_url = get_remote_url(author_id)
            remote = RemoteConnection(remote_url)

            # Group 6 does not use UUID's for their object IDs
            # Nor does Group 10
            # So we need to extract those specially
            if (author_id.startswith("https://cmput404-group6-instatonne.herokuapp.com/")):
                author_id = extract_id_if_url_group_6('author', author_id)
            elif (author_id.startswith("https://socialdistcmput404.herokuapp.com/")):
                author_id = extract_id_if_url_group_10('author', author_id)
            else:
                author_id = extract_uuid_if_url('author', author_id)

            try:
                response = remote.connection.get_post_likes(author_id, post_id)
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

            except Exception as e:
                return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
            author_id = extract_uuid_if_url('author', author_id)
            post_id = extract_uuid_if_url('post', post_id)
            if not (author_id and post_id):
                return Response(status=status.HTTP_404_NOT_FOUND)

            try:
                if not (Author.objects.filter(pk=author_id).exists() and Post.objects.filter(pk=post_id).exists()):
                    return Response('Author or post id does not exist', status=status.HTTP_404_NOT_FOUND)
                likes = Like.objects.filter(
                    object__endswith=f'authors/{author_id}/posts/{post_id}')
                serializer = LikesSerializer({'items': likes})
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Exception as e:
                traceback.print_exc()
                return Response(status=status.HTTP_404_NOT_FOUND)


class CommentLikes(APIView):

    @extend_schema(
        parameters=[
            docs.EXTEND_SCHEMA_PARAM_AUTHOR_ID,
            docs.EXTEND_SCHEMA_PARAM_POST_ID,
            docs.EXTEND_SCHEMA_PARAM_COMMENT_ID
        ],
        responses={
            200: docs.EXTEND_SCHEMA_RESP_LIST_COMMENT_LIKES,
            404: OpenApiResponse(
                description="The author, post, or comment does not exist",
            ),
        },
        tags=['Likes', 'Remote API'],
    )
    def get(self, request_id, author_id, post_id, comment_id):
        """Get a list of likes on {comment_id} for {post_id} posted by {author_id}. Supports remote authors; to make proxied requests to an external server, provide the full ID of the external author URL encoded in place of {author_id}, whereas {post_id} and {comment_id} needs to remain the UUID/identifier only (non-url)."""

        if is_remote_url(author_id):
            remote_url = get_remote_url(author_id)
            remote = RemoteConnection(remote_url)

            # Group 6 does not use UUID's for their object IDs
            # Nor does Group 10
            # So we need to extract those specially
            if (author_id.startswith("https://cmput404-group6-instatonne.herokuapp.com/")):
                author_id = extract_id_if_url_group_6('author', author_id)
            elif (author_id.startswith("https://socialdistcmput404.herokuapp.com/")):
                author_id = extract_id_if_url_group_10('author', author_id)
            else:
                author_id = extract_uuid_if_url('author', author_id)

            try:
                response = remote.connection.get_comment_likes(
                    author_id, post_id, comment_id)
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

            except Exception as e:
                return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
            author_id = extract_uuid_if_url('author', author_id)
            post_id = extract_uuid_if_url('post', post_id)
            comment_id = extract_uuid_if_url('comment', comment_id)
            if not (author_id and post_id and comment_id):
                return Response(status=status.HTTP_404_NOT_FOUND)

            try:
                if not (Author.objects.filter(pk=author_id).exists() and Post.objects.filter(pk=post_id).exists() and Comment.objects.filter(pk=comment_id).exists()):
                    print(comment_id)
                    print(Author.objects.filter(pk=author_id).exists(), Post.objects.filter(
                        pk=post_id).exists(), Comment.objects.filter(pk=comment_id).exists())
                    return Response('Author, post, or comment id does not exist', status=status.HTTP_404_NOT_FOUND)
                # likes = Like.objects.filter(author___id=author_id, object__endswith=f'/posts/{post_id}/comments/{comment_id}')
                likes = Like.objects.filter(
                    object__endswith=f'authors/{author_id}/posts/{post_id}/comments/{comment_id}')
                serializer = LikesSerializer({'items': likes})
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Exception as e:
                traceback.print_exc()
                return Response(status=status.HTTP_404_NOT_FOUND)


class LikedPosts(APIView):

    @extend_schema(
        parameters=[docs.EXTEND_SCHEMA_PARAM_AUTHOR_ID],
        responses={
            200: docs.EXTEND_SCHEMA_RESP_LIKED_POSTS,
            404: OpenApiResponse(
                description="The author does not exist",
            ),
        },
        tags=['Posts', 'Remote API'],
    )
    def get(self, request, author_id):
        """Get a list of likes originating from this {author_id}. Supports remote authors; to make proxied requests to an external server, provide the full ID of the external author URL encoded in place of {author_id}."""

        if is_remote_url(author_id):
            remote_url = get_remote_url(author_id)
            remote = RemoteConnection(remote_url)

            # Group 6 does not use UUID's for their object IDs
            # Nor does Group 10
            # So we need to extract those specially
            if (author_id.startswith("https://cmput404-group6-instatonne.herokuapp.com/")):
                author_id = extract_id_if_url_group_6('author', author_id)
            elif (author_id.startswith("https://socialdistcmput404.herokuapp.com/")):
                author_id = extract_id_if_url_group_10('author', author_id)
            else:
                author_id = extract_uuid_if_url('author', author_id)

            try:
                response = remote.connection.get_author_liked(author_id)
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

            except Exception as e:
                return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            # Extract a uuid if id was given in the form http://somehost/authors/<uuid>
            author_id = extract_uuid_if_url('author', author_id)
            if not author_id:
                return Response(status=status.HTTP_404_NOT_FOUND)

            try:
                if not (Author.objects.filter(pk=author_id).exists()):
                    return Response('Author id does not exist', status=status.HTTP_404_NOT_FOUND)
                likes = Like.objects.filter(author___id=author_id)
                serializer = LikedSerializer({'items': likes})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                traceback.print_exc()
                return Response(status=status.HTTP_404_NOT_FOUND)


class InboxDetail(APIView):

    pagination_class = StandardResultsSetPagination

    @extend_schema(
        parameters=[docs.EXTEND_SCHEMA_PARAM_AUTHOR_ID,
                    docs.EXTEND_SCHEMA_PARAM_PAGE,
                    docs.EXTEND_SCHEMA_PARAM_SIZE],
        tags=['Inbox'],
        responses={
            200: docs.EXTEND_SCHEMA_RESP_INBOX,
            404: OpenApiResponse(
                description="The author does not exist",
            ),
        },
    )
    def get(self, request, author_id):
        """Get list of posts sent to {author_id}."""

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
            return Response('That author id does not exist', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        parameters=[docs.EXTEND_SCHEMA_PARAM_AUTHOR_ID],
        request=InboxPostSerializer,
        examples=[docs.EXTEND_SCHEMA_EXAMPLE_INBOX_SEND_POST, docs.EXTEND_SCHEMA_EXAMPLE_INBOX_SEND_FOLLOW,
                  docs.EXTEND_SCHEMA_EXAMPLE_INBOX_SEND_LIKE, docs.EXTEND_SCHEMA_EXAMPLE_INBOX_SEND_COMMENT],
        responses={
            200: OpenApiResponse(
                description="The item that was sent to author_id's inbox",
                examples=[docs.EXTEND_SCHEMA_EXAMPLE_INBOX_SEND_POST, docs.EXTEND_SCHEMA_EXAMPLE_INBOX_SEND_FOLLOW,
                          docs.EXTEND_SCHEMA_EXAMPLE_INBOX_SEND_LIKE, docs.EXTEND_SCHEMA_EXAMPLE_INBOX_SEND_COMMENT],
                response=OpenApiTypes.OBJECT,
            ),
            404: OpenApiResponse(
                description="The author does not exist",
            ),
        },
        tags=['Inbox', 'Remote API'],
    )
    def post(self, request, author_id):
        """Send a object to {author_id}. Supports sending posts, likes, follow requests, and comments. Supports remote authors; to make proxied requests to an external server, provide the full ID of the external author URL encoded in place of {author_id}."""

        if is_remote_url(author_id):
            remote_url = get_remote_url(author_id)
            remote = RemoteConnection(remote_url)
            
            # Group 6 does not use UUID's for their object IDs
            # Nor does Group 10
            # So we need to extract those specially
            if (author_id.startswith("https://cmput404-group6-instatonne.herokuapp.com/")):
                author_id = extract_id_if_url_group_6('author', author_id)
            elif (author_id.startswith("https://socialdistcmput404.herokuapp.com/")):
                author_id = extract_id_if_url_group_10('author', author_id)
            else:
                author_id = extract_uuid_if_url('author', author_id)

            object = request.data
            match object['type']:
                case 'post':
                    response = remote.connection.send_post(
                        author_id, request.data)

                    return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

                case 'follow':
                    response = remote.connection.send_follow(
                        author_id, request.data)

                    return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

                case 'like':
                    response = remote.connection.send_like(
                        author_id, request.data)

                    return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

                case 'comment':
                    response = remote.connection.send_comment(
                        author_id, request.data)

                    return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

        else:
            author_id = extract_uuid_if_url('author', author_id)
            if not author_id or author_id == '':
                return Response(status=status.HTTP_400_BAD_REQUEST)

            object = request.data
            match object['type']:
                case 'post':
                    serializer = InboxPostSerializer(data=object["object"])
                    if serializer.is_valid():
                        # Create post and post author if they don't exist (foreign case)
                        if Post.objects.filter(id=serializer.validated_data['id']).exists():
                            # Will only work for local posts
                            post = Post.objects.get(
                                id=serializer.validated_data['id'])
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
                    serializer = LikeRequestSerializer(data=object["object"])
                    if serializer.is_valid():
                        like = serializer.create(serializer.data)
                        return Response(LikeResponseSerializer(like).data, status=status.HTTP_201_CREATED)
                    else:
                        print(serializer.errors)
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                case 'comment':
                    serializer = CommentSerializer(data=object["object"])
                    if serializer.is_valid():
                        comment = serializer.create(serializer.data)
                        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
                    else:
                        print(serializer.errors)
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                case _:
                    return Response("Object type must be one of 'post', 'follow', 'like', or 'comment'", status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Inbox'],
        responses={
            200: None,
            404: OpenApiResponse(
                description="The author does not exist",
            ),
        },
    )
    def delete(self, request, author_id):
        """Clear {author_id}'s inbox"""

        author_id = extract_uuid_if_url('author', author_id)
        if not author_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            inbox = Inbox.objects.get(author___id=author_id)
            # Use clear() because we don't want to delete related posts, just remove the relation
            inbox.items.clear()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FollowRequests(APIView):

    @extend_schema(
        parameters=[
            docs.EXTEND_SCHEMA_PARAM_AUTHOR_ID,
        ],
        tags=['Followers'],
        responses={
            200: docs.EXTEND_SCHEMA_RESP_LIST_FOLLOWS,
            404: OpenApiResponse(
                description="The author does not exist",
            ),
        },
    )
    def get(self, request, author_id):
        """Get requests to follow {author_id}."""
        author_id = extract_uuid_if_url('author', author_id)
        if not author_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            if not Author.objects.filter(pk=author_id).exists():
                return Response('That author id does not exist', status=status.HTTP_404_NOT_FOUND)
            follows = Follow.objects.filter(object___id=author_id)
            serializer = FollowsSerializer({'items': follows})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteFollowRequest(APIView):

    @extend_schema(
        parameters=[
            docs.EXTEND_SCHEMA_PARAM_AUTHOR_ID,
        ],
        tags=['Followers'],
        responses={
            200: None,
            404: OpenApiResponse(
                description="The author does not exist",
            ),
        },
    )
    def delete(self, request, author_id, actor_id):
        """Delete requests to follow {author_id} from {actor_id}."""
        author_id = extract_uuid_if_url('author', author_id)
        if not author_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            if not Author.objects.filter(pk=author_id).exists():
                return Response('That author id does not exist', status=status.HTTP_404_NOT_FOUND)

            deleted = Follow.objects.filter(
                object_id=author_id, actor=actor_id).delete()
            if deleted[0] > 0:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

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
        },
        tags=['Auth'],
        responses={
            200: None
        },
    )
    def post(self, request):
        """Login a user with a username and password."""
        try:
            data = json.loads(request.body)
            user = authenticate(
                request, username=data['username'], password=data['password'])
            if user:
                login(request, user)
                user_author = Author.objects.get(displayName=user.username)
                auth_response = {
                    "username": user.username, "id": user_author._id}
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
        },
        tags=['Auth'],
        responses={
            200: None
        },
    )
    def post(self, request):
        """Register a new user, with a username and a password."""
        try:
            # create our user and an author, and link it with the author.
            serializer = UserSerializer(data=json.loads(request.body))
            if serializer.is_valid():
                user = serializer.data
                user = User.objects.create_user(
                    user['username'], password=user['password'])
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


class RemoteGetAllAuthors(APIView):
    @extend_schema(
        tags=['Authors', 'Remote API'],
        responses={
            200: docs.EXTEND_SCHEMA_RESP_LIST_AUTHORS
        },
    )
    def get(self, request, remote_url):
        """Extra endpoint to help proxy requests to remote servers to get all authors. For internal use only."""
        try:
            if is_remote_url(remote_url):
                formatted_remote_url = get_remote_url(remote_url)
                remote = RemoteConnection(formatted_remote_url)
                response = remote.connection.get_authors()
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# DON'T LOOK AT / USE THESE:
class RemoteSendToInbox(APIView):
    def post(self, request, remote_url):
        """Extra endpoint to help proxy requests to remote servers to send to inbox"""
        try:
            if is_remote_url(remote_url):
                formatted_remote_url = get_remote_url(remote_url)
                remote = RemoteConnection(formatted_remote_url)
                response = remote.connection.send_to_inbox(request.data)
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

            else:
                # TODO: return error message
                return Response(status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RemoteSendLike(APIView):
    def post(self, request, remote_url):
        """Extra endpoint to help proxy requests to remote servers to send like"""
        try:
            if is_remote_url(remote_url):
                formatted_remote_url = get_remote_url(remote_url)
                remote = RemoteConnection(formatted_remote_url)
                response = remote.connection.send_like(request.data)
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

            else:
                # TODO: return error message
                return Response(status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

