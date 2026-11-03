import uuid
from django.db import models
from django.utils import timezone

class Registration(models.Model):
    RACE_CHOICES = [
        ("5K", "5K Fun Run"),
        ("10K", "10K Timed Run"),
        ("21K", "21K Half Marathon"),
    ]
    GENDER_CHOICES = [
        ("Male", "Male"), ("Female", "Female"), ("Other", "Other"),
        ("Prefer not to say", "Prefer not to say"),
    ]
    SHIRT_CHOICES = [(s, s) for s in ("XS", "S", "M", "L", "XL", "XXL", "3XL")]
    PAYMENT_CHOICES = [
        ("PENDING", "Pending"), ("PAID", "Paid"), ("FAILED", "Failed"),
    ]

    booking_id = models.CharField(max_length=14, unique=True, editable=False)
    race_category = models.CharField(max_length=3, choices=RACE_CHOICES)
    full_name = models.CharField(max_length=120)
    bib_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    mobile = models.CharField(max_length=10)
    whatsapp = models.CharField(max_length=10, blank=True)
    email = models.EmailField()
    emergency_contact = models.CharField(max_length=10)
    blood_group = models.CharField(max_length=5, blank=True)
    t_shirt_size = models.CharField(max_length=3, choices=SHIRT_CHOICES)
    address = models.TextField()
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=80, default="Kerala")
    pincode = models.CharField(max_length=6)
    team_name = models.CharField(max_length=120, blank=True)
    amount = models.PositiveIntegerField()
    payment_status = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default="PENDING")
    payment_reference = models.CharField(max_length=100, blank=True)
    terms_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = "KZM" + uuid.uuid4().hex[:8].upper()
        if not self.whatsapp:
            self.whatsapp = self.mobile
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_id} - {self.full_name}"
