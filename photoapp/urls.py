from django.urls import path
from .views import (
    photo_list_view,
    # PhotoListView,
    # PhotoTagListView,
    # PhotoPeopleListView,
    PhotoDetailView,
    PhotoCreateView,
    PhotoUpdateView,
    PhotoDeleteView
)

app_name = 'photo'

urlpatterns = [
    path('', photo_list_view, name='list'),
    # path('people/<slug:tag>/', PhotoPeopleListView.as_view(), name='people'),
    # path('tag/<slug:tag>/', PhotoTagListView.as_view(), name='tag'),
    path('photo/<int:pk>/', PhotoDetailView.as_view(), name='detail'),
    path('photo/create/', PhotoCreateView.as_view(), name='create'),
    path('photo/<int:pk>/update/', PhotoUpdateView.as_view(), name='update'),
    path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name='delete'),
]
