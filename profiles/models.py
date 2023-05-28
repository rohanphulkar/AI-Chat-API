from django.db import models
from accounts.models import User
from django.utils import timezone
import uuid

class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='profile')
    is_pro =  models.BooleanField(default=False)
    plan_validity = models.DateField(default=timezone.now() + timezone.timedelta(days=3))

    def __str__(self):
        return f'Profile for {self.user.email}'

class Purchase(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="purchase")
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Purchase for {self.user.email}'