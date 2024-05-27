from django.urls import path
from . import views

urlpatterns = [
    path("/", views.BlogPostListCreate.as_view(), name="blogpost-view-create"),
    path(
        "/<int:pk>/",
        views.BlogPostRetrieveUpdateDestory.as_view(),
        name="update",
    ),
]
