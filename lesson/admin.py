from django.contrib import admin
from lesson.models import Lesson, Tag

class LessonAdmin(admin.ModelAdmin):
    pass

class TagAdmin(admin.ModelAdmin):
    pass

admin.site.register(Lesson, LessonAdmin)
admin.site.register(Tag, TagAdmin)