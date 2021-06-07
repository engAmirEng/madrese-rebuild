from django.contrib import admin
from .models import Student,Achievement

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "birthday"]

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = [i.name for i in Achievement._meta.get_fields()]
    list_display.remove("detail")