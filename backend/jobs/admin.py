from django.contrib import admin
from jobs.models import JobCategory, Job

# Register your models here.


admin.site.register(JobCategory)

admin.site.register(Job)
