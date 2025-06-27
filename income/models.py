from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Income(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    income_category = models.ForeignKey(
            to='Income_Category',
            on_delete=models.SET_NULL,
            null=True,  # Allow expenses to exist even if category is deleted
            blank=True)
    def __str__(self) -> str:
        return f'{self.income_category.name if self.income_category else 'No Category'}'
    
    class Meta:
        ordering = ['-date']


class Income_Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Income Categories'
    
    def __str__(self) -> str:
        return self.name
    
