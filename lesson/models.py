from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.views.generic import TemplateView, ListView


class Tag(models.Model):
    name = models.CharField(max_length=50)


class UserCreatedObject(models.Model):
    class Meta:
        abstract = True

    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class Comment(UserCreatedObject):
    body = models.TextField()
    parent_comment = models.ForeignKey('Comment', related_name='children', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object = GenericForeignKey()



class Rating(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    obj = GenericForeignKey('content_type', 'object_id')
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    score = models.PositiveSmallIntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object = GenericForeignKey()



class CommentableObject(UserCreatedObject):
    class Meta:
        abstract = True

    comments = GenericRelation(Comment, related_query_name='comments')
    ratings = GenericRelation(Rating, related_query_name='ratings')
    avg_rating = models.FloatField(default=0.0)


class Lesson(CommentableObject):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    body = models.TextField(null=True)
    difficulty = models.SmallIntegerField(default=1) # 1 to 5
    language = models.CharField(max_length=30)
    length = models.FloatField(default=1) # Hours
    tags = models.ManyToManyField('Tag', related_name='lessons')

    def __str__(self):
        return self.title


class Curriculum(CommentableObject):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    lessons = models.ManyToManyField('Lesson', related_name='curricula')
    difficulty = models.SmallIntegerField(default=1) # 1 to 5
    description = models.TextField(null=True)
    length = models.FloatField(default=1) # Hours
    tags = models.ManyToManyField('Tag', related_name='curricula')

class Vote(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    value = models.SmallIntegerField(default=0)

class SearchResultsView(ListView):
    model = Lesson
    template_name = 'search_results.html'