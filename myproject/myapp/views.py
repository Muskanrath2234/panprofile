# Import Statements
import re
from datetime import datetime
from PIL import Image
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import pytesseract
from .forms import CreateUserForm, ImageUploadForm
from .models import Profile

# Configuration for Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


# Helper Function to Extract Information from Image
def extract_information(image):
    text = pytesseract.image_to_string(image)
    date_pattern = re.compile(r'\b\d{2}/\d{2}/\d{4}\b')
    pan_num_pattern = re.compile(r'Permanent Account Number Card\n.+')
    name_pattern = re.compile(r'Name\n.+')
    father_pattern = re.compile(r"Father's Name\n.+")

    date_match = re.search(date_pattern, text)
    pan_match = re.search(pan_num_pattern, text)
    name_match = re.search(name_pattern, text)
    father_match = re.search(father_pattern, text)

    date = date_match.group(0) if date_match else None
    pan = pan_match.group(0).split('\n')[-1].strip() if pan_match else None
    name = name_match.group(0).split('\n')[-1].strip() if name_match else None
    father_name = father_match.group(0).split('\n')[-1].strip() if father_match else None

    return date, pan, name, father_name


# View Functions
def upload_pan(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = Image.open(request.FILES['image'])
            date, pan, name, father_name = extract_information(image)

            if date and pan and name and father_name:
                dob = datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d')
                user_profile, created = Profile.objects.get_or_create(user=request.user)
                user_profile.name = name
                user_profile.DOB = dob
                user_profile.Pan = pan
                user_profile.father_Name = father_name
                user_profile.save()

            return render(request, 'result.html', {'date': date, 'pan': pan, 'name': name, 'father_name': father_name})
    else:
        form = ImageUploadForm()
    return render(request, 'upload_image.html', {'form': form})


def result(request):
    return render(request, 'result.html')


def register_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CreateUserForm()
    return render(request, 'register_page.html', {'form': form})


def index(request):
    return render(request, "home.html")


def Profile_1(request):
    return render(request, "profile.html")


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, f'Welcome back, {username}! You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return redirect('login')

    return render(request, 'login_page.html')




def user_pan(request):
    # Retrieve the profile of the currently logged-in user
    user_profile = Profile.objects.get(user=request.user)

    # Render the template with the profile information
    return render(request, 'user_pan.html', {'user': request.user, 'profile': user_profile})

def all_pan(request):
    profiles = Profile.objects.all()
    return render(request, 'all_pan.html', {'profiles': profiles})


def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')