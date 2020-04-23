from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ['email', 'is_staff', 'is_active']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    search_fields = ['email']
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'is_active', 'password')}),
        ('Permissions', {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
