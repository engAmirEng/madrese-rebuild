from django.urls import path
from .views import dashboard, achievement, achievement_form, achievement_delete, \
    achievement_waiting, achievement_confirm_deny, student, student_form, \
        student_delete, user_waiting, user_confirm_deny
    # student_waiting, student_confirm_deny

app_name = "manager"
urlpatterns = [
    path('dashboard', dashboard, name="dashboard"),
    path('dashboard/achievement', achievement, name="achievement"),
    path('dashboard/achievement/form/<int:refrence_id>', achievement_form, 
        name="achievement_form"),
    path('dashboard/achievement/delete/<int:refrence_id>', achievement_delete, 
        name="achievement_delete"),
    path('dashboard/achievement_waiting', achievement_waiting, name="achievement_waiting"),
    path('dashboard/achievement_confirm_deny/<str:action>/<int:refrence_id>/<int:id>', 
        achievement_confirm_deny, name="achievement_confirm_deny"),
    path('dashboard/student', student, name="student"),
    path('dashboard/student/form/<int:refrence_id>', student_form, name="student_form"),
    path('dashboard/student/delete/<int:refrence_id>', student_delete, name="student_delete"),
    # path('dashboard/student_waiting', student_waiting, name="student_waiting"),
    # path('dashboard/student_confirm_deny/<str:action>/<int:refrence_id>/<int:id>', 
    #                                             student_confirm_deny, name="student_confirm_deny"),
    path('dashboard/user_waiting', user_waiting, name="user_waiting"),
    path('dashboard/achievement_confirm_deny/<str:action>/<int:id>', 
        user_confirm_deny, name="user_confirm_deny"),
]