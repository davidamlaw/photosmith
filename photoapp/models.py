from django.db import models
from django.contrib.auth import get_user_model
# from django_resized import ResizedImageField
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase
from PIL import Image, ExifTags
from io import BytesIO
from django.core.files import File

class Year(models.Model):
    year = models.CharField(max_length=5, unique=True)

    class Meta:
         ordering = ['year']

    def __str__(self):
        return self.year

class GenericTag(TagBase):

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    # ... methods (if any) here

class PeopleTag(TagBase):

    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("People")

    # ... methods (if any) here

class TaggedGeneric(GenericTaggedItemBase):
    tag = models.ForeignKey(
        GenericTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )

class TaggedPeople(GenericTaggedItemBase):
    tag = models.ForeignKey(
        PeopleTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )

class Photo(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='photos/%Y%m')
    thumbnail = models.ImageField(blank=True, upload_to='thumbnails/%Y%m')
    submitter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    year = models.ForeignKey(Year, blank=True, on_delete=models.CASCADE)
    people = TaggableManager(through=TaggedPeople, verbose_name='People')
    tags = TaggableManager(through=TaggedGeneric, verbose_name='Tags')

    def save(self, *args, **kwargs):
        try:
            this = Photo.objects.get(id=self.id)
            if this.thumbnail != self.thumbnail:
                self.thumbnail.delete(save=False)
            return super().save(*args, **kwargs)
        except:
            if self.thumbnail:
                img = Image.open(BytesIO(self.thumbnail.read()))

                if hasattr(img, '_getexif'):
                    exif = img._getexif()
                    if exif:
                        for tag, label in ExifTags.TAGS.items():
                            if label == 'Orientation':
                                orientation = tag
                                break
                        if orientation in exif:
                            if exif[orientation] == 3:
                                img = img.rotate(180, expand=True)
                            elif exif[orientation] == 6:
                                img = img.rotate(270, expand=True)
                            elif exif[orientation] == 8:
                                img = img.rotate(90, expand=True)

                img.thumbnail((360,360), Image.ANTIALIAS)
                output = BytesIO()
                img.save(output, format='JPEG', quality=95)
                output.seek(0)
                self.thumbnail = File(output, self.thumbnail.name)

            return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    photo = models.ForeignKey(Photo, related_name='comments', on_delete=models.CASCADE)
    submitter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.photo.title
