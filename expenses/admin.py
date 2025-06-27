from django.contrib import admin
from .models import Category, Expense

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('amount', 'description', 'owner', 'category', 'date')
    search_fields = ('description', 'date', 'owner__username', 'category__name')
    list_per_page = 5

admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category)