from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, analyze_review_sentiments
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from datetime import datetime
import logging
import json
from .models import CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/djangoapp/')  # Redirect to the home page
    else:
        form = AuthenticationForm()
    
    return render(request, 'index.html', {'form': form})

def logout_request(request):
    logout(request)

    return redirect('/djangoapp/')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
        user.save()
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/djangoapp/')
    return render(request, 'djangoapp/registration.html')

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/ac844fdd-a8a1-4ac3-9754-64c371ab61d1/dealership-package/getalldealerships"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    car_models = CarModel.TYPE_CHOICES
    # Assuming all CarModels for the dealer have the same dealer name
    if car_models:
        dealer_name = car_models[0]
    else:
        dealer_name = "Dealer Name Not Found"  # You can customize this message

    reviews = get_dealer_reviews_from_cf(dealer_id)

    context = {
        'dealer_name': dealer_name,
        'reviews': reviews,
    }

    return render(request, 'your_template.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

