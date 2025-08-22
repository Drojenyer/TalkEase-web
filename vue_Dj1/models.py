from importlib.metadata import requires

from django.db import models

# Create your models here.
class UserLike(models.Model):
    likes = models.CharField(verbose_name='likes', max_length=10)


class User(models.Model):
    user_name = models.CharField(verbose_name='user_name', max_length=10)
    user_password = models.CharField(verbose_name='user_pwd', max_length=10)
    gender = models.CharField(verbose_name='user_gender', null=True, blank=True, max_length=6)
    preference = models.ForeignKey(to=UserLike, verbose_name='preference', on_delete=models.CASCADE, null=True, blank=True)
    focus = models.JSONField(null=True, blank=True, default=list)
    profile = models.CharField(null=True, blank=True, max_length=100)
    portrait = models.ImageField(upload_to='user_media', null=True, blank=True)



class Admin(models.Model):
    admin_name = models.CharField(verbose_name='admin_name', max_length=10)
    admin_password = models.CharField(verbose_name='admin_pwd', max_length=10)


class Content(models.Model):
    title = models.CharField(verbose_name='title', max_length=50)
    publisher = models.CharField(verbose_name='publisher', max_length=10)
    detail = models.CharField(verbose_name='detail', max_length=10000)
    sort = models.CharField(max_length=5, null=True, blank=True)
    date = models.CharField(verbose_name='date', max_length=20)
    views = models.SmallIntegerField(verbose_name='views')
    images = models.ImageField(upload_to='media', null=True, blank=True)
