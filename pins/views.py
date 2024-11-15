from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from .models import Pin, UserProfile  # Import your models here
import os
from .forms import PinForm 

def home(request):
    """Displays all pins on the homepage."""
    pins = Pin.objects.all()
    return render(request, 'home.html', {'pins': pins})

def register(request):
    """Handles user registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    """Handles user login."""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    """Logs the user out."""
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    """Displays the profile of the logged-in user."""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'user_profile': user_profile})

@login_required
def my_posts(request):
    """Displays only the posts uploaded by the logged-in user."""
    pins = Pin.objects.filter(user=request.user)
    return render(request, 'my_posts.html', {'pins': pins})

@login_required
def upload_pin(request):
    """Handles uploading new pins using PinForm."""
    if request.method == 'POST':
        form = PinForm(request.POST, request.FILES)
        if form.is_valid():
            pin = form.save(commit=False)
            pin.user = request.user  # Associate the pin with the current user
            pin.save()
            return redirect('home')
    else:
        form = PinForm()

    return render(request, 'upload_pin.html', {'form': form})


@login_required
def like_pin(request, pin_id):
    """Handles liking a pin."""
    pin = get_object_or_404(Pin, id=pin_id)
    pin.likes += 1
    pin.save()
    return redirect('home')

@login_required
def download_pin(request, pin_id):
    """Allows the user to download the image associated with a pin."""
    pin = get_object_or_404(Pin, id=pin_id)
    file_path = os.path.join(settings.MEDIA_ROOT, pin.image.name)
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="image/jpeg")
        response['Content-Disposition'] = f'attachment; filename="{pin.image.name}"'
        return response

@login_required
def delete_pin(request, pin_id):
    """Handles deleting a pin uploaded by the current user."""
    pin = get_object_or_404(Pin, id=pin_id, user=request.user)
    
    if request.method == 'POST':
        # Delete the image file from the file system
        if pin.image:
            image_path = os.path.join(settings.MEDIA_ROOT, pin.image.name)
            if os.path.exists(image_path):
                os.remove(image_path)
                
        pin.delete()
        return redirect('my_posts')  # Redirect to the page displaying the user's posts

    return redirect('my_posts')
