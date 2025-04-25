import re
import json
from validate_email import validate_email

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User

class SignupView(View):
    def get(self, request):
        return render(request, 'authentication/signup.html')


class EmailFieldView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Email already exists'}, status=409)
        return JsonResponse({'email_valid': True})


class UserNameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'sorry username already used'}, status=409)
        return JsonResponse({'username_valid': True})


class PasswordValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        password = data['password']

        password_validity_message = (
            "Password requirements:\n"
            "- Should have at least one number\n"
            "- Should have at least one uppercase and one lowercase character\n"
            "- Should have at least one special symbol\n"
            "- Should be between 6 to 20 characters long"
        )


        password_valid = self.check_password_validity(password)
        if not password_valid:
            return JsonResponse({'password_invalid': password_validity_message}, status=400)
        return JsonResponse({'password_valid': True})
        
    
    @staticmethod
    def check_password_validity(passwd):
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        pat = re.compile(reg)               
        mat = re.search(pat, passwd)
        
        if mat:
            return True
        return False