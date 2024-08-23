from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
#import all the models
# that you want to register
from databaseApp.models import User
from databaseApp.models import Course
from databaseApp.models import Unit
from databaseApp.models import Lesson

#register the models
admin.site.register(User, UserAdmin)
admin.site.register(Course)
admin.site.register(Unit)
admin.site.register(Lesson)