from django.contrib import admin
from lesson.models import Lesson, Curriculum

class LessonAdmin(admin.ModelAdmin):
    pass

class CurriculumAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Lesson, LessonAdmin)
#admin.site.register(CustomComment, CommentAdmin)
admin.site.register(Curriculum, CurriculumAdmin)

