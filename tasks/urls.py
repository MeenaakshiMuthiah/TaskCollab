from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LogoutView, LoginView
from .forms import LoginForm

app_name = "tasks"
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", LoginView.as_view(template_name="tasks/login.html", authentication_form=LoginForm), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("tasks/create/", views.task_create, name="task_create"),
    path("tasks/<int:pk>/edit/", views.task_edit, name="task_edit"),
    path("tasks/<int:pk>/toggle/", views.task_toggle_status, name="task_toggle"),
    path("tasks/export/csv/", views.export_tasks_csv, name="export_csv"),
    

    # path('admin/', admin.site.urls),
    # path('', include('tasks.urls', namespace='tasks')),
]
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('tasks.urls', namespace='tasks')),  # ✅ Include with namespace
# ]