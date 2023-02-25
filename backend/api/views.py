from rest_framework import status, renderers
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import AuthorSerializer
from .models import Author

class Authors(APIView):

    def get(self, request, format=None):
        """
        Get all authors

        TODO: Query params, paging
        """
        try:
            authors = Author.objects.all()
            serializer = AuthorSerializer(authors, many=True)  # Must include many=True because it is a list of authors
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class AuthorDetail(APIView):

    def get(self, request, author_id):
        """
        Get details for an author
        """
        try:
            author = Author.objects.get(pk=author_id)
            serializer = AuthorSerializer(author)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, author_id):
        """
        Update details for an author
        TODO: This must only be useable as a 'local' user
        """
        try:
            serializer = AuthorSerializer(data=request.POST.dict())
            if serializer.is_valid():
                author, created = Author.objects.update_or_create(serializer.data)
                # Serialize and return the updated or created author
                serializer = AuthorSerializer(author)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class Followers(APIView):

    def get(self, request, author_id):
        """
        Get a list of authors following the user given by author_id
        """
        try:
            author = Author.objects.get(pk=author_id)
            followers = Author.objects.filter(pk__in=author.followers)
            serializer = AuthorSerializer(followers, many=True)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class FollowersDetail(APIView):

    def delete(self, request, author_id, foreign_author_id):
        """Remove foreign_author_id as a follower of author_id"""
        try:
            author = Author.objects.get(pk=author_id)
            if foreign_author_id in author.followers:
                author.followers.remove(foreign_author_id)
                author.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                # Return 404 if foreign_author_id does not exist in author_id's followers
                return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, author_id, foreign_author_id):
        """Add foreign_author_id as a follower of author_id"""
        try:
            author = Author.objects.get(pk=author_id)
            if foreign_author_id not in author.followers:
                author.followers.append(foreign_author_id)
                author.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, author_id, foreign_author_id):
        """Check if foreign_author_id is a follower of author_id"""
        try:
            author = Author.objects.get(pk=author_id)
            response = {'isFollower': bool(foreign_author_id in author.followers)}
            return Response(response, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class Posts(APIView):

    def get(self, request, author_id):
        """Get paginated list of posts by author_id, ordered by post date with most recent first"""
        pass

    def post(self, request, author_id):
        """Create a post (post object in body) for author_id, but generate the ID (compare to PUT in PostDetail)"""
        pass

class PostDetail(APIView):

    def get(self, request, author_id, post_id):
        """Get post_id posted by author_id"""
        pass

    def post(self, request, author_id, post_id):
        """Update post_id posted by author_id (post object in body)"""
        pass

    def delete(self, request, author_id, post_id):
        """Delete post_id posted by author_id"""
        pass

    def put(self, request, author_id, post_id):
        """Create a post (post object in body) for author_id with id post_id"""
        pass

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