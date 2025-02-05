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


class Gender(str, Enum):
    MALE = _("Male")
    FEMALE = _("Female")
    OTHER = _("Other")


def generate_document_filepath(instance: "CustomUser", filename: str) -> str:
    custom_filename = str(uuid4()) + path.splitext(filename)[1]
    return f"user_document/{instance.category}/{custom_filename}"


def generate_profile_filepath(instance: "CustomUser", filename: str) -> str:
    custom_filename = str(uuid4()) + path.splitext(filename)[1]
    return f"user_profile/{instance.id}{custom_filename}"


class CustomUser(AbstractUser):
    """Both indiduals and organizations"""

    email = models.EmailField(_("email address"), blank=False, null=False, unique=True)
    password = models.CharField(_("password"), max_length=88)

    dob = models.DateField(
        verbose_name=_("Date of birth"),
        help_text=_("Date of birth"),
        null=True,
        blank=True,
    )

    gender = models.CharField(
        verbose_name=_("gender"),
        max_length=10,
        help_text=_("Can either be F/M/O"),
        choices=(
            ["Male", Gender.MALE.value],
            ["Female", Gender.FEMALE.value],
            ["Other", Gender.OTHER.value],
        ),
        blank=True,
        default=Gender.OTHER.value,
    )

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
        null=True,
        blank=True,
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

    jobs_applied = models.ManyToManyField(
        "jobs.Job",
        verbose_name=_("Jobs Applied"),
        help_text=_("Jobs that the user has applied for"),
        related_name="applicants",
        blank=True,
    )

    token = models.CharField(
        _("token"),
        help_text=_("Token for validation"),
        null=True,
        blank=True,
        max_length=40,
        unique=True,
    )

    REQUIRED_FIELDS = ["email", "category", "location"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        abstract = False

    def save(self, *args, **kwargs):
        if len(self.password) != 88:
            self.set_password(self.password)
        super().save(*args, **kwargs)
