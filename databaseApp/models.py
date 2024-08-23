from django.db import models
from django.contrib.auth.models import AbstractUser


class Lesson(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE, related_name='lessons', null=True)
    reading_material = models.TextField()
    video_link = models.TextField()
    practice_exercise = models.TextField()
    
class Unit(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='units', null=True)

class Course(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='courses', null=True)
    #by default a Course will not be attached to a User...
    
    def __str__(self):
        return self.title

class User(AbstractUser):
    # Your custom fields for the User model
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_query_name='user',
    )

    def __str__(self):
        return f"{self.id}: {self.username}"
