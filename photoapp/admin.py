from django.contrib import admin
from .models import Photo, Year, GenericTag, PeopleTag

admin.site.register(Photo)
admin.site.register(Year)
admin.site.register(GenericTag)
admin.site.register(PeopleTag)
