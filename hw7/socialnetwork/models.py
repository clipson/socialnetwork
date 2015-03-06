from django.db import models
from datetime import datetime

# User class for built-in authentication module
from django.contrib.auth.models import User

class Post(models.Model):
    text = models.CharField(max_length=160)
    user = models.ForeignKey(User)
    date_created = models.DateTimeField(default=datetime.now, blank=True)
    date_modified = models.DateTimeField(default=datetime.now, blank=True)

    def save(self):
        if self.date_created == None:
            self.date_created = datetime.now()
        self.date_modified = datetime.now()
        super(Post, self).save()

    def __unicode__(self):
        return self.text

class Comment(models.Model):
    text = models.CharField(max_length=160)
    date_created = models.DateTimeField(default=datetime.now, blank=True)
    date_modified = models.DateTimeField(default=datetime.now, blank=True)
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)

    def save(self):
        if self.date_created == None:
            self.date_created = datetime.now()
        self.date_modified = datetime.now()
        super(Comment, self).save()

    def __unicode__(self):
        return self.text

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    age = models.IntegerField(max_length=3, blank=True, null=True)
    bio = models.TextField(max_length=430,  blank=True, null=True)
    picture = models.FileField(upload_to="pictures", blank=True, null=True)
    content_type = models.CharField(max_length=50, blank=True, null=True)
    picture_url = models.CharField(blank=True, max_length=256)

    def __unicode__(self):
        return 'UserProfile(id=' + str(self.id) + ')'

    def save(self):
        super(UserProfile, self).save()

class Relationship(models.Model):
    follower = models.ForeignKey(User, related_name="user_follower")
    followed = models.ForeignKey(User, related_name="user_followed")

    def __unicode__(self):
        return 'Relationship(id=' + str(self.id) + ' follower=' + str(self.follower)+' followed='+str(self.followed) + ')'

    def save(self, **kwargs):
        super(Relationship, self).save()
