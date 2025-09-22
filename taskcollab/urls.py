from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Fixed this line
    path('', include('tasks.urls')),  # Add this line to include your tasks app
]