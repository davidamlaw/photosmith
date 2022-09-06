from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from . import forms
from .models import TempPassword

class SignUp(CreateView):
    form_class = forms.SignUpForm
    success_url = '/'
    template_name = 'accounts/register.html'

class UserListView(ListView):
    model = get_user_model()
    template_name = 'accounts/user_list.html'

    def get_queryset(self):
        return get_user_model().objects.order_by('username')

def register_one(request):
    password = request.POST.get('password')
    passwords = TempPassword.objects.all()
    for pwd in passwords:
        if pwd.password == password:
            return redirect('/accounts/register/photoappuser/')
    return render(request, 'accounts/registerone.html')
