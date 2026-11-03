# Kasaragod Marathon — Django recreation

A responsive Django recreation inspired by the publicly visible layout and event information for Mathrubhumi India's VKC Kasaragod Marathon 2027. This is an independent demo project, not the official website and not affiliated with the event organisers.

## Included
- Responsive landing page, race cards, prize information, about, partner section and footer
- Django registration form with server-side validation
- SQLite database model and booking ID generation
- Age eligibility validation based on 10 January 2027
- Django admin for viewing registrations and updating payment status
- Booking confirmation page
- Event rules page

## Event information currently represented
- Event date: Sunday, 10 January 2027
- Venue: Freedom Square, Kasaragod Beach
- 5K: ₹675 (minimum age 5)
- 10K: ₹725 (minimum age 15)
- 21K: ₹840 (minimum age 15)
- Event helpdesk details shown in the public event information

Prices and details may change. Confirm with the event organisers before using this demo for real registrations.

## Setup (Windows)

1. Install Python 3.10+.
2. Extract this ZIP file.
3. Open Command Prompt in the extracted `Kasaragod_marathon_django` folder.
4. Create a virtual environment:

   ```bash
   py -m venv .venv
   .venv\Scripts\activate
   ```

5. Install packages:

   ```bash
   pip install -r requirements.txt
   ```

6. Create database tables:

   ```bash
   python manage.py makemigrations registrations
   python manage.py migrate
   ```

7. Create admin login:

   ```bash
   python manage.py createsuperuser
   ```

8. Start the website:

   ```bash
   python manage.py runserver
   ```

9. Open `http://127.0.0.1:8000/` in your browser.
10. Admin dashboard: `http://127.0.0.1:8000/admin/`

## Important: payment is NOT integrated

The registration form stores a booking with `PENDING` payment status. It does not collect money, issue an official event ticket, or connect to Razorpay/any payment gateway. Before accepting real registrations, integrate a payment provider using its official server-side SDK, verify payment signatures/webhooks, and only then mark registrations paid.

## Before production deployment
- Set a strong `DJANGO_SECRET_KEY` in environment variables.
- Set `DJANGO_DEBUG=False`.
- Set `DJANGO_ALLOWED_HOSTS` to your domain.
- Configure HTTPS, secure cookies, database backups and production database (PostgreSQL recommended).
- Configure a real email backend (SMTP).
- Add privacy notice, consent and data-retention procedures.
- Obtain permission for official logos, sponsor marks, photographs and branding. The included stock photos are external Unsplash URLs and can be replaced with licensed local images.
- Confirm event date, prices, rules, age requirements, prize details and contact information with the organiser.

## Project structure

```text
Kasaragod_marathon_django/
├── manage.py
├── requirements.txt
├── README.md
├── marathon_project/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── registrations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
├── templates/
│   ├── base.html
│   └── registrations/
│       ├── home.html
│       ├── register.html
│       ├── success.html
│       └── rules.html
└── static/
    ├── css/style.css
    └── js/main.js
```
