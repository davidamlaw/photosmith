from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_one, name='register_one'),
    path('register/photoappuser/', views.SignUp.as_view(), name='register')
    # path('', views.UserListView.as_view(), name='user_list'),
    # path('<slug:slug>', views.user_update_view, name='user_form'),
]
