from django.urls import path
from .views import register_view, registration_success

urlpatterns = [
    path('register/', register_view, name='register'),
    path('success/', registration_success, name='registration_success'),
]