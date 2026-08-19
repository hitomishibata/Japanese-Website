from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:blog_id>/", views.content, name="content"),
    path("category/<str:tag>/", views.category, name="category"),

]