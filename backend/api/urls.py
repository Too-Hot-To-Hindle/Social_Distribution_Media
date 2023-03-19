from django.urls import include, path, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import views
from django.views.generic import TemplateView

# Regex pattern to extract uuids into a named argument that is passed to the view function
uuid_regex = r'[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}'
author_id_group = r'.*?(?P<author_id>' + uuid_regex + r')'
foreign_author_id_group = r'.*?(?P<foreign_author_id>' + uuid_regex + r')'
post_id_group = r'(?P<post_id>' + uuid_regex + r')'
comment_id_group = r'(?P<comment_id>' + uuid_regex + r')'

import re
print(r'^authors\/' + author_id_group)
print(r'^authors\/' + author_id_group + r'\/followers\/' + foreign_author_id_group + r'')
print(bool(re.match(r'^authors\/' + author_id_group, 'authors/d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc/followers/83ee4e3d-7f1f-4d43-8698-8adb60f2e9bd')))

urlpatterns = [
    path('authors', views.Authors.as_view()),

    # re_path(r'^authors\/' + author_id_group, views.AuthorDetail.as_view()),
    # re_path(r'^authors\/' + author_id_group + r'\/followers$', views.Followers.as_view()),
    # re_path(r'^authors\/' + author_id_group + r'\/followers\/' + foreign_author_id_group + r'', views.FollowersDetail.as_view()),
    # re_path(r'^authors\/' + author_id_group + r'\/posts$', views.Posts.as_view()),
    # re_path(r'^authors\/' + author_id_group + r'\/posts\/' + post_id_group + r'$', views.PostDetail.as_view()),
    # re_path(r'^authors\/' + author_id_group + r'\/posts\/' + post_id_group + r'\/image$', views.ImagePosts.as_view()),
    # re_path(r'^authors\/' + author_id_group + r'\/posts\/' + post_id_group + r'\/comments$', views.Comments.as_view()),
    # re_path(r'^authors\/' + author_id_group + r'\/posts\/' + post_id_group + r'\/likes$', views.PostLikes.as_view()),
    # re_path(r'^authors\/' + author_id_group + r'\/posts\/' + post_id_group + r'\/comments\/' + comment_id_group + r'\/likes$', views.CommentLikes.as_view()),
    # re_path(r'^authors\/' + author_id_group + r'\/liked$', views.LikedPosts.as_view()),
    # re_path(r'^authors\/' + author_id_group + r'\/inbox$', views.InboxDetail.as_view()),
    # re_path(r'^authors\/' + author_id_group + r'\/inbox\/followers$', views.FollowRequests.as_view()),

    path('authors/<str:author_id>', views.AuthorDetail.as_view()),
    path('authors/<str:author_id>/followers', views.Followers.as_view()),
    path('authors/<str:author_id>/followers/<str:foreign_author_id>', views.FollowersDetail.as_view()),
    path('authors/<author_id>/posts', views.Posts.as_view()),
    path('authors/<author_id>/posts/<post_id>', views.PostDetail.as_view()),
    path('authors/<author_id>/posts/<post_id>/image', views.ImagePosts.as_view()),
    path('authors/<author_id>/posts/<post_id>/comments', views.Comments.as_view()),
    path('authors/<author_id>/posts/<post_id>/likes', views.PostLikes.as_view()),
    path('authors/<author_id>/posts/<post_id>/comments/<comment_id>/likes', views.CommentLikes.as_view()),
    path('authors/<author_id>/liked', views.LikedPosts.as_view()),
    path('authors/<author_id>/inbox', views.InboxDetail.as_view()),
    path('authors/<author_id>/inbox/followers', views.FollowRequests.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('csrf/', views.Csrf.as_view()),
    path('auth', views.Auth.as_view()),
    path('auth/register', views.AuthRegister.as_view()),]