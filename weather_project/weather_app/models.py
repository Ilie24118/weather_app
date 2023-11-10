from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class City(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'cities'
        unique_together = ('owner','name')