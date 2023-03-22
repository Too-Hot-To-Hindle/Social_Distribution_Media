from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Author, Post, Comment, Like, Follow, Inbox

from pprint import pprint

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'id')

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("_id", 'type', 'id', 'host', 'displayName', 'url', 'github', 'profileImage', 'followers', 'following')

class AuthorsSerializer(serializers.Serializer):

    type = serializers.SerializerMethodField()
    items = AuthorSerializer(many=True)

    def get_type(self, obj):
        return 'authors'

class FollowersSerializer(serializers.Serializer):

    type = serializers.SerializerMethodField()
    items = AuthorSerializer(many=True)

    def get_type(self, obj):
        return 'followers'

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("_id", 'type', 'id', 'title', 'source', 'origin', 'description', 'contentType', 'content', 'author', 'categories', 'count', 'comments', 'commentsSrc', 'published', 'visibility', 'unlisted')
        depth = 1

class InboxPostSerializer(serializers.ModelSerializer):

    author = AuthorSerializer()

    class Meta:
        model = Post
        fields = ("_id", 'type', 'id', 'title', 'source', 'origin', 'description', 'contentType', 'content', 'author', 'categories', 'count', 'comments', 'commentsSrc', 'published', 'visibility', 'unlisted')
        depth = 1
        extra_kwargs = {
            '_id': {
                'validators': []
            }
        }
    
    def create(self, validated_data):
        author_data = validated_data.pop('author')
        # Retrieve or create the author of this like
        if Author.objects.filter(id=author_data['id']).exists():
            author = Author.objects.get(id=author_data['id'])
        else:
            author = Author.objects.create(**author_data, remote=True)  # If creating here it is a remote user
        return Post.objects.create(author=author, **validated_data)

class CommentSerializer(serializers.ModelSerializer):

    author = AuthorSerializer()

    class Meta:
        model = Comment
        fields = ('type', 'id', 'author', 'comment', 'contentType', 'published')

    def create(self, validated_data):
        print(validated_data)
        author_data = validated_data.pop('author')
        print('in create')
        # Below means that comments by authors that do not exist will fail
        if Author.objects.filter(id=author_data['id']).exists():
            print('exists')
            author = Author.objects.get(id=author_data['id'])
        else:
            print('does not exist')
            author = Author.objects.create(**author_data, remote=True)  # If creating here it is a remote user
        pprint(validated_data)
        return Comment.objects.create(author=author, **validated_data)

class LikeRequestSerializer(serializers.ModelSerializer):

    author = AuthorSerializer()
    # context = serializers.CharField(source="@context")

    class Meta:
        model = Like
        fields = ('type', 'summary', 'author', 'object')
        optional_fields = ['context', ]
        depth = 1

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        # Retrieve or create the author of this like
        if Author.objects.filter(id=author_data['id']).exists():
            author = Author.objects.get(id=author_data['id'])
        else:
            author = Author.objects.create(**author_data, remote=True)  # If creating here it is a remote user
        return Like.objects.create(author=author, **validated_data)

class LikeResponseSerializer(serializers.ModelSerializer):

    author = AuthorSerializer()

    class Meta:
        model = Like
        fields = ('type', 'summary', 'author', 'object', 'context')
        depth = 1

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        # Retrieve or create the author of this like
        if Author.objects.filter(id=author_data['id']).exists():
            author = Author.objects.get(id=author_data['id'])
        else:
            author = Author.objects.create(**author_data, remote=True)  # If creating here it is a remote user
        return Like.objects.create(author=author, **validated_data)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['@context'] = data.pop('context', '')
        return data

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
        # Create actor object if they don't exist (remote follow case)
        if Author.objects.filter(id=actor_data['id']).exists():
            actor = Author.objects.get(id=actor_data['id'])
        else:
            actor = Author.objects.create(**actor_data, remote=True)  # If creating here it is a remote user
        object = Author.objects.get(**object_data)
        return Follow.objects.create(actor=actor, object=object, **validated_data)

class InboxSerializer(serializers.ModelSerializer):

    class Meta:
        model = Inbox
        fields = ('type', 'author', 'items')
        depth = 1