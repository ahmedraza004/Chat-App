from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

class ChatRoom(models.Model):
    participants = models.ManyToManyField(User ,related_name='chatrooms' )
    name = models.CharField(max_length=30 ,null=True,blank=True)
    is_group = models.BooleanField(default=False)

    def check_group_status(self):
        if self.participants.count() > 2:
            self.is_group = True
            self.save(update_fields=['is_group'])


    def __str__(self):
      return self.name if self.name else f"ChatRoom #{self.id}"

class Messages(models.Model):
    room = models.ForeignKey(ChatRoom,on_delete=models.CASCADE, related_name='messages',null=True,blank=True)
    sender = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
      sender_name = self.sender.username if self.sender else "Unknown"
      if self.message:
          preview = self.message[:20] + "..." if len(self.message) > 20 else self.message
      else:
          preview = "No message"
      return f"{sender_name} : {preview}"


