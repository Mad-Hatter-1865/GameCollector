from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Game, Player
from .forms import ExpansionForm

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'gamecollector2'

import uuid
import boto3
from .models import Game, Player, Photo



def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def games_index(request):
    games = Game.objects.filter(user=request.user)
    return render(request, 'games/index.html', {'games': games})
@login_required
def games_detail(request, game_id):
    game = Game.objects.get(id=game_id)
    players_game_doesnt_have = Player.objects.exclude(id__in = game.players.all().values_list('id'))
    expansion_form = ExpansionForm()
    return render(request, 'games/detail.html', {'game': game, 'expansion_form': expansion_form, 'players': players_game_doesnt_have})
@login_required
def add_expansion(request, game_id):
    form = ExpansionForm(request.POST)
    if form.is_valid():
        new_expansion = form.save(commit=False)
        new_expansion.game_id = game_id
        new_expansion.save()
    return redirect('detail', game_id=game_id)
@login_required
def assoc_player(request, game_id, player_id):
    Game.objects.get(id=game_id).players.add(player_id)
    return redirect('detail', game_id=game_id)
@login_required
def add_photo(request, game_id):
    
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            
            photo = Photo(url=url, game_id=game_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', game_id=game_id)


def signup(request):
  error_message = ''
  if request.method == 'POST':
  
    form = UserCreationForm(request.POST)
    if form.is_valid():
      
      user = form.save()
      
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
 
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class GameCreate(LoginRequiredMixin, CreateView):
    model = Game
    fields = ['title','platform', 'description', 'relyear']
    success_url = '/games/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class GameUpdate(LoginRequiredMixin, UpdateView):
    model = Game
    fields = ['platform', 'description', 'relyear']

class GameDelete(LoginRequiredMixin, DeleteView):
    model = Game
    success_url = '/games/'

class PlayerList(LoginRequiredMixin, ListView):
    model = Player

class PlayerDetail(LoginRequiredMixin, DetailView):
    model= Player

class PlayerCreate(LoginRequiredMixin, CreateView):
    model = Player
    fields = '__all__'

class PlayerUpdate(LoginRequiredMixin, UpdateView):
    model = Player
    fields = '__all__'

class PlayerDelete(LoginRequiredMixin, DeleteView):
    model = Player
    success_url = '/players/'
