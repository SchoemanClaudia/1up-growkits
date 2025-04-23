from django.contrib import admin
from .models import GrowGuide


class GrowGuideAdmin(admin.ModelAdmin):
    list_display = ('guide_title', 'step_no', 'instructions', 'image')


admin.site.register(GrowGuide, GrowGuideAdmin)
