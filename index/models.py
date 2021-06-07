from django.db import models
from django.utils import timezone


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthday = models.DateField()
    photo = models.ImageField(upload_to="photoes/students/%Y/%m/%d")

    def __str__(self):
        return(f"{self.first_name} {self.last_name}")


class Achievement(models.Model):
    owner = models.ForeignKey("Student" , on_delete=models.CASCADE)
    title = models.CharField(max_length=50)

    y_CHOICES = ((i, i) for i in range(1385, timezone.now().year-619))
    year = models.IntegerField(choices=y_CHOICES)

    f_CHOICES = (("پرورشی","پرورشی"), 
                ("آموزشی","آموزشی"), 
                ("پژوهشی","پژوهشی"), 
                ("ورزشی","ورزشی"))
    field = models.CharField(max_length=50, choices=f_CHOICES)

    v_CHOICES = (("مدرسه","مدرسه"), 
                ("ناحیه","ناحیه"), 
                ("شهر","شهر"), 
                ("استان","استان"),
                ("کشور","کشور"),
                ("بین الملل","بین الملل"))
    level = models.CharField(max_length=50, choices=v_CHOICES)
    dore = models.CharField(max_length=50, choices=(("اول","اول"), ("دوم", "دوم")))
    pic = models.ImageField(upload_to="photoes/achievement/%Y/%m/%d", blank=True)
    video_link = models.CharField(max_length=255, blank=True)
    detail = models.TextField(max_length=1024, blank=True)

    refrence_id = models.IntegerField(null=True)
    modify_level = models.CharField(choices=(("student", "student"), ("mentor", "mentor"), \
                                            ("manager", "manager")), blank=True, max_length=50)
    is_main = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return(self.title)


class Permissions(models.Model):
    class Meta:
        permissions = (
                        ("student", "student"),
                        ("mentor", "mentor"),
                        ("parvareshi_mentor", "parvareshi_mentor"),
                        ("amoozeshi_mentor", "amoozeshi_mentor"),
                        ("pazhooheshi_mentor", "pazhooheshi_mentor"),
                        ("varzeshi_mentor", "varzeshi_mentor"),
                        ("manager", "manager")
                        )