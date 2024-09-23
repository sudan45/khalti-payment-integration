from django.db import models
from food.models import Food
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Order(models.Model):
    class Orderstatus(models.IntegerChoices):
        PENDING = (1, "Pending")
        INITIATED = (2, "Initiated")
        SUCCESS = (3, "Success")
        FAILURE = (4, "Failure")
        
    order_id = models.UUIDField(unique=True,default=uuid.uuid4)
    title = models.CharField(max_length=40, null=True, blank=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    total_price  = models.FloatField()
    order_status = models.PositiveSmallIntegerField(choices=Orderstatus.choices, default=Orderstatus.PENDING)
    pidx = models.CharField(max_length=50, null=True, blank=True)
    khalti_txn_id = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.title
    
    def save(self,*args, **kwargs):
        self.title = f'{self.food.name} {self.qty} {self.user.username}'
        return super().save()
        