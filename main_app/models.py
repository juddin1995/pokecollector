from django.db import models
from django.urls import reverse

# Create your models here.

class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    poke_id = models.IntegerField()
    xp = models.IntegerField()
    type = models.CharField(max_length=100)
    abilities = models.TextField()
    image_url = models.URLField()
    nickname = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.id}'
    
    def get_absolute_url(self):
        return reverse('poke-detail', kwargs={'poke_id': self.poke_id})
