from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
import uuid
import re

import uuid
from uuid import UUID

UUIDV5_SECRET = uuid.UUID("49a5e3fc-1753-4934-806c-114a7956fbe9")

def is_valid_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID.
    
     Parameters
    ----------
    uuid_to_test : str
    version : {1, 2, 3, 4}
    
     Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.
    
     Examples
    --------
    >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
    True
    >>> is_valid_uuid('c9bf9e58')
    False
    """
    
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test

from .utils import extract_uuid

SERVICE_ADDRESS = "https://social-distribution-media.herokuapp.com/api"
PREFIX = 'api'
API_BASE = f"{SERVICE_ADDRESS}"

class Author(models.Model):

    type = models.CharField(max_length=15, default='author')

    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.URLField(blank=True, default=None)
    url = models.URLField(blank=True, default=None)
    host = models.URLField(default=SERVICE_ADDRESS)
    displayName = models.CharField(max_length=100)
    github = models.URLField(blank=True)
    profileImage = models.URLField(blank=True)
    followers = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="author_followers")
    following = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="author_following")
    user = models.OneToOneField(User, on_delete= models.CASCADE, blank=True, null=True)
    remote = models.BooleanField(default=False)

    def __str__(self):
        return self.displayName
    
    def save(self, *args, **kwargs) -> None:
        # Store if this is the first or not
        first_save = self._state.adding

        # Set the id and url fields intially, using the generated id.
        ## TODO: CONTINUE UPDATING THIS
        if not self.host:
            self.host = SERVICE_ADDRESS
        
        # If an author is created with an id, make sure _id matches
        if self.id and first_save:
            _id = extract_uuid('authors', self.id)

            if not _id:
                _id = str(uuid.uuid5(UUIDV5_SECRET, self.id))

            self._id = _id

        elif first_save:
            self.id = f"{self.host}/authors/{self._id}"
        
        if not self.url:
            self.url = f"{self.host}/authors/{self._id}"
        super().save(*args, **kwargs)

        # Create inbox on Author creation
        if first_save and not self.remote:
            Inbox.objects.create(author_id=self._id)

class Post(models.Model):

    PUBLIC = 'PUBLIC'
    FRIENDS = 'FRIENDS'

    MARKDOWN = 'text/markdown'
    PLAINTEXT = 'text/plain'
    BASE64 = 'application/base64'
    BASE64_PNG = 'image/png;base64'
    BASE64_JPEG = 'image/jpeg;base64'
    BASE64_JPG = 'image/jpg;base64'

    VISIBILITY_CHOICES = [
        (PUBLIC, 'Public'),
        (FRIENDS, 'Friends')
    ]

    CONTENT_TYPES = [
        (MARKDOWN, 'Common mark'),
        (PLAINTEXT, 'UTF-8 plain text'),
        (BASE64, 'Base 64 string'),
        (BASE64_PNG, 'Base 64 string of PNG image'),
        (BASE64_JPEG, 'Base 64 string of JPEG image'),
        (BASE64_JPG, 'Base 64 string of JPG image')
    ]

    type = 'post'

    _id = models.UUIDField(primary_key=True, default=uuid.uuid4)  # Editable for the PUT endpoint
    id = models.URLField(blank=True, default=None)
    title = models.TextField()
    source = models.URLField(blank=True)  # Need to clarify source and origin fields
    origin = models.URLField(blank=True)
    description = models.TextField(blank=True)
    contentType = models.TextField(choices=CONTENT_TYPES, default=PLAINTEXT)
    content = models.TextField(blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True)
    categories = models.JSONField(default=list, null=False, blank=True)
    count = models.IntegerField(default=0, editable=False)
    comments = models.URLField(blank=True)
    commentsSrc = models.JSONField(default=dict, null=False, blank=True)
    published = models.DateTimeField(auto_now_add=True)  # Sets to timezone.now on first creation
    visibility = models.TextField(choices=VISIBILITY_CHOICES, default=FRIENDS)
    unlisted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Post by {self.author.displayName}"
    
    def save(self, *args, **kwargs) -> None:

        # Store if this is the first or not
        first_save = self._state.adding

        # Set the id and url fields intially, using the generated id.
        if self.id and first_save:
            _id = extract_uuid('posts', self.id)
            self._id = _id
        elif first_save:
            self.id = f"{SERVICE_ADDRESS}/authors/{self.author._id}/posts/{self._id}"
            self.comments = f"{self.id}/comments"

            # when creating a new post on our own server, we need to set the source and origin
            # double check w/ TA if this is correct
            self.source = f"{SERVICE_ADDRESS}/authors/{self.author._id}/posts/{self._id}"
            self.origin = f"{SERVICE_ADDRESS}/authors/{self.author._id}/posts/{self._id}"
        return super().save(*args, **kwargs)

class Comment(models.Model):

    MARKDOWN = 'text/markdown'
    PLAINTEXT = 'text/plain'

    CONTENT_TYPES = [
        (MARKDOWN, 'Common mark'),
        (PLAINTEXT, 'UTF-8 plain text'),
    ]
    
    type = "comment"

    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    _post_author_id = models.UUIDField(blank=True, null=True)
    _post_id = models.UUIDField(blank=True, null=True)
    
    id = models.URLField(blank=True, default=None, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True)
    comment = models.TextField()
    contentType = models.TextField(choices=CONTENT_TYPES)
    published = models.DateTimeField(auto_now_add=True)  # Sets to timezone.now on first creation

    def save(self, *args, **kwargs) -> None:

        if self._state.adding:
            self._id = extract_uuid('comments', self.id)

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Comment by {Author.displayName}"
    
class Like(models.Model):

    type = 'Like'

    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    summary = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    object = models.URLField()
    context = "https://www.w3.org/ns/activitystreams"

    def __str__(self) -> str:
        return f"Like by {self.author.displayName}"

class Follow(models.Model):

    type = 'follow'

    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    summary = models.TextField()
    actor = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='follow_request_from')
    object = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='follow_request_to')

    def __str__(self) -> str:
        return f"Follow request from {self.actor.displayName} to {self.object.displayName}"
    
    class Meta:
        verbose_name_plural = 'Follow Requests'
    
# class Followers(models.Model):

#     type = 'followers'

#     author = models.ForeignKey(Author, on_delete=models.CASCADE)
#     items = models.ManyToManyField(Author, blank=True)

class Inbox(models.Model):

    type = 'inbox'
    
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    items = models.ManyToManyField(Post, blank=True)

    def __str__(self) -> str:
        return f"{self.author.displayName}'s Inbox"
    
    class Meta:
        verbose_name_plural = 'Inboxes'

class AllowedRemoteNode(models.Model):

    pass