from django.urls import path
from .views import login, logout, register_student, register_mentor, register_manager

app_name = "accounts"
urlpatterns = [
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('register/student', register_student, name="register_student"),
    path('register/mentor', register_mentor, name="register_mentor"),
    path('register/manager', register_manager, name="register_manager"),
]
