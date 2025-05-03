from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.core.paginator import Paginator

from userpreferences.models import UserPreference
from .models import Category, Expense

@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
@method_decorator(never_cache, name='dispatch')
class IndexView(View):
    def get(self, request):

        expenses = Expense.objects.filter(owner=request.user)
        
        preference = None
        if UserPreference.objects.filter(user=request.user).exists():
            preference = UserPreference.objects.get(user=request.user)
            currency = preference.preference.split("-")[0]
            # print(preference.preference)

        PAGE_NUMBER = 2
        page_number = request.GET.get('page')
        paginator = Paginator(expenses, PAGE_NUMBER)
        page_obj =  paginator.get_page(page_number)
        context = {
            'expenses': expenses,
            'preference': currency,
            'page_obj': page_obj
        }
        return render(request, 'expenses/index.html', context=context)

    
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



@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
@method_decorator(never_cache, name='dispatch')
class EditExpenseView(View):
    def get(self, request, id):
        expense = get_object_or_404(Expense, id=id)
        categories = Category.objects.all()
        context = {
            'expense': expense,
            'categories': categories
        }
        return render(request, 'expenses/edit-expense.html', context)

        # try:
        #     expense = Expense.objects.get(id=id)
        #     category = Category.objects.all()
        #     context = {
        #         'expense': expense,
        #         'categories': category
        #     }
        #     return render(request, 'expenses/edit-expense.html', context=context)
        
        # except Expense.DoesNotExist:
        #     messages.error(request, 'That expense does not exist')
        #     return redirect('home')

        # # return render(request, 'expenses/edit-expense.html', context=context)



    def post(self, request, id):
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('date')
        category_id = request.POST.get('category')

        category = Category.objects.get(id=category_id)

        expense = Expense.objects.get(id=id)

        expense.amount = amount
        expense.owner = request.user
        expense.description = description
        expense.date = date
        expense.category = category

        expense.save()
        messages.success(request, 'Expense updated successfully')
        return redirect('home')


@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
@method_decorator(never_cache, name='dispatch')
class DeleteExpenseView(View):
    def post(self, request, id):
        expense = Expense.objects.get(id=id)
        expense.delete()
        messages.success(request, "Expense deleted successfully.")
        return redirect('home')


# @never_cache
# @login_required(login_url='/authentication/login')
# def index_view(request):
#     return render(request, 'expenses/index.html')

# def add_expenses_view(request):
#     return render(request, 'expenses/add_expense.html')
