from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField
from .helpers import *
from django.db.models import Prefetch

class Registration(models.Model):
    name =  models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    profile_pic=models.ImageField( upload_to="profile" ,null=True , blank=True)
    
    def __str__(self):
        return self.name

class Blogmodel(models.Model):
    title = models.CharField(max_length=1000)
    author = models.CharField(max_length=1000)
    content = FroalaField()
    slug = models.SlugField(max_length=1000, null=True, blank=True)
    user = models.ForeignKey(Registration, blank=True, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog')
    created_at = models.DateTimeField(auto_now_add=True)
    upload_to = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    ratings = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.title


    

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        super(Blogmodel, self).save(*args, **kwargs)

class Rating(models.Model):
    username=models.ForeignKey(Registration,on_delete=models.SET_NULL,null=True)
    title=models.ForeignKey(Blogmodel,on_delete=models.CASCADE)
    rate = models.IntegerField()
    
    def _str_(self):
        return self.username.title
    
class Feedbacks(models.Model):
    blog = models.ForeignKey(Blogmodel, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return str(self.blog)

    
class drafts(models.Model):

   
    title = models.CharField(max_length=1000)
    author = models.CharField(max_length=1000)
    content = FroalaField()
    slug = models.SlugField(max_length=1000, null=True, blank=True)
    user = models.ForeignKey(Registration, blank=True, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    upload_to = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        super(drafts, self).save(*args, **kwargs)





