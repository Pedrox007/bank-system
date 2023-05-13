from django.urls import path

from core.views import create_account

urlpatterns = [
    path('create-account/',
         create_account,
         name='create-account'),
]
