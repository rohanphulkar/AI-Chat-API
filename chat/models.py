from django.db import models
import uuid
from accounts.models import User

class Chat(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=255,blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Chat"
        verbose_name_plural = "Chats"

class ChatItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE)
    input = models.TextField()
    output = models.TextField(blank=True)

    def __str__(self):
        return self.chat.name