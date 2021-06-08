from django.db import models
from django.contrib.auth.models import AbstractUser
from index.models import Student

class User(AbstractUser):
    # if want to add or change fields, consider updating ".admin"
    meli_code = models.CharField(max_length=10, blank=True)
    # student_rel = models.OneToOneField(Student, null=True, on_delete=models.SET_NULL)
    # position_CHOICES = (
    #     ('student','student'), ('mentor_parvareshi','mentor_parvareshi'), 
    #     ('amoozeshi_mentor','amoozeshi_mentor'), ('pazhooheshi_mentor','pazhooheshi_mentor'), 
    #     ('pazhooheshi_mentor','pazhooheshi_mentor'), ('varzeshi_mentor','varzeshi_mentor'), 
    #     ('manager','manager')
    # )
    # position = models.CharField(max_length=20, choices=position_CHOICES)
