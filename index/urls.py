from django.urls import path
from .views import index, detail

app_name = "index"
urlpatterns = [
    path('', index, name="index"),
    path('detail/<int:refrence_id>', detail, name="detail"),
]