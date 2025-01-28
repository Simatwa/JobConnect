from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from enum import Enum
from uuid import uuid4
from os import path
from django.core.validators import FileExtensionValidator, RegexValidator

# Create your models here.


class UserCategory(str, Enum):
    ORG = _("Organization")
    INDIVIDUAL = _("Individual")


def generate_document_filepath(instance: "CustomUser", filename: str) -> str:
    custom_filename = str(uuid4()) + path.splitext(filename)[1]
    return f"user_document/{instance.category}/{custom_filename}"


def generate_profile_filepath(instance: "CustomUser", filename: str) -> str:
    custom_filename = str(uuid4()) + path.splitext(filename)[1]
    return f"user_profile/{instance.id}{custom_filename}"


class CustomUser(AbstractUser):
    """Both indiduals and organizations"""

    category = models.CharField(
        verbose_name=_("category"),
        help_text=_("Can either be an Individual or Organization"),
        choices=(
            ["Organization", UserCategory.ORG.value],
            ["Individual", UserCategory.INDIVIDUAL.value],
        ),
        null=False,
        max_length=30,
    )
    description = models.TextField(
        verbose_name=_("description"),
        help_text=_("Information about user in details."),
        null=True,
        blank=True,
    )

    location = models.CharField(
        verbose_name=_("location"),
        help_text=_("User's place of residence or office"),
        null=False,
        blank=False,
        max_length=50,
    )

    phone_number = models.CharField(
        verbose_name=_("phone number"),
        help_text=_("Active telephone number"),
        null=False,
        blank=False,
        max_length=15,
        validators=[
            RegexValidator(
                r"\+\d{12,13}|\d{10,11}",
                "Enter a valid phone number. This phone number may start with '+COUNTRY-CODE'",
            )
        ],
    )

    documents = models.FileField(
        verbose_name=_("documents"),
        help_text=_("Individual's resume or company's Certificate of Existence (pdf)"),
        upload_to=generate_document_filepath,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        blank=True,
        null=True,
    )

    profile = models.ImageField(
        _("Profile Picture"),
        default="default/user_avatar.png",
        upload_to=generate_profile_filepath,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
        blank=True,
        null=True,
    )

    REQUIRED_FIELDS = [
        "category",
        "description",
        "phone_number",
        "email",
        "location",
    ]

    DISPLAY_FIELDS = [
        "first_name",
        "last_name",
        "category",
        "category",
        "phone_number",
        "location",
        "date_joined",
    ]

    search_fields = ["first_name", "last_name", "email", "phone_number", "location"]

    def get_form_fields(self):
        return [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "category",
            "description",
            "location",
            "phone_number",
            "documents",
        ]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        abstract = False
