from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class StripeCustomer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stripe_customer')
    stripe_id = models.CharField(max_length=255)

    def __str__(self):
        return f'Stripe customer of {self.user.get_username()}'
