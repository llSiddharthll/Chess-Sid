from django.urls import path
from . import views
from .views import SignUpView

urlpatterns=[
    path('', views.index, name="home"),
    path('create-game/', views.create_game, name='create_game'),
    path('chess-game/<int:id>', views.chess_game, name='chess_game'),
    path('games-list/', views.games_list, name='games_list'),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('profile/<int:id>', views.profile, name='profile')
]