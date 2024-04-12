from django.contrib import admin

from .models import ScormAsset, ScormResponse

admin.site.register(ScormAsset)
admin.site.register(ScormResponse)