from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase

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
    image = models.ImageField(upload_to='photos/')
    submitter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    year = models.ForeignKey(Year, blank=True, on_delete=models.CASCADE)
    people = TaggableManager(through=TaggedPeople, verbose_name='People')
    tags = TaggableManager(through=TaggedGeneric, verbose_name='Tags')

    def __str__(self):
        return self.title
