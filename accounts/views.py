from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.db.models import Q
from . import forms
from .models import TempPassword
from photoapp.models import Photo
from django.template.defaulttags import register

class SignUp(CreateView):
    form_class = forms.SignUpForm
    success_url = '/'
    template_name = 'accounts/register.html'

@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)

def member_list_view(request):
    members = get_user_model().objects.order_by('first_name')
    photos = Photo.objects.all()
    member_photos = {}
    for member in members:
        x = member.id
        lookups = Q(submitter_id__exact=member.id)
        count = Photo.objects.filter(lookups)
        member_photos[x] = len(count)

    context = {'members':members, 'member_photos':member_photos,}

    return render(request, 'accounts/member_list.html', context)


def register_one(request):
    password = request.POST.get('password')
    passwords = TempPassword.objects.all()
    for pwd in passwords:
        if pwd.password == password:
            return redirect('/accounts/register/photoappuser/')
    return render(request, 'accounts/registerone.html')
