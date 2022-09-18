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
from .models import Photo, GenericTag, PeopleTag, Year, Comment
from .forms import AddPhotoForm, CommentForm

@login_required
def photo_list_view(request):
    if request.GET.get('sort_by') == 'createdasc':
        sort = 'created'
    elif request.GET.get('sort_by') == 'yearasc':
        sort = 'year'
    elif request.GET.get('sort_by') == 'yeardesc':
        sort = '-year'
    else:
        sort = '-created'
    photos = photo_list = Photo.objects.all().order_by(sort)
    tags = GenericTag.objects.all().order_by('name')
    people = PeopleTag.objects.all().order_by('name')
    year = Year.objects.all().order_by('year')
    search = ''
    search_m = ''
    if request.GET.get('tag'):
        lookups = Q(tags__name__exact=request.GET.get('tag'))
        search = request.GET.get('tag')
        search_m = 'tag'
    elif request.GET.get('year'):
        lookups = Q(year__year__exact=request.GET.get('year'))
        search = request.GET.get('year')
        search_m = 'year'
    elif request.GET.get('person'):
        lookups = Q(people__name__exact=request.GET.get('person'))
        search = request.GET.get('person')
        search_m = 'person'
    elif request.GET.get('search'):
        search = request.GET.get('search')
        lookups = Q(title__icontains=search) | Q(tags__name__icontains=search) | Q(people__name__icontains=search) | Q(year__year__icontains=search)
        search_m = 'search'
    message = 'PhotoSmith Photos'

    if search != '' and search is not None:
        photos = photo_list.filter(lookups).distinct()
        message = search + ' Photos'
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
        'search':search,
        'search_m':search_m,
        'sort':request.GET.get('sort_by'),
    }
    return render(request, 'photoapp/list.html', context)

class PhotoDetailView(LoginRequiredMixin, DetailView):
    model = Photo
    template_name = 'photoapp/detail.html'
    context_object_name = 'photo'
#
# @login_required
# def photo_create_view(request):
#     form = AddPhotoForm()
#     if request.method == 'POST':
#         image = request.FILES['image']
#         thumbnail = request.FILES['image']
#         title = request.POST.get('title')
#         description = request.POST.get('description')
#         year_id = request.POST.get('year')
#         people = request.POST.get('people')
#         tags = request.POST.getlist('tags')
#         photo = Photo(image=image, thumbnail=thumbnail, title=title, description=description, year_id=year_id,
#         people=people, tags=tags, submitter=request.user,)
#         photo.save()
#         return redirect('/photo/?page=1')
#     return render(request, 'photoapp/create.html', context={'form':form})

class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ['image', 'title', 'description', 'year', 'people', 'tags']
    template_name = 'photoapp/create.html'
    success_url = '/photo/?page=1'
    extra_context = {'tags':GenericTag.objects.all().order_by('name'),'people':PeopleTag.objects.all().order_by('name'),}

    def form_valid(self, form):
        form.instance.thumbnail = self.request.FILES['image']
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

class PhotoUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'photoapp/update.html'
    model = Photo
    fields = ['title', 'description', 'year', 'people', 'tags']
    success_url = '/photo/?page=1'

class PhotoDeleteView(UserIsSubmitter, DeleteView):
    template_name = 'photoapp/delete.html'
    model = Photo
    success_url = '/photo/?page=1'

@login_required
def add_comment_to_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.submitter = request.user
            comment = form.save(commit=False)

            comment.photo = photo
            comment.save()
            return redirect('photo:detail', pk=photo.pk)
    else:
        form = CommentForm()
    return render(request, 'photoapp/comment.html', {'form':form})

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    photo_pk = comment.photo.pk
    comment.delete()
    return redirect('photo:detail', pk=photo_pk)
