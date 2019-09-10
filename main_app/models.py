from django.db import models
from django.urls import reverse

class Game(models.Model):
    title = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    relyear = models.IntegerField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'game_id': self.id})

class Expansion(models.Model):
    extitle = models.CharField(max_length=100)
    rely = models.IntegerField()

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
