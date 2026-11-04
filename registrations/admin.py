from django.contrib import admin
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from .models import Registration

def export_registrations_excel(modeladmin, request, queryset):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Marathon Registrations"

    headers = [
        "Booking ID", "Full Name", "BIB Name", "Race Category",
        "Date of Birth", "Gender", "Mobile", "WhatsApp", "Email",
        "Emergency Contact", "Blood Group", "T-Shirt Size",
        "Address", "City", "State", "Pincode", "Team Name",
        "Amount", "Payment Status", "Payment Reference",
        "Registration Date",
    ]

    sheet.append(headers)
    # Style heading row
    for cell in sheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(
            start_color="4338CA",
            end_color="4338CA",
            fill_type="solid"
        )
        cell.alignment = Alignment(horizontal="center")

    for registration in queryset:
        sheet.append([
            registration.booking_id,
            registration.full_name,
            registration.bib_name,
            registration.race_category,
            registration.date_of_birth.strftime("%d-%m-%Y")
            if registration.date_of_birth else "",
            registration.gender,
            registration.mobile,
            registration.whatsapp,
            registration.email,
            registration.emergency_contact,
            registration.blood_group,
            registration.t_shirt_size,
            registration.address,
            registration.city,
            registration.state,
            registration.pincode,
            registration.team_name,
            registration.amount,
            registration.payment_status,
            registration.payment_reference,
            registration.created_at.strftime("%Y-%m-%d %H:%M")
            if registration.created_at else "",
        ])

    # Automatically adjust column widths
    for column in sheet.columns:
        max_length = 0
        column_letter = column[0].column_letter

        for cell in column:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))

        sheet.column_dimensions[column_letter].width = max_length + 4

    # Add filters and freeze heading row
    sheet.auto_filter.ref = sheet.dimensions
    sheet.freeze_panes = "A2"

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        'attachment; filename="kasaragod_marathon_registrations.xlsx"'
    )

    workbook.save(response)
    return response

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    actions = [export_registrations_excel]

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
