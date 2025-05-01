from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('add_expense/', AddExpenseView.as_view(), name='add_expense'),
]