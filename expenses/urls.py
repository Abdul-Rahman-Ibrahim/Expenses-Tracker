from django.urls import path
from .views import *

urlpatterns = [
    path('', index_view, name='home'),
    path('add_expense/', add_expenses_view, name='add_expense'),
]