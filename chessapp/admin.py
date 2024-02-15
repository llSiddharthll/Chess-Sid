from django.contrib import admin
from .models import *  # Replace 'your_app' with the actual name of your app

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('game_name', 'game_type')