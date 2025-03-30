from django.contrib import admin
from .models import ContactMessage, MissionInput

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)

@admin.register(MissionInput)
class MissionInputAdmin(admin.ModelAdmin):
    list_display = ('user', 'rocket_name', 'destination', 'launch_date', 'created_at')
    search_fields = ('rocket_name', 'destination', 'user__username')
    readonly_fields = ('created_at',)
