from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "assigned_to", "status", "deadline", "priority", "created_by")
    list_filter = ("status", "priority", "deadline")
    search_fields = ("title", "description")
