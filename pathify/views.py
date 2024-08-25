from django.shortcuts import render
import json
from django.db import IntegrityError
from databaseApp.models import *
from django.http import JsonResponse
#from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
import google.generativeai as google_ai


#helper function
def get_gemini_api_key():
    #this is outside the scope of the repo
    #other people will need their own api key for google gemini's AI
    f = open("../gemini_api_key.txt", "r")
    key = f.read()
    return key

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


#add a course under request.user with all parameters filled in
def create_course_view(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        skill = body.get('skill', '')
        print(f"Skill to learn: {skill}")  # Print the skill to the backend console
        
        #use google gemini to write a poem about the skill
        gemini_key = get_gemini_api_key()
        
        
        print("gemini api key: "+gemini_key)
        google_ai.configure(api_key=gemini_key)
        gemini_model = google_ai.GenerativeModel('gemini-1.5-flash')
        
        gemini_response = gemini_model.generate_content("Write a poem about "+skill)
        
        print("poem about "+skill+": "+gemini_response.text)
        
        
        #CREATING NEW COURSE
        #prompts
        
        #prompt for units
        """
        For learning the skill "__course__", name 2-3 subskills that make up that skill. only tell me those 2 to 5 words
        and seperate them with commas only. for example if it were the skill "guitar", you would tell me:
        "chords,scales,strumming patterns"
        """
        
        #prompt for lessons
        """
        For learning the skill "___unit___" in the context of learning "__course__",
        name 1-3 lessons that can be done to grasp some experience with that skill.
        only tell me those 1 to 3 names and seperate them with commas only. for example if it were "learning
        "chords" in the context of 'guitar', you would tell me: 'Open Chords, Barre Chords'
        
        """
        
        
        #creating database entries:
        #from prompts, save unit and lesson names to Json with arrays
        """
        1. Course:
        """
        new_course = Course(title="test_Course", description="this is for testing purposes")
        new_course.save()
        new_course.user = request.user
        new_course.save()
        
        """
        2. Units:
        """
        uOne = Unit(title="unit_one", description="testing", course=new_course)
        uOne.save()
        uTwo = Unit(title="unit_two", description="testing", course=new_course)
        uTwo.save()
        """
        3. Lessons:
        """
        uOneLessonOne = Lesson(title="uOneLessonOne", description="test", unit=uOne, reading_material="test", 
        video_link="https://youtu.be/J8ksL3oqqUE?si=GqSxNCOJiSvgwj0c", practice_exercise="test")
        uOneLessonOne.save()
        
        uTwoLessonOne = Lesson(title="uTwoLessonOne", description="test", unit=uTwo, reading_material="test", 
        video_link="https://youtu.be/J8ksL3oqqUE?si=GqSxNCOJiSvgwj0c", practice_exercise="test")
        uTwoLessonOne.save()
        
        
        return JsonResponse({"message": "Successfully created course"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)




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