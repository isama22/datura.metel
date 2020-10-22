from django.db import models
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name
    
  # Add this method
    def get_absolute_url(self):
        return reverse('detail', kwargs={'post_id': self.id})