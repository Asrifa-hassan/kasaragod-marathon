from django.contrib import admin
from .models import Registration

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("booking_id", "full_name", "race_category", "mobile", "amount", "payment_status", "created_at")
    list_filter = ("race_category", "payment_status", "gender", "created_at")
    search_fields = ("booking_id", "full_name", "mobile", "email")
    readonly_fields = ("booking_id", "created_at")
    list_editable = ("payment_status",)
