from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Author, Post, Comment, Like, Follow, Inbox

class AuthorInline(admin.StackedInline):
    model = Author
    can_delete = False
    verbose_name_plural = 'authors'

class UserAdmin(BaseUserAdmin):
    inlines = (AuthorInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register your models here.
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(Inbox)