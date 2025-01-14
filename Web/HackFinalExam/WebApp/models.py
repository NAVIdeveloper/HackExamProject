from django.db import models

# Create your models here.

class Question(models.Model):
    text = models.TextField(null=True,blank=True)
    answer = models.TextField(null=True,blank=True)
    message_id = models.CharField(max_length=255,null=True,blank=True)
    is_answered = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now=True)
    
class Info(models.Model):
    telegram_group = models.CharField(max_length=255,null=True,blank=True)
    no_group = models.BooleanField(default=True)
