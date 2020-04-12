from django.contrib import admin
from tinymce.widgets import TinyMCE
from django.db import models
from .models import Tutorial, TutorialSeries, TutorialCategory

class TutorialAdmin(admin.ModelAdmin):
    # fields = ["tutorial_title",
    #           "tutorial_published",
    #           "tutorial_content"
    # ]

    fieldsets = [
        ("Title/Date", {"fields": ["tutorial_title", "tutorial_published"]}),
        ("URL", {"fields": ["tutorial_slug"]}),
        ("Series", {"fields": ["tutorial_series"]}),
        ("Content", {"fields": ["tutorial_content"]}),
    ]

    # overrides the TextField to give a full editor using the TinyMCE app
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()}
    }


admin.site.register(TutorialSeries)
admin.site.register(TutorialCategory)

# Register your models here.
admin.site.register(Tutorial, TutorialAdmin)
