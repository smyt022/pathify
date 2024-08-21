"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('/signup/', views.signup, name='signup')
]
"""



from django.urls import re_path
from django.urls import path
from django.views.generic import TemplateView
from . import views
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/logout/', views.logout_view, name='api-logout'),
    path('api/is_authenticated/', views.is_authenticated, name='api-isAuthenticated'), #backend route to check if user is authenticated
    path('api/signup/', views.signup_view, name='api-signup'), #backend api route
    path('api/login/', views.login_view, name='api-login'), #backend api route
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]
