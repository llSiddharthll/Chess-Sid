from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.views.generic import CreateView

def index(request):
    return render(request, "home.html", {'user': request.user})

def chess_game(request, id):
    game = get_object_or_404(Game, id=id)
    current_user = request.user

    # Retrieve the game object
    game = Game.objects.get(id=id)
    user_profile, created = UserProfile.objects.get_or_create(user=current_user)
        
    # Check if the current user is the creator or opponent
    if current_user == game.creator:
        # The current user is the creator
        is_creator = True
        is_opponent = False
    else:
        # The current user is the opponent
        is_creator = False
        is_opponent = True
    
    if is_opponent and (current_user != game.creator):
        game.opponent = current_user
        game.save()
    if game.selected_side == 'white':
        game.other_side = 'black'
        game.save()
    else:
        game.other_side = 'white'
        game.save()
    if current_user == game.creator:
        user_profile.selected_side = game.selected_side
    else:
        user_profile.other_side = game.other_side
    
    user_profile.save()
    
    context = {
        'user_profile': user_profile,
        'game': game,
        'is_creator': is_creator,
        'is_opponent': is_opponent,
    }
    return render(request, 'chess.html', context)

@login_required(login_url='signup')
def create_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.creator = request.user  # Set the creator to the current user
            game.other_side = 'white' if game.selected_side == 'black' else 'black'
            game.save()

            return redirect('chess_game', game.id)
    else:
        form = GameForm()

    return render(request, 'create_game.html', {'form': form, 'user': request.user})

@login_required(login_url='signup')
def games_list(request):
    games = Game.objects.all().order_by('-created_at')
    return render(request, 'game_list.html', {"games": games, 'user': request.user})

def profile(request, id):
    user_profile = UserProfile.objects.get(id=id)
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'profile.html', context)


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"