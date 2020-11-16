from django.shortcuts import render, redirect
from .models import Post, Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# Add the following import
# from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

import uuid
import boto3

S3_BASE_URL = 'hhtps://s3-us-west-1.amazonaws.com/'
BUCKET =  'datura.metel'


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

class PostCreate(LoginRequiredMixin, CreateView):
  model = Post
  fields = '__all__'
  # success_url = '/'
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, UpdateView):
  model = Post
  # Let's disallow the renaming of a cat by excluding the name field!
  fields = '__all__'

class PostDelete(LoginRequiredMixin, DeleteView):
  model = Post
  success_url = '/'


def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('/')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

# def add_photo(request, post_id):
#   photo_file = request.FILES.get('photo-file', None)
#   if photo_file:
#       s3 = boto3.client('s3')
#       key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
#       try:
#         s3.upload_fileobj(photo_file, BUCKET, key)
#         url = f"{S_BASE_URL}{BUCKET}/{key}"
#         photo = Photo(url=url, post_id=post_id)
#         photo.save()
#       except:
#         print('An error occured uploading file to S3')
#   return redirect('detail', post_id=post_id)        

def add_photo(request, post_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, post_id=post_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', post_id=post_id)