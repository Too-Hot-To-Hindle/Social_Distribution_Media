from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
import uuid

SERVICE_ADDRESS = "https://social-distribution-media.herokuapp.com"
PREFIX = 'api'
API_BASE = f"{SERVICE_ADDRESS}/{PREFIX}"

class Author(models.Model):

    type = 'author'

    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.URLField(blank=True, default=None, editable=False)
    url = models.URLField(blank=True, default=None, editable=False)
    host = models.URLField(default=SERVICE_ADDRESS, editable=False)
    displayName = models.CharField(max_length=100)
    github = models.URLField(blank=True)
    profileImage = models.URLField(blank=True)
    # https://stackoverflow.com/questions/35957837/trying-to-make-a-postgresql-field-with-a-list-of-foreign-keys-in-django
    # https://docs.djangoproject.com/en/4.1/ref/models/fields/#django.db.models.ManyToManyField.symmetrical
    # NOTE: Can't specify on_delete for this, but the default behaviour is CASCADE which is correct for us :)
    followers = models.ManyToManyField("self", symmetrical=False, blank=True)
    # store a default User object for leveraging Django's built-in auth
    user = models.OneToOneField(User, on_delete= models.CASCADE, blank=True)

    def __str__(self):
        return self.displayName
    
    def save(self, *args, **kwargs) -> None:
        # Set the id and url fields intially, using the generated id.
        if not self.id:
            self.id = f"{API_BASE}/authors/{self._id}"
        if not self.url:
            self.url = f"{SERVICE_ADDRESS}/authors/{self._id}"
        return super().save(*args, **kwargs)

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
    id = models.URLField(blank=True, default=None, editable=False)
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
        return f"Post by {Author.displayName}"
    
    def save(self, *args, **kwargs) -> None:
        # Set the id and url fields intially, using the generated id.
        if not self.id:
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
    id = models.URLField(blank=True, default=None, editable=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    contentType = models.TextField(choices=CONTENT_TYPES)
    published = models.DateTimeField(auto_now_add=True)  # Sets to timezone.now on first creation

    def __str__(self) -> str:
        return f"Comment by {Author.displayName}"
    
    def save(self, *args, **kwargs) -> None:
        # Set the id and url fields intially, using the generated id.
        if not self.id:
            self.id = f"{API_BASE}/authors/{self.author._id}/posts/{self._id}"
            self.comments = f"{self.id}/comments"
        return super().save(*args, **kwargs)

class Like(models.Model):

    type = 'Like'

    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    summary = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    # These 3 properties let us define the object foreign key model generically
    # NOTE: It is recomended to define indexes for the generic foreign key fields
    # https://docs.djangoproject.com/en/4.1/ref/models/options/#django.db.models.Options.indexes
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    object = GenericForeignKey('content_type', 'object_id')

    def __str__(self) -> str:
        return f"Like by {Author.displayName}"
    
class FriendRequest(models.Model):

    type = 'request'

    from_author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='friend_request_from')
    to_author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='friend_request_to')

    def __str__(self) -> str:
        return f"Friend request from {self.from_author.displayName} to {self.to_author.displayName}"

class Follow(models.Model):

    type = 'follow'

    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fromAuthor = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Friend request from {self.fromAuthor.displayName}"

class Inbox(models.Model):

    type = 'inbox'
    
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    # These 3 properties let us define the object foreign key model generically
    # NOTE: It is recomended to define indexes for the generic foreign key fields
    # https://docs.djangoproject.com/en/4.1/ref/models/options/#django.db.models.Options.indexes
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.UUIDField()
    # items = GenericForeignKey('content_type', 'object_id')

    items = GenericRelation('InboxObject', content_type_field='object_content_type', object_id_field='object_id')

    def __str__(self) -> str:
        return f"{self.author.displayName}'s Inbox"

class InboxObject(models.Model):

    object_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    object = GenericForeignKey('object_content_type', 'object_id')

    def __str__(self) -> str:
        return "Inbox Items Object"