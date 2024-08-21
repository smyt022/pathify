from django.db import models
from django.contrib.auth.models import AbstractUser


class Course(models.Model):
    #
    title = models.CharField(max_length=64)
    description = models.TextField()
    
#user model
class User(AbstractUser):
    #add any properties you want for user
    # Resolve conflicts by defining related_name for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Set custom related_name
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  # Set custom related_name
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_query_name='user',
    )
    
    currentCourses = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='user', null=True)

    def __str__(self):
        return f"{self.id}: {self.username}"
    
    