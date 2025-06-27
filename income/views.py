from django.shortcuts import render, redirect
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

from .models import Income, Income_Category
from userpreferences.models import UserPreference

class IncomeView(View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        incomes = Income.objects.filter(owner=request.user)

        if search_query:
            incomes = incomes.filter(
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query) |
                Q(amount__icontains=search_query)
            )

        preference = ''
        if UserPreference.objects.filter(user=request.user).exists():
            preference = UserPreference.objects.get(user=request.user)
            preference = preference.preference.split("-")[0]

        PAGE_NUMBER = 5
        page_number = request.GET.get('page')
        paginator = Paginator(incomes.order_by('-date'), PAGE_NUMBER)
        page_obj = paginator.get_page(page_number)

        context = {
            'incomes': incomes,
            'preference': preference,
            'page_obj': page_obj,
            'search_query': search_query
        }
        return render(request, 'income/index.html', context=context)
    

@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
@method_decorator(never_cache, name='dispatch')
class AddIncomeView(View):
    def get(self, request):
        
        context = {
            'categories': Income_Category.objects.all()
        }

        # import pdb
        # pdb.set_trace()
        return render(request, 'income/add_income.html', context=context)
    
    def post(self, request):
        amount = request.POST.get("amount")
        description = request.POST.get("description")
        category_id = request.POST.get("category")
        date = request.POST.get("income_date")

        category = Income_Category.objects.get(id=category_id)

        Income.objects.create(
            amount=amount,
            description=description,
            income_category=category,
            owner=request.user,
            date=date
        )

        messages.success(request, "Income added successfully!")
        return redirect('income')


@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
@method_decorator(never_cache, name='dispatch')
class EditIncomeView(View):
    def get(self, request, id):
        income = get_object_or_404(Income, id=id)
        categories = Income_Category.objects.all()
        context = {
            'income': income,
            'categories': categories
        }
        return render(request, 'income/edit-income.html', context)



    def post(self, request, id):
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('date')
        category_id = request.POST.get('category')

        category = Income_Category.objects.get(id=category_id)

        income = Income.objects.get(id=id)

        income.amount = amount
        income.owner = request.user
        income.description = description
        income.date = date
        income.income_category = category

        income.save()
        messages.success(request, 'Income updated successfully')
        return redirect('income')
    

@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
@method_decorator(never_cache, name='dispatch')
class DeleteIncomeView(View):
    def post(self, request, id):
        income = Income.objects.get(id=id)
        income.delete()
        messages.success(request, "Income deleted successfully.")
        return redirect('income')
    


