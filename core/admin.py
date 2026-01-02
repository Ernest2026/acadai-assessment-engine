# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AcadUser

class AcadUserAdmin(UserAdmin):
    # This adds the fields to the User Edit page
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_student', 'is_admin')}),
    )
    
    # This adds the fields to the User Add page
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_student', 'is_admin')}),
    )

    # This shows the fields in the user list view
    list_display = ('username', 'email', 'is_student', 'is_admin', 'is_staff')

# Register your custom admin class
admin.site.register(AcadUser, AcadUserAdmin)