from django.contrib import admin
from .models import Game, Expansion, Player, Photo
# Register your models here.

admin.site.register(Game)
admin.site.register(Expansion)
admin.site.register(Player)
admin.site.register(Photo)