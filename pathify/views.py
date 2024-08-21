from django.shortcuts import render
import json
from django.db import IntegrityError
from databaseApp.models import *
from django.http import JsonResponse
#from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required #decorator that can be used for some views functions


#helper endpoint
def is_authenticated(request):
    return JsonResponse({'is_authenticated': request.user.is_authenticated})

def logout_view(request):
    logout(request)
    return JsonResponse({'message':'logout successful'})

def index(request):
    return render(request, 'index.html')

#@csrf_exempt  # Temporarily disabling CSRF for testing; add proper CSRF handling later.

def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        usernameInput = data.get('username')
        passwordInput = data.get('password')
        print(f"Received username: {usernameInput}, password: {passwordInput}")
        
        user = authenticate(request, username=usernameInput, password=passwordInput)
        #check if authentication successful
        if user is not None:
            login(request, user)
            return JsonResponse({'message':'login successful'})
        else:
            return JsonResponse({'message':'invalid username and/or password'}, status=400)
        
        

def signup_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        
        #process data
        
        #if new, save,
        #attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            login(request, user) #log the user in
            return JsonResponse({'message':'user created successfully'})
        except IntegrityError: #if not new, say user already exists
            return JsonResponse({'message':'cannot create user, user already exists'})
            
        
    else:
        return JsonResponse({'error':'Invalid request'}, status=400)