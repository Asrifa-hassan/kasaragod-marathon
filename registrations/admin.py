from django.contrib import admin
from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):

    list_display = (
        "booking_id",
        "full_name",
        "bib_name",
        "race_category",
        "mobile",
        "email",
        "amount",
        "payment_status",
        "created_at",
    )

    list_filter = (
        "race_category",
        "payment_status",
        "gender",
        "t_shirt_size",
        "created_at",
    )

    search_fields = (
        "booking_id",
        "full_name",
        "bib_name",
        "mobile",
        "email",
    )

    readonly_fields = (
        "booking_id",
        "created_at",
    )

    list_editable = ("payment_status",)

    ordering = ("-created_at",)

    list_per_page = 25
