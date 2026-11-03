from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from .forms import RegistrationForm, RACE_PRICES
from .models import Registration

RACE_INFO = [
    {"code": "5K", "name": "Fun Run", "distance": "5 KM", "price": 675, "original": 900, "age": "5+ years", "description": "Walk, jog or run — bring everyone."},
    {"code": "10K", "name": "Timed 10K", "distance": "10 KM", "price": 725, "original": 1000, "age": "15+ years", "description": "Chase a personal best along Beach Road."},
    {"code": "21K", "name": "Half Marathon", "distance": "21 KM", "price": 840, "original": 1200, "age": "15+ years", "description": "Take on the full coastal challenge."},
]

def home(request):
    return render(request, "registrations/home.html", {"races": RACE_INFO})

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.amount = RACE_PRICES[registration.race_category]
            registration.save()
            # This starter project records the booking as PENDING.
            # Add a real payment gateway (e.g. Razorpay) before accepting live payments.
            try:
                send_mail(
                    f"Marathon registration received - {registration.booking_id}",
                    f"Hello {registration.full_name}, your registration has been received. "
                    f"Booking ID: {registration.booking_id}. Payment is currently pending.",
                    settings.DEFAULT_FROM_EMAIL, [registration.email], fail_silently=True,
                )
            except Exception:
                pass
            return redirect("registration_success", booking_id=registration.booking_id)
    else:
        form = RegistrationForm()
    return render(request, "registrations/register.html", {"form": form, "races": RACE_INFO})

def registration_success(request, booking_id):
    registration = get_object_or_404(Registration, booking_id=booking_id)
    return render(request, "registrations/success.html", {"registration": registration})

def rules(request):
    return render(request, "registrations/rules.html")
