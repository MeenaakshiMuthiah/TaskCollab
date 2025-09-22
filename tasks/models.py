from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

PRIORITY_CHOICES = [
    ("low", "Low"),
    ("medium", "Medium"),
    ("high", "High"),
]

STATUS_CHOICES = [
    ("pending", "Pending"),
    ("completed", "Completed"),
]

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, related_name="created_tasks", on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, related_name="assigned_tasks", on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def is_overdue(self):
        return self.status == "pending" and self.deadline < timezone.now()

    def __str__(self):
        return f"{self.title} ({self.assigned_to})"
