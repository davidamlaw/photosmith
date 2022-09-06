from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import Photo, GenericTag, PeopleTag, Year

@login_required
def photo_list_view(request):
    photos = photo_list = Photo.objects.all().order_by('-created')
    tags = GenericTag.objects.all().order_by('name')
    people = PeopleTag.objects.all().order_by('name')
    year = Year.objects.all().order_by('year')
    search = request.GET.get('search')
    message = 'PhotoSmith Photos'
    lookups = Q(title__icontains=search) | Q(tags__name__icontains=search) | Q(people__name__icontains=search) | Q(year__year__icontains=search) | Q(description__icontains=search)
    if search != '' and search is not None:
        photos = photo_list.filter(lookups).distinct()
        message = search.title() + ' Photos'
    paginator = Paginator(photos, 24)
    if request.GET.get('page') != '':
        page_number = request.GET.get('page')
    else:
        page_number = 1
    photos = paginator.get_page(page_number)
    photos.adjusted_elided_pages = paginator.get_elided_page_range(page_number)
    context = {
        'message':message,
        'photos':photos,
        'tags':tags,
        'people':people,
        'year':year,
    }
    return render(request, 'photoapp/list.html', context)

# class PhotoListView(ListView):
#     model = Photo
#     template_name = 'photoapp/list.html'
#     context_object_name = 'photos'
#
# class PhotoTagListView(PhotoListView):
#     template_name = 'photoapp/taglist.html'
#
#     def get_tag(self):
#         return self.kwargs.get('tag')
#
#     def get_queryset(self):
#         return self.model.objects.filter(tags__slug=self.get_tag())
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["tag"] = self.get_tag()
#         context["year"] = Year.objects.all().order_by('year')
#         context["tags"] = GenericTag.objects.all().order_by('name')
#         context["people"] = PeopleTag.objects.all().order_by('name')
#         return context
#
# class PhotoPeopleListView(PhotoListView):
#     template_name = 'photoapp/taglist.html'
#
#     def get_tag(self):
#         return self.kwargs.get('tag')
#
#     def get_queryset(self):
#         return self.model.objects.filter(tags__slug=self.get_tag())
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["people"] = self.get_tag()
#         context["tags"] = GenericTag.objects.all().order_by('name')
#         context["people"] = PeopleTag.objects.all().order_by('name')
#         return context

class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'photoapp/detail.html'
    context_object_name = 'photo'

class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ['image', 'title', 'description', 'year', 'people', 'tags']
    template_name = 'photoapp/create.html'
    success_url = '/photo/?page=1'

    def form_valid(self, form):
        form.instance.submitter = self.request.user
        return super().form_valid(form)

class UserIsSubmitter(UserPassesTestMixin):

    def get_photo(self):
        return get_object_or_404(Photo, pk=self.kwargs.get('pk'))

    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user == self.get_photo().submitter
        else:
            raise PermissionDenied('Sorry you are not allowed here')

class PhotoUpdateView(UserIsSubmitter, UpdateView):
    template_name = 'photoapp/update.html'
    model = Photo
    fields = ['title', 'description', 'year', 'people', 'tags']
    success_url = '/photo/?page=1'

class PhotoDeleteView(UserIsSubmitter, DeleteView):
    template_name = 'photoapp/delete.html'
    model = Photo
    success_url = '/photo/?page=1'
