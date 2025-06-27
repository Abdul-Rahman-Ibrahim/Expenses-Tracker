from datetime import date
import random
from django.contrib.auth.models import User
from .models import Source, Income

users = User.objects.all()
root = users[2]

category_names = ['Salary', 'Gift']
categories = Source.objects.all()

today = date.today()

for _ in range(10):
    category_name = random.choice(category_names)
    category = Source.objects.filter(name=category_name)
    Income.objects.create(
        amount = random.randint(100, 1000),
        date = today,
        description = 'Random',
        owner = root,
        source = category[0]
    )
