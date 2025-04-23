from django.shortcuts import render

def index_view(request):
    return render(request, 'expenses/index.html')

def add_expenses_view(request):
    return render(request, 'expenses/add_expense.html')
