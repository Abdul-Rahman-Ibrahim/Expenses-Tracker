from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import *

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('validate-username/', csrf_exempt(UserNameValidationView.as_view()), name='validate_username'),
]