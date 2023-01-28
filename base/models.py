from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Room(models.Model):
    host=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic=models.ForeignKey('Topic', on_delete=models.SET_NULL, null=True) #use the '' inside Topic only if topic is down in the code literally
    name=models.CharField(max_length=200)
    description=models.TextField(null=True, blank=True) #now null is allowed, by default it's false, i.e, null not allowed, Blank means form submitted can be empty
    participants=models.ManyToManyField(User, related_name='participants', blank=True)
    updated= models.DateTimeField(auto_now=True)    #takes a snapshot anytime this model.. or table was updated
    created= models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['-updated','-created'] #it somehow makes the new rooms in ascending order

    def __str__(self):
        return self.name

class Topic(models.Model):
    name=models.CharField(max_length=200)
    
    def __str__(self):
        return self.name


class Message(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    room=models.ForeignKey(Room, on_delete=models.CASCADE) #delete all messages in room if room is deleted # why no primary key it is refering to?
    body=models.TextField()
    updated= models.DateTimeField(auto_now=True)    #takes a snapshot anytime this model.. or table was updated
    created= models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return self.body[0:50] #first 50 characters     