from django.db import models

# Create your models here.


class Motorista(models.Model):
    nome = models.CharField(max_length=70, blank=False, default='')
    carro= models.CharField(max_length=200,blank=False, default='')
    id = models.IntegerField(primary_key=True)
