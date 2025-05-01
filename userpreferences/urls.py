from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', IndexView.as_view(), name='general'),
    path('preference/', PreferenceView.as_view(), name='preferences'),
]