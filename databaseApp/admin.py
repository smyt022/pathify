from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
#import all the models
# that you want to register
from databaseApp.models import User
from databaseApp.models import Course

#register the models
admin.site.register(User, UserAdmin)
admin.site.register(Course)