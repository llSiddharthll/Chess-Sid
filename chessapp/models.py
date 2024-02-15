# models.py
from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Game_Creator")
    opponent = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="Opponent_player", default=None)
    game_name = models.CharField(max_length=255, unique=True)
    selected_side = models.CharField(max_length=10)
    other_side = models.CharField(max_length=10)
    game_type = models.CharField(max_length=50)
    fen = models.CharField(max_length=225, default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1' )
    game_is = models.CharField(max_length=50, default="normal")
    turn = models.CharField(max_length=1, default='w')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.creator.username}'s {self.game_name} Game"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    selected_side = models.CharField(max_length=10, blank=True, null=True)
    other_side = models.CharField(max_length=10, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    ranking = models.IntegerField(default=0)
    matches_played = models.IntegerField(default=0)
    matches_won = models.IntegerField(default=0)
    matches_lost = models.IntegerField(default=0)
    matches_draw = models.IntegerField(default=0)