from django.urls import path
from .views import IncomeView, AddIncomeView, EditIncomeView, DeleteIncomeView

urlpatterns = [
    path('', IncomeView.as_view(), name='income'),
    path('add_income/', AddIncomeView.as_view(), name='add_income'),
    path('edit_income/<int:id>', EditIncomeView.as_view(), name='edit_income'),
    path('delete_income/<int:id>', DeleteIncomeView.as_view(), name='delete_income'),
]