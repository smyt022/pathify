from django.shortcuts import render
import json
from django.db import IntegrityError
from databaseApp.models import *
from django.http import JsonResponse
#from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout


#helper endpoint
def user_info(request):
    user_info = {
        'is_authenticated': request.user.is_authenticated,
        'username': request.user.username,
        'courses': []
    }
    
    #add courses if user is authenticated
    if(request.user.is_authenticated):
        #populate courses 
        for course in request.user.courses.all():
            course_info = {
                'title': course.title,
                'description': course.description,
                'units': []
            }
            
            #populate the units for the course_info
            for unit in course.units.all():
                unit_info = {
                    'title': unit.title,
                    'description': unit.description,
                    'lessons': []
                }
                
                #populate the lessons for the unit_info
                for lesson in unit.lessons.all():
                    lesson_info = {
                        'title': lesson.title,
                        'description': lesson.description,
                        'reading_material': lesson.reading_material,
                        'video_link': lesson.video_link,
                        'practice_exercise': lesson.practice_exercise
                    }
                    #add lesson to unit_info lessons
                    unit_info['lessons'].append(lesson_info)
                
                #add unit to course_info units
                course_info['units'].append(unit_info)
            
            #add course to user_info courses
            user_info['courses'].append(course_info)
    
    return JsonResponse(user_info)

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