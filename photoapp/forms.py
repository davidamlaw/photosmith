from django.forms import ModelForm
from .models import Photo, Comment, Favorite

class AddPhotoForm(ModelForm):

    class Meta:
        model = Photo
        fields = ('year',)

class CommentForm(ModelForm):

    class Meta():
        model = Comment
        fields = ('text',)

class FavoriteForm(ModelForm):

    class Meta():
        model = Favorite
        fields = ('user', 'favorite',)
