from django.contrib import admin
from .models import Entry, Skill, Tag, Media

# Register your models here.
admin.site.register(Entry)
admin.site.register(Skill)
admin.site.register(Tag)
admin.site.register(Media)
