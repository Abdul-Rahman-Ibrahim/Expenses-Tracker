from django.shortcuts import render, redirect
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages

from .models import Category, Expense

@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
@method_decorator(never_cache, name='dispatch')
class IndexView(View):
    def get(self, request):
        return render(request, 'expenses/index.html')
    

@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
@method_decorator(never_cache, name='dispatch')
class AddExpenseView(View):
    def get(self, request):
        
        context = {
            'categories': Category.objects.all()
        }

        # import pdb
        # pdb.set_trace()
        return render(request, 'expenses/add_expense.html', context=context)
    
    def post(self, request):
        amount = request.POST.get("amount")
        description = request.POST.get("description")
        category_id = request.POST.get("category")
        date = request.POST.get("expense_date")

        category = Category.objects.get(id=category_id)

        # Create and save new Expense
        Expense.objects.create(
            amount=amount,
            description=description,
            category=category,
            owner=request.user,
            date=date
        )

        messages.success(request, "Expense added successfully!")
        return redirect('home')






# @never_cache
# @login_required(login_url='/authentication/login')
# def index_view(request):
#     return render(request, 'expenses/index.html')

# def add_expenses_view(request):
#     return render(request, 'expenses/add_expense.html')
