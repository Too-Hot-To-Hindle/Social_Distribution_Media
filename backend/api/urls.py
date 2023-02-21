from django.urls import include, path
from rest_framework import routers
from . import views

# router = routers.DefaultRouter()
# router.register(r'authors', views.AuthorViewSet)

urlpatterns = [
    path('authors/', views.Authors.as_view()),
    path('authors/<author_id>/', views.AuthorDetail.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]