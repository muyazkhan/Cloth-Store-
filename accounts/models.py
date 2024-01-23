from django.db import models
from django.contrib.auth.models import User

class UserAccount(models.Model):
    user = models.OneToOneField(User, related_name="account", on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=13)
    balance = models.DecimalField(default=1000, max_digits=12, decimal_places=2)
    customer_id = models.IntegerField(unique=True)


    def __str__(self):
        return str(self.customer_id)