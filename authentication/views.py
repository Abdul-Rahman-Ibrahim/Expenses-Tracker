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

    