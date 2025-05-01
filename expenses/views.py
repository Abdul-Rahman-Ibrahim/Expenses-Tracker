from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
@method_decorator(never_cache, name='dispatch')
class IndexView(View):
    def get(self, request):
        return render(request, 'expenses/index.html')
    

@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
@method_decorator(never_cache, name='dispatch')
class AddExpenseView(View):
    def get(self, request):
        return render(request, 'expenses/add_expense.html')

# @never_cache
# @login_required(login_url='/authentication/login')
# def index_view(request):
#     return render(request, 'expenses/index.html')

# def add_expenses_view(request):
#     return render(request, 'expenses/add_expense.html')
