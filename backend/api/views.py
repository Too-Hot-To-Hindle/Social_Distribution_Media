from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from .serializers import AuthorSerializer
from .models import Author

class Authors(APIView):

    def get(self, request, format=None):
        """
        Get all authors

        TODO: Query params, paging
        """
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)  # Must include many=True because it is a list of authors
        return Response(serializer.data)

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