from django.db import models
from django.contrib.auth.models import User

class ProfileModel(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.IntegerField()
    def __str__(self):
        return str(self.user)
# Create your models here.
