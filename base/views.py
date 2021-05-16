from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.conf import settings

import stripe
from . import models

stripe.api_key = settings.STRIPE['secret']


def index(request):
    context = {
        'stripe_public': settings.STRIPE['public']
    }
    return render(request, 'base/index.html', context)


def charge(request):
    if request.method == 'POST':
        amount = int(request.POST['amount'])
        print(request.POST['stripeToken'])

        customer = models.StripeCustomer.objects.filter(user=request.user).first()
        if customer is None:
            stripe_customer = stripe.Customer.create(
                email=request.user.email,
                source=request.POST['stripeToken']
            )

            customer = models.StripeCustomer.objects.create(user=request.user, stripe_id=stripe_customer.stripe_id)

        charge = stripe.Charge.create(
            customer=customer.stripe_id,
            amount=amount * 100,
            currency='usd',
            description="Donation"
        )

    return redirect(reverse('success', args=[amount]))


def successMsg(request, args):
    amount = args
    return render(request, 'base/success.html', {'amount': amount})
