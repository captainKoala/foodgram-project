from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email']
    fields = ['username', 'last_name', 'first_name', 'email', 'password',
              'is_staff']
    search_fields = ['username', 'first_name', 'last_name']


admin.site.register(User, UserAdmin)
