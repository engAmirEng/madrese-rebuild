from django.urls import path
from .views import dashboard, achievement, achievement_form, achievement_confirm_deny, \
    achievement_waiting, achievement_delete

app_name = "student"
urlpatterns = [
    path('dashboard', dashboard, name="dashboard"),
    path('dashboard/achievement', achievement, name="achievement"),
    path('dashboard/achievement/form/<int:refrence_id>', achievement_form, name="achievement_form"),
    path('dashboard/achievement/delete/<int:refrence_id>', achievement_delete, name="achievement_delete"),
    path('dashboard/achievement_waiting', achievement_waiting, name="achievement_waiting"),
    path('dashboard/achievement_confirm_deny/<str:action>/<int:refrence_id>/<int:id>', 
                                                achievement_confirm_deny, name="achievement_confirm_deny"),
]