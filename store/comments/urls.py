from django.urls import path

from . import views

app_name = 'comments'

urlpatterns = [
    path('create/<int:product_id>/', views.CommentCreateView.as_view(), name='create'),
    path('like/<int:comment_id>/<str:reaction>/', views.comment_like, name='like'),
]
