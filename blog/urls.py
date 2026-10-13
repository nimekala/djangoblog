from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("my-posts/", views.my_posts, name="my_posts"),
    path("post/new/", views.post_create, name="post_create"),
    path("post/<slug:slug>/edit/", views.post_edit, name="post_edit"),
    path("post/<slug:slug>/delete/", views.post_delete, name="post_delete"),
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
    path("categories/", views.category_list, name="category_list"),
    path("category/<int:pk>/", views.category_posts, name="category_posts"),
]