from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import FollowerTable, User

class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ['username', "email", "private_status"]
    fieldsets = (
        (None, {"fields": ("username", "password","private_status")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "email", "phone_number", "birthday", "gender", "biography")}),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser")}
        ),
        ("Important dates", {"fields": ("last_login","date_joined")})
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide", ),
            "fields": ("username", "password1", "password2",)
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(FollowerTable)