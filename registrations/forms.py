from datetime import date
from django import forms
from .models import Registration

RACE_PRICES = {"5K": 675, "10K": 725, "21K": 840}
MIN_AGES = {"5K": 5, "10K": 15, "21K": 15}

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = [
            "race_category", "full_name", "bib_name", "date_of_birth", "gender",
            "mobile", "whatsapp", "email", "emergency_contact", "blood_group",
            "t_shirt_size", "team_name", "address", "city", "state", "pincode",
            "terms_accepted",
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "address": forms.Textarea(attrs={"rows": 3}),
            "terms_accepted": forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != "terms_accepted":
                field.widget.attrs.update({"class": "form-control"})
        self.fields["race_category"].widget.attrs["class"] = "form-select"
        self.fields["gender"].widget.attrs["class"] = "form-select"
        self.fields["t_shirt_size"].widget.attrs["class"] = "form-select"
        self.fields["terms_accepted"].widget.attrs["class"] = "form-check-input"
        self.fields["whatsapp"].required = False
        self.fields["team_name"].required = False
        self.fields["blood_group"].required = False
        self.fields["bib_name"].help_text = "Maximum 30 characters; this name is printed on your bib."

    def clean_mobile(self):
        value = self.cleaned_data["mobile"]
        if not value.isdigit() or len(value) != 10:
            raise forms.ValidationError("Enter a valid 10-digit mobile number.")
        return value

    def clean_whatsapp(self):
        value = self.cleaned_data.get("whatsapp", "")
        if value and (not value.isdigit() or len(value) != 10):
            raise forms.ValidationError("Enter a valid 10-digit WhatsApp number.")
        return value

    def clean_emergency_contact(self):
        value = self.cleaned_data["emergency_contact"]
        if not value.isdigit() or len(value) != 10:
            raise forms.ValidationError("Enter a valid 10-digit emergency contact.")
        return value

    def clean_pincode(self):
        value = self.cleaned_data["pincode"]
        if not value.isdigit() or len(value) != 6:
            raise forms.ValidationError("Enter a valid 6-digit PIN code.")
        return value

    def clean(self):
        cleaned = super().clean()
        dob = cleaned.get("date_of_birth")
        race = cleaned.get("race_category")
        if dob and race:
            today = date(2027, 1, 10)  # age is assessed on event day
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < MIN_AGES[race]:
                self.add_error("date_of_birth", f"Minimum age for {race} is {MIN_AGES[race]} years on event day.")
        if not cleaned.get("terms_accepted"):
            self.add_error("terms_accepted", "You must accept the event terms to register.")
        return cleaned
