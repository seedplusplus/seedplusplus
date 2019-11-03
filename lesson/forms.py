from django import forms
from lesson.models import Lesson,Curriculum

DIFFICULTY_CHOICES = [
    (1, "Never programmed"),
    (2, "Novice programmer"),
    (3, "Some experience required"),
    (4, "Advanced"),
    (5, "Expert")
]


# class LessonForm(forms.Form):
#     title = forms.CharField(label = "Title", max_length=255)
#     description = forms.CharField(label="Description", widget=forms.Textarea)
#     body = forms.CharField(label="body", widget=forms.Textarea)
#     difficulty = forms.MultipleChoiceField(
#         label="Difficulty",
#         widget = forms.RadioSelect,
#         choices = DIFFICULTY_CHOICES,
#     )
#     language = forms.CharField(label="Language")
#     length = forms.FloatField(label = "Length (hours)")
#     tags = forms.ModelMultipleChoiceField

class LessonForm(forms.ModelForm):
    difficulty = forms.ChoiceField(
        label="Difficulty",
        widget=forms.RadioSelect,
        choices=DIFFICULTY_CHOICES,
    )

    length = forms.FloatField(label="Length (hours)")

    class Meta:
        model = Lesson
        fields = ['title',
                  'description',
                  'body',
                  'difficulty',
                  'language',
                  'length']


class CurriculumForm(forms.ModelForm):
    difficulty = forms.ChoiceField(
        label="Difficulty",
        widget=forms.RadioSelect,
        choices=DIFFICULTY_CHOICES,
    )

    length = forms.FloatField(label="Length (hours)")

    class Meta:
        model = Curriculum
        widgets = {'lessons': forms.CheckboxSelectMultiple(),}
        fields = ['title',
                  'description',
                  'lessons',
                  'difficulty',
                  'length']