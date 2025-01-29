from django import forms
from users.models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "username",
            "location",
            "phone_number",
            "last_name",
            "email",
            "category",
            "description",
            "documents",
            "profile",
        ]
