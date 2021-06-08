from django.contrib import admin
from .models import User
from .forms import UserAdminForm
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = User
    add_form = UserAdminForm
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'our fields',
            {
                'fields': (
                    'meli_code',
                    'position',
                )
            }
        )
    )

admin.site.register(User, CustomUserAdmin)