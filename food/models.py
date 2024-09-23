from django.db import models

# Create your models here.

class Food(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to="food/", null=True,blank=True)
    price = models.FloatField()

    def __str__(self) -> str:
        return self.name