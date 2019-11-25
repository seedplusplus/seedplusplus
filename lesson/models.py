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
    
#class CustomComment(BaseCommentAbstractModel):
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'),
                             #blank=True, null=True, related_name="%(class)s_comments",
                             #on_delete=models.SET_NULL)
    #user_name = models.CharField(_("user's name"), max_length=50, blank=True)
    #comment = models.TextField(_('comment'), max_length=COMMENT_MAX_LENGTH)
    #submit_date = models.DateTimeField(_('date/time submitted'), default=None, db_index=True)
    
    #class Meta:
            #abstract = True
            #ordering = ('submit_date',)
            #permissions = [("can_moderate", "Can moderate comments")]
            #verbose_name = _('comment')
            #verbose_name_plural = _('comments')    
            
    #def __str__(self):
        #return "%s: %s..." % (self.name, self.comment[:50])
            
    #def save(self, *args, **kwargs):
        #if self.submit_date is None:
            #self.submit_date = timezone.now()
        #super(CustomComment, self).save(*args, **kwargs) 
        
    #def _get_userinfo(self):
        #"""
        #Get a dictionary that pulls together information about the poster
        #safely for both authenticated and non-authenticated comments.
        #This dict will have ``name``, ``email``, and ``url`` fields.
        #"""
        #if not hasattr(self, "_userinfo"):
            #userinfo = {
                #"name": self.user_name,
                #"email": self.user_email,
                #"url": self.user_url
            #}
            #if self.user_id:
                #u = self.user
                #if u.email:
                    #userinfo["email"] = u.email

                ## If the user has a full name, use that for the user name.
                ## However, a given user_name overrides the raw user.username,
                ## so only use that if this comment has no associated name.
                #if u.get_full_name():
                    #userinfo["name"] = self.user.get_full_name()
                #elif not self.user_name:
                    #userinfo["name"] = u.get_username()
            #self._userinfo = userinfo
        #return self._userinfo

    #userinfo = property(_get_userinfo, doc=_get_userinfo.__doc__)
   
    #def _get_name(self):
        #return self.userinfo["name"]

    #def _set_name(self, val):
        #if self.user_id:
            #raise AttributeError(_("This comment was posted by an authenticated "
                                   #"user and thus the name is read-only."))
        #self.user_name = val

    #name = property(_get_name, _set_name, doc="The name of the user who posted this comment")    
        
    #def get_as_text(self):
        #"""
        #Return this comment as plain text.  Useful for emails.
        #"""
        #d = {
            #'user': self.user or self.name,
            #'date': self.submit_date,
            #'comment': self.comment,
            #'domain': self.site.domain,
            #'url': self.get_absolute_url()
        #}
        #return _('Posted by %(user)s at %(date)s\n\n%(comment)s\n\nhttp://%(domain)s%(url)s') % d 

#class Comment(UserCreatedObject):
    #body = models.TextField()
    #parent_comment = models.ForeignKey('Comment', related_name='children', on_delete=models.CASCADE)
    #score = models.IntegerField(default=0)
    #content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    #object_id=models.PositiveIntegerField()
    #content_object = GenericForeignKey()

# class Rating(models.Model):
#     owner = models.ForeignKey(User, on_delete=models.CASCADE)
#     obj = GenericForeignKey('content_type', 'object_id')
#     created_on = models.DateTimeField(auto_now_add=True)
#     last_modified = models.DateTimeField(auto_now=True)
#     score = models.PositiveSmallIntegerField(default=0)
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id=models.PositiveIntegerField()
#     content_object = GenericForeignKey()

#class CommentableObject(UserCreatedObject):
    #class Meta:
        #abstract = True

    #comments = GenericRelation(Comment, related_query_name='comments')
    #ratings = GenericRelation(Rating, related_query_name='ratings')
    #avg_rating = models.FloatField(default=0.0)

class Lesson(models.Model):
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

class Curriculum(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    lessons = models.ManyToManyField('Lesson', related_name='curricula')
    tags = TaggableManager()
    difficulty = models.SmallIntegerField(default=1) # 1 to 5
    description = models.TextField(null=True)
    length = models.FloatField(default=1) # Hours
    created_on = models.DateTimeField(auto_now_add=True)

#class Vote(models.Model):
    #owner = models.ForeignKey(User, on_delete=models.CASCADE)
    #comment = models.ForeignKey(CustomComment, on_delete=models.CASCADE)
    #value = models.SmallIntegerField(default=0)
