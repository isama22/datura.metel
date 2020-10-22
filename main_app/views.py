from django.shortcuts import render
from .models import Post

# Add the following import
# from django.http import HttpResponse

# Define the home view
# def home(request):
#   return HttpResponse('<h1>Hello /ᐠ｡‸｡ᐟ\ﾉ</h1>')
def home(request):
  posts = Post.objects.all()
  return render(request, 'home.html', {'posts': posts}) 

def posts_detail(request, post_id):
  post = Post.objects.get(id=post_id)
  return render(request, 'posts/detail.html', { 'post': post })

def about(request):
  return render(request, 'about.html')  

def post(request):
  return render(request, 'post.html')  

