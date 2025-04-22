from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('add_expense/', add_expenses, name='add_expense'),
]