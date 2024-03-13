# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_list, name="blog_list"),
    path("create/", views.blog_create, name="blog_create"),
    path("<int:pk>/", views.blog_detail, name="blog_detail"),
    path("<int:pk>/edit/", views.blog_update, name="blog_update"),
    path("<int:pk>/delete/", views.blog_delete, name="blog_delete"),
    path("search/", views.blog_search, name="blog_search"),
    path("comment/<int:pk>/delete/", views.comment_delete, name="comment_delete"),
]
