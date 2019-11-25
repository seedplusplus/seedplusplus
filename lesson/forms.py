from django import forms
from django_comments.forms import CommentForm
from lesson.models import Lesson,Curriculum#,CustomComment
from .models import *
from django.utils.translation import gettext as _

DIFFICULTY_CHOICES = [
    (1, "Never programmed"),
    (2, "Novice programmer"),
    (3, "Some experience required"),
    (4, "Advanced"),
    (5, "Expert")
]

COMMENT_MAX_LENGTH = getattr(settings, 'COMMENT_MAX_LENGTH', 3000)

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
        
#class CustomCommentForm(CommentForm):
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'),
                             #blank=True, null=True, related_name="%(class)s_comments",
                             #on_delete=models.SET_NULL)
    #user_name = models.CharField(_("user's name"), max_length=50, blank=True)
    #comment = models.TextField(_('comment'), max_length=COMMENT_MAX_LENGTH)
    #submit_date = models.DateTimeField(_('date/time submitted'), default=None, db_index=True)
    
    #def get_comment_create_data(self):
            ## Use the data of the superclass, and add in the title field
            #data = super(CustomComment, self).get_comment_create_data()
            #data['user'] = self.cleaned_data['user']
            #data['user_name'] = self.cleaned_data['user_name']
            #data['comment'] = self.cleaned_data['comment']
            #data['submit_date'] = self.cleaned_data['submit_date']
            #return data    
        
    #def get_comment_model(self):
        #return CustomComment
        
class CustomCommentForm(CommentForm):
    def __init__(self,*args, **kwargs):
        super(CustomCommentForm, self).__init__(*args, **kwargs)
        self.fields["email"].required = False