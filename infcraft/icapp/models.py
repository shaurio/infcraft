from django.db import models

# Create your models here.

class Btn(models.Model):
    label = models.CharField(max_length=120)
    emoji = models.CharField(max_length=16)


    def __str__(self):
        return self.label


