from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Income(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    source = models.ForeignKey(
            to='Source',
            on_delete=models.SET_NULL,
            null=True,  # Allow expenses to exist even if category is deleted
            blank=True)
    def __str__(self) -> str:
        return f'{self.source.name if self.source else 'No Source'}'
    
    class Meta:
        ordering = ['-date']


class Source(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Sources'
    
    def __str__(self) -> str:
        return self.name
    
