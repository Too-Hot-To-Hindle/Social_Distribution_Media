from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Author, Post, Comment, Like, Follow, Inbox


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'id')

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('type', 'id', 'host', 'displayName', 'url', 'github', 'profileImage', 'followers', 'following')

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('type', 'id', 'title', 'source', 'origin', 'description', 'contentType', 'content', 'author', 'categories', 'count', 'comments', 'commentsSrc', 'published', 'visibility', 'unlisted')

class CommentSerializer(serializers.ModelSerializer):

    author = AuthorSerializer()

    class Meta:
        model = Comment
        fields = ('type', 'id', 'author', 'comment', 'contentType', 'published', '_post_author_id', '_post_id')

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        # Below means that comments by authors that do not exist will fail
        author = Author.objects.get(**author_data)
        return Comment.objects.create(author=author, **validated_data)

class LikeSerializer(serializers.ModelSerializer):

    author = AuthorSerializer()

    class Meta:
        model = Like
        fields = ('type', 'summary', 'author', 'object')
        depth = 1

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        # Below means that likes by authors that do not exist will fail
        author = Author.objects.get(**author_data)
        return Like.objects.create(author=author, **validated_data)

class FollowSerializer(serializers.ModelSerializer):

    fromAuthor = AuthorSerializer()
    toAuthor = AuthorSerializer()

    class Meta:
        model = Follow
        fields = ('type', 'summary', 'actor', 'object')
        depth = 1
    
    def create(self, validated_data):
        from_author_data = validated_data.pop('actor')
        to_author_data = validated_data.pop('object')
        from_author = Author.objects.get(**from_author_data)
        to_author = Author.objects.get(**to_author_data)
        return Follow.objects.create(fromAuthor=from_author, toAuthor=to_author, **validated_data)

class InboxSerializer(serializers.ModelSerializer):

    class Meta:
        model = Inbox
        fields = ('type', 'author', 'items')
        depth = 1