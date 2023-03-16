from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Author, Post, Comment, Like, Follow, Inbox, RemoteNodeRequest


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'id')

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("_id", 'type', 'id', 'host', 'displayName', 'url', 'github', 'profileImage', 'followers', 'following')

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("_id", 'type', 'id', 'title', 'source', 'origin', 'description', 'contentType', 'content', 'author', 'categories', 'count', 'comments', 'commentsSrc', 'published', 'visibility', 'unlisted')
        depth = 1

class InboxPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("_id", 'type', 'id', 'title', 'source', 'origin', 'description', 'contentType', 'content', 'author', 'categories', 'count', 'comments', 'commentsSrc', 'published', 'visibility', 'unlisted')
        depth = 1
        extra_kwargs = {
            '_id': {
                'validators': []
            }
        }

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

    actor = AuthorSerializer()
    object = AuthorSerializer()

    class Meta:
        model = Follow
        fields = ('type', 'summary', 'actor', 'object')
        depth = 1
    
    def create(self, validated_data):
        actor_data = validated_data.pop('actor')
        object_data = validated_data.pop('object')
        actor = Author.objects.get(**actor_data)
        object = Author.objects.get(**object_data)
        return Follow.objects.create(actor=actor, object=object, **validated_data)

class InboxSerializer(serializers.ModelSerializer):

    class Meta:
        model = Inbox
        fields = ('type', 'author', 'items')
        depth = 1
    
class RemoteNodeRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = RemoteNodeRequest
        fields = ('name', 'discord', 'group', 'host')