from django.urls import path
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .views import *

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>/', VerificationView.as_view(), name='activate'),
    path('validate-username/', csrf_exempt(UserNameValidationView.as_view()), name='validate_username'),
    path('validate-email/', csrf_exempt(EmailFieldView.as_view()), name='validate_email'),
    path('validate-password/', csrf_exempt(PasswordValidationView.as_view()), name='validate_password'),
    path('reset-password/', csrf_exempt(RequestPasswordResetEmail.as_view()), name='reset-password'),
    path('new-password/<uidb64>/<token>/', ResetPasswordVerificationView.as_view(), name='new-password'),
]