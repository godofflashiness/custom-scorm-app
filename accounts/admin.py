from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser) 
class CustomUserAdmin(admin.ModelAdmin):
    exclude = ('client',)  # For core admins
    list_display = ('username', 'email', 'client', 'is_admin')  
    list_filter = ('client', 'is_admin') 
