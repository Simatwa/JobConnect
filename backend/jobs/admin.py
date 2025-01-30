from django.contrib import admin # type: ignore
from jobs.models import JobCategory, Job

# Register your models here.


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "created_on"]
    search_fields = ["name"]
    list_filter = ["created_on"]
    ordering = ["-created_on"]


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = [
        "company",
        "category",
        "title",
        "minimum_salary",
        "maximum_salary",
        "updated_at",
    ]
    search_fields = ["title"]
    list_filter = [
        "company",
        "category",
        "minimum_salary",
        "maximum_salary",
        "updated_at",
    ]
    ordering = ["-updated_at"]
