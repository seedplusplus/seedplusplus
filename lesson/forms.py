from django import forms
from lesson.models import Lesson,Curriculum
from .models import *

DIFFICULTY_CHOICES = [
    (1, "Never programmed"),
    (2, "Novice programmer"),
    (3, "Some experience required"),
    (4, "Advanced"),
    (5, "Expert")
]


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
        
class ProfPicForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic']