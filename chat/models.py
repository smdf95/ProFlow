from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse # Change here
from django.utils import timezone
from PIL import Image, ExifTags



# Create your models here.
class Chat(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField('auth.User', related_name='chats')
    messages = models.ManyToManyField('ChatMessage', related_name='chat_related')
    image = models.ImageField(default='default_chat.png', upload_to='chat_images')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_created')
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=True)


    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('chat-detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path) # Open image

        if hasattr(img, '_getexif') and img._getexif() is not None:
            exif = dict(img._getexif().items())
            if 0x0112 in exif:
                orientation = exif[0x0112]
                if orientation == 3:
                    img = img.rotate(180, expand=True)
                elif orientation == 6:
                    img = img.rotate(270, expand=True)
                elif orientation == 8:
                    img = img.rotate(90, expand=True)

        # resize image
        if img.height > 600 or img.width > 600:
            output_size = (600, 600)
            img.thumbnail(output_size) # Resize image
            
        img.save(self.image.path)

class ChatMessage(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    chat = models.ManyToManyField('Chat', related_name='messages_related')

    def get_absolute_url(self):
        return reverse('chat-detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        # Call the superclass save() method
        super().save(*args, **kwargs)
        
        for chat in self.chat.all():  # Loop through all related chats
            chat.last_updated = timezone.now()
            chat.save(update_fields=['last_updated'])