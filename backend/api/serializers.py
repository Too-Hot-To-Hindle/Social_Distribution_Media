from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Author, Post


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'id')

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("_id", 'type', 'id', 'host', 'displayName', 'url', 'github', 'profileImage', 'followers')

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("_id", 'type', 'id', 'title', 'source', 'origin', 'description', 'contentType', 'content', 'author', 'categories', 'count', 'comments', 'commentsSrc', 'published', 'visibility', 'unlisted')