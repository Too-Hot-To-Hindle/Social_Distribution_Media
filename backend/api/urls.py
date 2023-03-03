from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('authors', views.Authors.as_view()),
    path('authors/<author_id>', views.AuthorDetail.as_view()),
    path('authors/<author_id>/followers', views.Followers.as_view()),
    path('authors/<author_id>/followers/<foreign_author_id>', views.FollowersDetail.as_view()),
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
    path('csrf/', views.Csrf.as_view()),
    path('auth', views.Auth.as_view()),
    path('auth/register', views.AuthRegister.as_view()),
]