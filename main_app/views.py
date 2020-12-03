from django.shortcuts import render, redirect
from .models import Post, Photo, Comment
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import CommentForm
# Add the following import
# from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import SingleObjectMixin

import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'datura.metel'


# Define the home view
# def home(request):
#   return HttpResponse('<h1>Hello /ᐠ｡‸｡ᐟ\ﾉ</h1>')
def home(request):
  posts = Post.objects.all()
  return render(request, 'home.html', {'posts': posts}) 

def posts_detail(request, post_id):
  post = Post.objects.get(id=post_id)
  # return render(request, 'posts/detail.html', { 'post': post })
  comment_form = CommentForm()
  return render(request, 'posts/detail.html', { 'post': post, 'comment_form': comment_form })

@login_required
def add_comment(request, post_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    form.instance.user = request.user
    new_comment = form.save(commit=False)
    new_comment.post_id = post_id
    new_comment.save()
  return redirect('detail', post_id=post_id)

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




# class ProfileObjectMixin(SingleObjectMixin):
#     """
#     Provides views with the current user's profile.
#     """
#     model = Profile

#     def get_object(self):
#         """Return's the current users profile."""
#         try:
#             return self.request.user.get_profile()
#         except Profile.DoesNotExist:
#             raise NotImplemented(
#                 "What if the user doesn't have an associated profile?")

#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         """Ensures that only authenticated users can access the view."""
#         klass = ProfileObjectMixin
#         return super(klass, self).dispatch(request, *args, **kwargs)


# class ProfileUpdateView(ProfileObjectMixin, UpdateView):
#     """
#     A view that displays a form for editing a user's profile.

#     Uses a form dynamically created for the `Profile` model and
#     the default model's update template.
#     """
#     pass  # That's All Folks!

# def profile(request):
#   return render(request, 'profile.html')  


# @login_required
# def add_comment(request, post_id):
#   form = CommentForm(request.POST)
#   if form.is_valid():
#     form.instance.user = request.user
#     new_comment = form.save(commit=False)
#     new_comment.post_id = post_id
#     new_comment.save()
#   return redirect('detail', post_id=post_id)

# def add_comment(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.save()
#             return redirect('detail', pk=post.pk)
#     else:
#         form = CommentForm()
#     return render(request, '/add_comment.html', {'form': form})