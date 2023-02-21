from rest_framework import serializers
from .models import Author

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('type', 'id', 'host', 'display_name', 'url', 'github', 'profile_image')