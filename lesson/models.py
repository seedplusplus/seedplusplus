from django.db import models
from django.conf import settings
from django_comments.abstracts import BaseCommentAbstractModel
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _
from django.views.generic import TemplateView, ListView
from taggit.managers import TaggableManager
from star_ratings.models import Rating

COMMENT_MAX_LENGTH = getattr(settings, 'COMMENT_MAX_LENGTH', 3000)


class UserCreatedObject(models.Model):
    class Meta:
        abstract = True

    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='images/', null=True)

class Comment(UserCreatedObject):
    body = models.TextField()
    parent_comment = models.ForeignKey('Comment', related_name='children', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object = GenericForeignKey()

#class Rating(models.Model):
    #owner = models.ForeignKey(User, on_delete=models.CASCADE)
    #obj = GenericForeignKey('content_type', 'object_id')
    #created_on = models.DateTimeField(auto_now_add=True)
    #last_modified = models.DateTimeField(auto_now=True)
    #score = models.PositiveSmallIntegerField(default=0)
    #content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    #object_id=models.PositiveIntegerField()
    #content_object = GenericForeignKey()

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
    tags = TaggableManager()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Curriculum(CommentableObject):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    lessons = models.ManyToManyField('Lesson', related_name='curricula')
    tags = TaggableManager()
    difficulty = models.SmallIntegerField(default=1) # 1 to 5
    description = models.TextField(null=True)
    length = models.FloatField(default=1) # Hours
    created_on = models.DateTimeField(auto_now_add=True)

class Vote(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    value = models.SmallIntegerField(default=0)
