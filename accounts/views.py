from django.shortcuts import render
from django.views.generic import CreateView, ListView #, UpdateView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponseRedirect, HttpResponse
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

# def user_update_view(request, slug):
#     # dictionary for initial data with
#     # field names as keys
#     context ={}
#
#     # fetch the object related to passed id
#     obj = get_object_or_404(get_user_model(), username = slug)
#
#     # pass the object as instance in form
#     form = forms.UserUpdateForm(request.POST or None, instance = obj)
#
#     # save the data from the form and
#     # redirect to detail_view
#     if form.is_valid():
#         form.save()
#         return HttpResponseRedirect('/accounts/')
#     # else:
#     #     return HttpResponse("form is not validated")
#
#     # add form dictionary to context
#     context['form'] = form
#
#     return render(request, 'accounts/user_form.html', context)


# class UserUpdateView(UpdateView):
#     model = get_user_model()
#     form_class = forms.UserUpdateForm
#     # template_name = 'accounts/user_form.html'
#     slug_field = 'username'
#
#     def get_success_url(self):
#         return '/accounts/'
