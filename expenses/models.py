from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
    to='Category',
    on_delete=models.SET_NULL,
    null=True,  # Allow expenses to exist even if category is deleted
    blank=True)

    def __str__(self) -> str:
        return f"{self.category.name if self.category else 'No Category'}"

    
    class Meta:
        ordering = ['-date']
        
    
class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.name
