from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('add_expense/', AddExpenseView.as_view(), name='add_expense'),
    path('edit_expense/<int:id>', EditExpenseView.as_view(), name='edit_expense'),
    path('delete_expense/<int:id>', DeleteExpenseView.as_view(), name='delete_expense'),
    # path('search_expense/', SearchView.as_view(), name='search_expense'),
]