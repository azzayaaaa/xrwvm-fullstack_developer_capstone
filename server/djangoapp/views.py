import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CarModel
from .populate import initiate
from .restapis import analyze_review_sentiments, get_request, post_review


@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    data = {'userName': username}
    if user is not None:
        login(request, user)
        data = {
            'userName': username,
            'firstName': user.first_name,
            'lastName': user.last_name,
            'status': 'Authenticated',
        }
    return JsonResponse(data)


def logout_request(request):
    logout(request)
    return JsonResponse({'userName': '', 'status': 200})


@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data.get('firstName', '')
    last_name = data.get('lastName', '')
    email = data.get('email', '')

    if User.objects.filter(username=username).exists():
        return JsonResponse({'userName': username, 'error': 'Already Registered'})

    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email,
    )
    login(request, user)
    return JsonResponse({'userName': username, 'status': 'Authenticated'})


def get_dealerships(request, state='All'):
    endpoint = '/fetchDealers' if state == 'All' else f'/fetchDealers/{state}'
    dealerships = get_request(endpoint)
    return JsonResponse({'status': 200, 'dealers': dealerships})


def fetch_dealerships(request, state='All'):
    return get_dealerships(request, state)


def get_dealer_reviews(request, dealer_id):
    reviews = get_request(f'/fetchReviews/dealer/{dealer_id}')
    for review in reviews:
        if 'sentiment' not in review:
            sentiment = analyze_review_sentiments(review.get('review', ''))
            review['sentiment'] = sentiment.get('sentiment', 'neutral')
    return JsonResponse({'status': 200, 'reviews': reviews})


def analyze_review(request, text):
    text = text.replace('+', ' ')
    return JsonResponse(analyze_review_sentiments(text))


def get_dealer_details(request, dealer_id):
    dealer = get_request(f'/fetchDealer/{dealer_id}')
    return JsonResponse({'status': 200, 'dealer': dealer})


def fetch_dealer_details(request, dealer_id):
    return get_dealer_details(request, dealer_id)


def get_cars(request):
    if not CarModel.objects.exists():
        initiate()
    cars = [
        {
            'CarMake': car.car_make.name,
            'CarModel': car.name,
        }
        for car in CarModel.objects.select_related('car_make').all()[:15]
    ]
    return JsonResponse({'status': 200, 'CarModels': cars})


@csrf_exempt
def add_review(request):
    data = json.loads(request.body)
    saved_review = post_review(data)
    return JsonResponse({'status': 200, 'review': saved_review})
