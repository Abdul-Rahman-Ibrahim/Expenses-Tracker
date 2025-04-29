from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index_view(request):
    return render(request, 'expenses/index.html')

def add_expenses_view(request):
    return render(request, 'expenses/add_expense.html')
