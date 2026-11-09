
from datetime import date

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegistrationForm, RACE_PRICES
from .models import Registration


RACE_INFO = [
    {
        "code": "5K",
        "name": "Fun Run",
        "distance": "5 KM",
        "price": 675,
        "original": 900,
        "age": "5+ years",
        "description": "Walk, jog or run — bring everyone.",
    },
    {
        "code": "10K",
        "name": "Timed 10K",
        "distance": "10 KM",
        "price": 725,
        "original": 1000,
        "age": "15+ years",
        "description": "Chase a personal best along Beach Road.",
    },
    {
        "code": "21K",
        "name": "Half Marathon",
        "distance": "21 KM",
        "price": 840,
        "original": 1200,
        "age": "15+ years",
        "description": "Take on the full coastal challenge.",
    },
]


def home(request):
    return render(request, "registrations/home.html", {"races": RACE_INFO})


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data.copy()

            # Store the date as text for session storage.
            data["date_of_birth"] = data["date_of_birth"].isoformat()

            request.session["pending_registration"] = data

            return redirect("payment")

    else:
        form = RegistrationForm()

    return render(
        request,
        "registrations/register.html",
        {"form": form, "races": RACE_INFO},
    )


def payment(request):
    data = request.session.get("pending_registration")

    if not data:
        return redirect("register")

    race_code = data.get("race_category")
    payment_method = data.get("payment_method")

    if race_code not in RACE_PRICES or payment_method not in ("UPI", "CASH"):
        request.session.pop("pending_registration", None)
        return redirect("register")

    amount = RACE_PRICES[race_code]
    race_name = dict(Registration.RACE_CHOICES).get(race_code)

    if request.method == "POST":
        payment_reference = request.POST.get("payment_reference", "").strip()

        if payment_method == "UPI" and not payment_reference:
            return render(
                request,
                "registrations/payment.html",
                {
                    "amount": amount,
                    "race_name": race_name,
                    "payment_method": payment_method,
                    "error": "Please enter your UPI transaction reference.",
                },
            )

        data["date_of_birth"] = date.fromisoformat(data["date_of_birth"])

        registration = Registration.objects.create(
            **data,
            amount=amount,
            payment_status="PENDING",
            payment_reference=payment_reference,
        )

        request.session.pop("pending_registration", None)

        try:
            send_mail(
                f"Marathon registration received - {registration.booking_id}",
                (
                    f"Hello {registration.full_name}, your registration has been received. "
                    f"Booking ID: {registration.booking_id}. "
                    f"Payment status: Pending verification."
                ),
                settings.DEFAULT_FROM_EMAIL,
                [registration.email],
                fail_silently=True,
            )
        except Exception:
            pass

        return redirect(
            "registration_success",
            booking_id=registration.booking_id,
        )

    return render(
        request,
        "registrations/payment.html",
        {
            "amount": amount,
            "race_name": race_name,
            "payment_method": payment_method,
        },
    )


def registration_success(request, booking_id):
    registration = get_object_or_404(
        Registration,
        booking_id=booking_id,
    )
    return render(
        request,
        "registrations/success.html",
        {"registration": registration},
    )


def rules(request):
    return render(request, "registrations/rules.html")
