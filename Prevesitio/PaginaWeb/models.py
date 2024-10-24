from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField( upload_to='perfiles', null=True)

    def __str__(self):
        return f'{self.user.username} Perfil'
