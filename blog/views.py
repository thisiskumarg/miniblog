from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, PostForm
from .models import Post
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

# Create your views here.

# Home Page
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})

# About Page
def about(request):
    return render(request, 'blog/about.html')

# Contact Page
def contact(request):
    return render(request, 'blog/contact.html')

# Dashboard Page
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request, 'blog/dashboard.html', {'posts': posts, 'full_name': full_name, 'groups': gps})
    else:
        return redirect('/login')

# Signup Page
def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
            messages.success(request, 'Congratulations! You have an Author.')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})

# Login Page
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in Successfully.')
                    return redirect('/dashboard')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})
    else:
        return redirect('/dashboard')

# Add Post Page
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            post_form = PostForm(request.POST)
            if post_form.is_valid():
                title = post_form.cleaned_data['title']
                desc = post_form.cleaned_data['desc']
                pst = Post(title=title, desc=desc)
                pst.save()
                messages.success(request, 'Post added Successfully!')
                return redirect('/dashboard')
        else:
            post_form = PostForm()
        return render(request, 'blog/addpost.html', {'form': post_form})
    else:
        return redirect('/login')

# Update Post Page
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk = id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request, 'Post updated Successfully!')
                return redirect('/dashboard')
        else:
            pi = Post.objects.get(pk = id)
            form = PostForm(instance=pi)
        return render(request, 'blog/updatepost.html', {'form': form})
    else:
        return redirect('/login')

# Delete Post Page
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk = id)
            pi.delete()
            messages.success(request, 'Post deleted Successfully!')
        return redirect('/dashboard')
    else:
        return redirect('/login')

# Logout
def user_logout(request):
    logout(request)
    return redirect('/')
