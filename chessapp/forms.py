from django import forms
from .models import Game
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        exclude = ['creator','opponent', 'other_side', 'fen', 'turn', 'move_history']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
