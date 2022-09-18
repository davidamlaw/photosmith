from django.urls import path
from .views import (
    photo_list_view,
    # photo_create_view,
    PhotoDetailView,
    PhotoCreateView,
    PhotoUpdateView,
    PhotoDeleteView,
    add_comment_to_photo,
    delete_comment,
)

app_name = 'photo'

urlpatterns = [
    path('', photo_list_view, name='list'),
    path('<int:pk>/', PhotoDetailView.as_view(), name='detail'),
    path('create/', PhotoCreateView.as_view(), name='create'),
    path('<int:pk>/update/', PhotoUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', PhotoDeleteView.as_view(), name='delete'),
    path('<int:pk>/comment/', add_comment_to_photo, name='add_comment_to_photo'),
    path('<int:pk>/delete_comment/', delete_comment, name='delete_comment'),
]
