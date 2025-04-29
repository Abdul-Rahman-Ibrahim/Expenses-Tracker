import re
import json
from validate_email import validate_email

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages

from django.core.mail import EmailMessage

def send_email(rcpt_email):
    subject = 'Activate your account.'
    body = 'Please verify your account'

    email = EmailMessage (
        subject,
        body,
        "abdulrahmanibrahim.ish@gmail.com",
        [rcpt_email],
    )

    email.send(fail_silently=False)


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        print(username)
        return render(request, 'authentication/login.html')

class SignupView(View):
    def get(self, request):
        return render(request, 'authentication/signup.html')
    
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if not PasswordValidationView().check_password_validity(password):
                    messages.error(request, 'Invalid password: Please read password requirements!')
                    return render(request, 'authentication/signup.html', context=context)
                
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                send_email(email)

                messages.success(request, 'Account successfully created!')
            else:
                messages.error(request, 'Email is taken.')
                return render(request, 'authentication/signup.html', context=context)

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