from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Count, Q
from django.utils import timezone
import csv
from django.contrib.auth import logout

from .forms import SignUpForm, TaskForm
from .models import Task
from django.contrib.auth import get_user_model

User = get_user_model()

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("tasks:dashboard")
    else:
        form = SignUpForm()
    return render(request, "tasks/signup.html", {"form": form})


@login_required
# def dashboard(request):
#     status = request.GET.get("status")
#     order = request.GET.get("order", "deadline")

#     # All tasks for this user (for analytics)
#     all_tasks = Task.objects.filter(Q(created_by=request.user) | Q(assigned_to=request.user)).distinct()

#     # Counts for analytics
#     pending_count = all_tasks.filter(status="pending").count()
#     completed_count = all_tasks.filter(status="completed").count()

#     # Apply filters for the displayed tasks
#     tasks_qs = all_tasks
#     if status in ["pending", "completed"]:
#         tasks_qs = tasks_qs.filter(status=status)

#     if order == "priority":
#         tasks_qs = tasks_qs.order_by("priority")
#     else:
#         tasks_qs = tasks_qs.order_by("deadline")

#     context = {
#         "tasks": tasks_qs,
#         "pending_count": pending_count,
#         "completed_count": completed_count,
#         "now": timezone.now(),
#     }
#     return render(request, "tasks/dashboard.html", context)

def dashboard(request):
    status = request.GET.get("status")
    order = request.GET.get("order", "deadline")

    if request.user.is_authenticated:
        # Tasks for logged-in user (created or assigned)
        all_tasks = Task.objects.filter(Q(created_by=request.user) | Q(assigned_to=request.user)).distinct()
    else:
        # Tasks for anonymous users: show all tasks or only public ones if you have a 'public' field
        all_tasks = Task.objects.all()  # Or add filter(public=True) if you have a public flag

    # Counts for analytics
    pending_count = all_tasks.filter(status="pending").count()
    completed_count = all_tasks.filter(status="completed").count()

    # Apply filters for displayed tasks
    tasks_qs = all_tasks
    if status in ["pending", "completed"]:
        tasks_qs = tasks_qs.filter(status=status)

    if order == "priority":
        tasks_qs = tasks_qs.order_by("-priority")  # usually high priority first
    else:
        tasks_qs = tasks_qs.order_by("deadline")

    context = {
        "tasks": tasks_qs,
        "pending_count": pending_count,
        "completed_count": completed_count,
        "now": timezone.now(),
    }
    return render(request, "tasks/dashboard.html", context)

@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            return redirect("tasks:dashboard")
    else:
        form = TaskForm()
        form.fields["assigned_to"].queryset = User.objects.all()
    return render(request, "tasks/task_form.html", {"form": form, "action": "Create"})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.user != task.created_by and request.user != task.assigned_to:
        return redirect("tasks:dashboard")
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("tasks:dashboard")
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/task_form.html", {"form": form, "action": "Edit"})

@login_required
def task_toggle_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.user == task.assigned_to or request.user == task.created_by:
        task.status = "completed" if task.status != "completed" else "pending"
        task.save()
    return redirect("tasks:dashboard")

@login_required
def export_tasks_csv(request):
    tasks = Task.objects.filter(Q(created_by=request.user) | Q(assigned_to=request.user)).distinct()

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="tasks.csv"'

    writer = csv.writer(response)
    writer.writerow(["Title","Description","Created By","Assigned To","Deadline","Priority","Status","Created At"])
    for t in tasks:
        writer.writerow([t.title, t.description, t.created_by.username, t.assigned_to.username, t.deadline, t.priority, t.status, t.created_at])
    return response
def logout_view(request):
    logout(request)
    return redirect("tasks:login")