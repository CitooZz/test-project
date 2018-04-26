from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('username', 'role', 'is_active')
    search_fields = ('username', )
