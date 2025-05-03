from datetime import date
import random
from django.contrib.auth.models import User
from .models import Category, Expense

users = User.objects.all()
root = users[2]

category_names = ['Travel', 'Food', 'Insurance', 'Family']
categories = Category.objects.all()

today = date.today()

for _ in range(10):
    category_name = random.choice(category_names)
    category = Category.objects.filter(name=category_name)
    Expense.objects.create(
        amount = random.randint(100, 1000),
        date = today,
        description = 'Random',
        owner = root,
        category = category[0]
    )
