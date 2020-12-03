from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=10000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date']
  # Add this method
    def get_absolute_url(self):
        return reverse('detail', kwargs={'post_id': self.id})

# class Comment(models.Model):
#   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
#   post = models.ForeignKey(Post, on_delete=models.CASCADE)
#   text = models.CharField(max_length=100)
#   created_date = models.DateTimeField(default=timezone.now)

#   def __str__(self):
#     return self.text

#   def get_absolute_url(self):
#     return reverse('detail', kwargs={'post_id': self.id}) 
class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

class Photo(models.Model):
    url = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for post_id: {self.post_id} @{self.url}"