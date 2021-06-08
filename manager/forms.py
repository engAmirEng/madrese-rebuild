from django import forms
from django.forms import widgets
from index.models import Student, Achievement


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [i.name for i in Student._meta.get_fields()]
        fields.remove("achievement")
        labels = {"first_name":"نام", "last_name":"نام خانوادگی", "birthday":"تاریخ تولد", "photo":"تصویر", "meli_code":"کد ملی"}

class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = [i.name for i in Achievement._meta.get_fields()]
        labels = {"owner":"مقام آورنده", "title":"عنوان", "year":"سال کسب", "field":"زمینه", \
            "level":"سطح عنوان", "dore":"دوره", "pic":"تصویر مدرک", "video_link":"لینک ویدیو", "detail":"جزییات"}