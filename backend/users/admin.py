from django.contrib import admin
from users.models import CustomUser

# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "category", "email", "date_joined"]
    search_fields = ["username", "first_name", "last_name", "email"]
    list_filter = ["category", "date_joined"]
    ordering = ["-date_joined"]

    exclude = ["last_login", "date_joined"]
