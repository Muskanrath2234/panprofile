# admin.py
from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'DOB', 'Pan', 'father_Name', 'Profile_img')
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'name', 'DOB', 'Pan', 'father_Name', 'Profile_img'),
        }),
    )

admin.site.register(Profile, ProfileAdmin)
