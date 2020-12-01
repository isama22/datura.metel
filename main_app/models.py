from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=10000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
  # Add this method
    def get_absolute_url(self):
        return reverse('detail', kwargs={'post_id': self.id})

class Comment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  text = models.CharField(max_length=100)

  def __str__(self):
    return self.text

  def get_absolute_url(self):
    return reverse('detail', kwargs={'post_id': self.id}) 


class Photo(models.Model):
    url = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for post_id: {self.post_id} @{self.url}"        

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField(max_length=50, blank=True)
#     birth_date = models.DateField(null=True, blank=True)    

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()                