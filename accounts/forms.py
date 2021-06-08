# This form is used in .admin in order to customizing the defult User Model

from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserAdminForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'
