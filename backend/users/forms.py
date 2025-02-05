from django import forms
from users.models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    password = forms.PasswordInput()

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "username",
            "password",
            "location",
            "phone_number",
            "last_name",
            "email",
            "category",
            "description",
            "documents",
            "profile",
        ]


class CustomUserUpdateForm(forms.ModelForm):
    password = forms.PasswordInput()

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "username",
            "password",
            "dob",
            "gender",
            "location",
            "phone_number",
            "last_name",
            "email",
            "category",
            "description",
            "documents",
            "profile",
        ]
