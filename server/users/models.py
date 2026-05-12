from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    
    
    name = models.CharField(max_length=255)
    
    email = models.EmailField(unique=True)
    
    date_of_birth = models.DateField(null=True, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    
    modified_date = models.DateTimeField(auto_now=True)
    
    
    
    def __str__(self):
        return self.email

# Create your models here.
