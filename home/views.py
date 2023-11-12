from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as authlogin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.

def home(request):
    # Post = Post.objects.all()
    post = Post.objects.all()
    return render(request, 'home.html',{'post':post})

def article(request, pk):
    post = get_object_or_404(Post, id=pk)
    comments = Comment.objects.filter(post=post)

    if request.method == "POST":
        content = request.POST.get('body')
        user = request.user  # This assumes the user is logged in

        Comment.objects.create(body=content, name=user, post=post)
        # Refresh the comments queryset after adding a new comment
        comments = Comment.objects.filter(post=post)
        return redirect('article', pk=pk)
    
    recommended_posts = Post.objects.exclude(id=pk).order_by('?')[:5]

    return render(request, 'article.html', {'post': post, 'comments': comments, 'recommended_posts': recommended_posts})

def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method == "POST":
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        subject = request.POST['subject']
        email = request.POST['email']
        message = request.POST['message']
        Contact.objects.create(firstName=fname,lastName=lname,subject=subject, email=email, message=message)
        messages.success(request, "Congratulations! Your Form has been submited.")
        return redirect(contact)
    return render(request,'contact.html')

def login_page(request):
    if request.method== "POST":
        data = request.POST.get
        username = data('username')
        password = data('password')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request, "User does'nt Exits!")
            return redirect(login_page)
        else:
            authlogin(request, user)
            return redirect(home)


        
    return render(request, 'login.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('password2')
        userimage = request.FILES.get('userimage')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.info(request, "Username or Email Already Exists!")
            return redirect('signup')  # Replace 'signup' with the correct URL name

        # Check if passwords match
        if pass1 != pass2:
            messages.info(request, "Passwords don't match!")
            return redirect('signup')  # Replace 'signup' with the correct URL name

        try:
            # Create User
            user = User.objects.create_user(username=username, email=email, password=pass1)

            # Create UserProfile with avatar
            UserProfile.objects.create(user=user, avatar=userimage)

            
            return redirect(login_page)  # Replace 'login_page' with the correct URL name

        except IntegrityError:
            messages.error(request, "Error creating user profile. Please try again.")
            return redirect('signup')  # Replace 'signup' with the correct URL name

    return render(request, 'signup.html')  # Replac

def logout_page(request):
    
    logout(request)
    return redirect(home)

def custom_404(request, exception):
    return render(request, '404.html', status=404)