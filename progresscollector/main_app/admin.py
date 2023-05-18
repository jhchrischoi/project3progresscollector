from django.contrib import admin

# Register your models here.
from .models import Progress, Checklist, Recommendation, Photo

admin.site.register(Progress)
admin.site.register(Checklist)
admin.site.register(Recommendation)
admin.site.register(Photo)