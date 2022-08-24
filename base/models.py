from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
# Create your models here.

class Tasks(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    titulo =  models.CharField(max_length=200, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    completado = models.BooleanField(default=False)
    crear = models.DateTimeField(auto_now_add=True, auto_now=False)
    #actualizar = models.DateTimeField(auto_now=True)
    #due = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    def __str__(self):

        return self.titulo

    class Meta:
        ordering =['completado'] 