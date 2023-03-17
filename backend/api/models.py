from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
import uuid
import re

SERVICE_ADDRESS = "https://social-distribution-media.herokuapp.com"
PREFIX = 'api'
API_BASE = f"{SERVICE_ADDRESS}/{PREFIX}"

def extract_author_uuid(id: str):
    regex = r'.*authors\/([0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}).*'
    search = re.search(regex, id)
    if search:
        return search.group(1)
    return ''
def extract_post_uuid(id: str):
    regex = r'.*posts\/([0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}).*'
    search = re.search(regex, id)
    if search:
        return search.group(1)
    return ''

class Author(models.Model):

    type = 'author'

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
            _id = extract_author_uuid(self.id)
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
            _id = extract_post_uuid(self.id)
            self._id = _id
        elif first_save:
            self.id = f"{API_BASE}/authors/{self.author._id}/posts/{self._id}"
            self.comments = f"{self.id}/comments"
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
    _post_author_id = models.UUIDField(blank=True)
    _post_id = models.UUIDField(blank=True)
    
    id = models.URLField(blank=True, default=None, editable=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True)
    comment = models.TextField()
    contentType = models.TextField(choices=CONTENT_TYPES)
    published = models.DateTimeField(auto_now_add=True)  # Sets to timezone.now on first creation

    def __str__(self) -> str:
        return f"Comment by {Author.displayName}"
    
    def save(self, *args, **kwargs) -> None:
        # Set the id and url fields intially, using the generated id.
        if not self.id:
            self.id = f"{API_BASE}/authors/{self._post_author_id}/posts/{self._post_id}/comments/{self._id}"

        return super().save(*args, **kwargs)

class Like(models.Model):

    type = 'Like'

    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    summary = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    object = models.URLField()

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
    """
    List of IPs that are allowed access to remote endpoints
    """
    ip = models.GenericIPAddressField(blank=True, null=True, editable=False)
    host = models.CharField(blank=True, max_length=200)
    detail = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.host}"
    
class AllowedLocalNode(models.Model):
    """
    List of IPs that are allowed access to local endpoints
    """
    ip = models.GenericIPAddressField(blank=True, null=True, editable=False)
    host = models.CharField(blank=True, max_length=200)
    detail = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.host}"
    
class RemoteNodeRequest(models.Model):
    """
    List of requests to be added as an allowed remote node
    """
    ip = models.GenericIPAddressField(blank=True, null=True)
    meta = models.TextField(blank=True, null=True)
    name = models.TextField()
    discord = models.TextField()
    group = models.TextField()
    host = models.TextField()

    def __str__(self) -> str:
        return f"Request from {self.ip}"