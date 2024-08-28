from django.shortcuts import render
import json
from django.db import IntegrityError
from databaseApp.models import *
from django.http import JsonResponse
#from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
import google.generativeai as google_ai
import time
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import requests
from bs4 import BeautifulSoup
import urllib.parse

def find_youtube_link(title_word, hashtag_word1, hashtag_word2):
    query = f"{title_word} site:youtube.com"
    youtube_url = f"https://www.google.com/search?q={query}&gbv=1"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    response = requests.get(youtube_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all valid YouTube links on the page
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and "youtube.com/watch" in href:
            video_url = urllib.parse.unquote(href.split("&")[0].replace("/url?q=", ""))
            video_response = requests.get(video_url)
            video_soup = BeautifulSoup(video_response.text, "html.parser")
            
            # Check if the title contains the word and hashtags contain the specified words
            title = video_soup.find("title")
            hashtags = video_soup.find_all("meta", {"property": "og:video:tag"})
            
            
            if title and title_word.lower() in title.text.lower():
                
                # Uncomment the following lines to check hashtags as well
                for hashtag in hashtags:
                    tag = hashtag.get("content").lower()
                    print("tag:"+ tag)
                    if hashtag_word1.lower() in tag or hashtag_word2.lower() in tag:
                        return video_url
    
    return None

#helper function
def get_gemini_api_key():
    #this is outside the scope of the repo
    #other people will need their own api key for google gemini's AI
    f = open("../gemini_api_key.txt", "r")
    key = f.read()
    return key

def get_unit_names_array(course_name):
    time.sleep(2)#add time delay so we dont overload google with requests and get error
    
    #prompt for units array
    prompt = '''For learning the skill: '''+course_name+''', name 2-3 subskills that make up that skill. 
    only respond with those 2 to 5 words and seperate them with commas only. for example if it were the skill: guitar, you would
    respond with: chords,scales,strumming'''
    gemini_key = get_gemini_api_key()
    google_ai.configure(api_key=gemini_key)
    gemini_model = google_ai.GenerativeModel('gemini-1.5-flash')
     
    gemini_response = gemini_model.generate_content(prompt)
     
    #print("units array response: "+gemini_response.text)
    units = str(gemini_response.text).split(",")     
    return units

def get_lesson_names_array(course_name, unit_name):
    time.sleep(12)#add time delay so we dont overload google with requests and get error
    
    #safety config so gemini api doesnt block any requests
    """
    safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    }
    """
    
    #prompt for getting lessons array
    prompt = ''' For learning the skill: '''+unit_name+''' in the context of learning: '''+course_name+''',
        name 1-3 lessons that can be done to grasp some experience with that skill.
        only respond with those 1 to 3 names and seperate them with commas only. for example if it were learning the skill: 
        chords in the context of learning: guitar, you would respond with: Open Chords, Barre Chords'''
    gemini_key = get_gemini_api_key()
    google_ai.configure(api_key=gemini_key)
    gemini_model = google_ai.GenerativeModel('gemini-1.5-flash') 
    
    
    gemini_response = gemini_model.generate_content(prompt)
    #PROMPT FEEDBACK (for safety), TESTING
    print("PROMPT FEEDBACK: "+str(gemini_response.prompt_feedback))
    
    #remove any trailing spaces, and seperate by ","
    lessons = str(gemini_response.text).strip().split(",")
    
    return lessons

#get_lesson_content(course_name, unit_name, lesson_name) 
# #-> returns array of strings [description, reading material, video link, practice_exercise]
def get_lesson_content(course_name, unit_name, lesson_name):
    time.sleep(7)#add time delay so we dont overload google with requests and get error
    
    #setup gemini
    gemini_key = get_gemini_api_key()
    google_ai.configure(api_key=gemini_key)
    gemini_model = google_ai.GenerativeModel('gemini-1.5-flash') 
    
    #return list
    lesson_content = []
    
    #ask for lesson description
    prompt = '''there is a lesson on: '''+lesson_name+''' in the context of learning: '''+unit_name+''' in 
    order to learn: '''+course_name+'''. respond with 1 to 2 sentences on what the lesson is about and why it matters
    in the greater context, no additional text.
    for example if it were learning a lesson on: Open Chords in the context of learning: Chords in order to learn: guitar,
    you would respond with: Open chords, or open position chords, 
    are guitar chords that include at least one unfretted open string. 
    Open chords are also called “cowboy chords” because they're among the simplest chords to play, 
    making them easy to learn for beginners.'''
    
    description = gemini_model.generate_content(prompt).text
    lesson_content.append(description)
    
    #ask for lesson reading material
    prompt = '''I am trying to learn about '''+lesson_name+''' in the context 
    of learning about '''+unit_name+''' for '''+course_name+'''. what is some key general 
    knowledge I should know about. You answer should be between 2 and 6 sentences, 
    use whatever you find appropriate in that range. No Additional text.'''
    
    reading_material = gemini_model.generate_content(prompt).text
    lesson_content.append(reading_material)
    
    #wait to avoid overloading request
    time.sleep(2)
    
    # link
    video_link = str(find_youtube_link(lesson_name,course_name,unit_name))
    lesson_content.append(video_link)
    
    
    #ask for practice exercise
    prompt = '''Trying to learn about '''+lesson_name+''' in the context of
    learning about '''+unit_name+''' for '''+course_name+'''. explain (in 2 to 5 sentences) a practice exercise or project i can do to 
    develop my skill in this topic. For example if I were learning about open chords in the context of learning  
    chords for guitar, you would tell me... Exercise: Open Chord Mastery with "Wonderwall".
    For this exercise, you'll practice the fundamental open chords G, Am, C, and D using the classic Oasis song "Wonderwall." 
    These chords are essential building blocks in guitar playing. Learn the chords and practice playing them smoothly and accurately. Once comfortable, 
    play along with the song's rhythm. This exercise will improve your chord transitions and tempo control.'''
    practice_exercise = gemini_model.generate_content(prompt).text
    lesson_content.append(practice_exercise)
    
    #TESTING
    print("LESSON: "+ lesson_name)
    print(lesson_content)
    
    return lesson_content
    
    

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
        """
        gemini_key = get_gemini_api_key()
        google_ai.configure(api_key=gemini_key)
        gemini_model = google_ai.GenerativeModel('gemini-1.5-flash')
        
        gemini_response = gemini_model.generate_content("Write a poem about "+skill)
        
        print("poem about "+skill+": "+gemini_response.text)
        """
        
        
        #CREATING NEW COURSE
        
        #1. course model
        new_course = Course(title=skill, description="this course is about: "+skill)
        new_course.save()
        new_course.user = request.user
        new_course.save()
        
        #prompt for units array
        unit_names = get_unit_names_array(skill) #TESTING: just prints the gemini response for now
        
        #create each unit
        for unit_name in unit_names:
            #2. create unit models
            newUnit = Unit(title=unit_name, description="testing", course=new_course)
            newUnit.save()
            #prompt for lessons array
            lesson_names = get_lesson_names_array(skill, unit_name)
            #create each lesson
            for lesson_name in lesson_names:
                #get_lesson_content() -> returns array of strings [description, reading material, video link, practice_exercise]
                lesson_content = get_lesson_content(skill,unit_name,lesson_name)
                newLesson = Lesson(title=lesson_name, description=lesson_content[0], unit=newUnit, reading_material=lesson_content[1], 
                video_link=lesson_content[2], practice_exercise=lesson_content[3])
                newLesson.save()
        
        
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