from django.db import models
from django.utils.translation import gettext as _
from enum import Enum

# Create your models here.


class JobTypes(str, Enum):
    FULL_TIME = _("Full-time")
    INTERNSHIP = _("Internship")


class JobCategory(models.Model):
    name = models.CharField(
        _("name"),
        help_text=_("Job category name"),
        max_length=100,
        unique=True,
        blank=False,
    )

    created_on = models.DateTimeField(
        _("date created"), auto_now_add=True, help_text=_("Time it firstly made entry")
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Job(models.Model):
    company = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    category = models.ForeignKey(
        JobCategory, verbose_name=_("Category"), on_delete=models.CASCADE
    )
    title = models.CharField(
        _("title"), help_text=_("Job title"), null=False, blank=False, max_length=100
    )
    type = models.CharField(
        _("type"),
        help_text=_("Can either be Intership or Full-time"),
        choices=(
            ["Full-time", JobTypes.FULL_TIME.value],
            ["Internship", JobTypes.INTERNSHIP.value],
        ),
        default=JobTypes.FULL_TIME.value,
        max_length=30,
    )
    minimum_salary = models.PositiveIntegerField(
        _("minimum salary"),
        help_text=_("The least possible pay"),
        null=False,
        blank=False,
    )

    maximum_salary = models.PositiveIntegerField(
        _("maximum salary"),
        help_text=_("The highest possible pay"),
        null=False,
        blank=False,
    )

    description = models.TextField(
        _("description"),
        help_text=_("Job description in details"),
        null=False,
        blank=False,
    )

    is_available = models.BooleanField(
        _("Is available"), help_text=_("Job availability status"), default=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Updated at"),
        help_text=_("Last time to be modified"),
        auto_now=True,
    )

    created_on = models.DateTimeField(
        _("Date created"),
        help_text=_("Date when the job was initially added"),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _("Job")
        verbose_name_plural = _("Jobs")

    def __str__(self):
        return self.title + " - " + self.company.username or self.company.first_name
