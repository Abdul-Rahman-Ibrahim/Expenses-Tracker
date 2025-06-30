import re
import json
from validate_email import validate_email

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.urls import reverse
from django.http import HttpResponse

from django.core.mail import EmailMessage

from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

from .utils import token_generator

def send_email(activate_url, user):
    subject = 'Activate your account.'
    body = f'Hi {user.username}\n. Please use this link {activate_url} to verify your account.'

    email = EmailMessage (
        subject,
        body,
        "abdulrahmanibrahim.ish@gmail.com",
        [user.email],
    )

    email.send(fail_silently=False)


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

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
                activate_url = 'http://'+ domain + link

                send_email(activate_url, user)

                messages.success(request, 'Account successfully created!')
            else:
                messages.error(request, 'Email is taken.')
                return render(request, 'authentication/signup.html', context=context)
        
        else:
            messages.error(request, 'User name is taken!')
            return render(request, 'authentication/signup.html', context=context)

        return render(request, 'authentication/signup.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        context = {
            "fieldValues": request.POST
        }

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, f'Welcome {username}. You are now logged in')
                    return redirect('home')
                else:
                    messages.error(request, 'Account is not active, please check your email')
                    return render(request, 'authentication/login.html', context=context)
            else:
                messages.error(request, f'Invalid credentials')
                return render(request, 'authentication/login.html', context=context)
        
        else:
            return render(request, 'authentication/login.html', context=context)


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('login')


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
    

class VerificationView(View):
    def get(self, request, uidb64, token):
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)

        if not token_generator.check_token(user, token):
            return HttpResponse('<h1>Verification Link Expired</h1>')

        if user.is_active:
            return redirect(reverse('login'))
        
        user.is_active = True
        user.save()

        messages.success(request, 'Account activated succesfully')
        return redirect(reverse('login'))
    

class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')
    
    def post(self, request):
        email = request.POST.get('email')
        context = {
            'fieldValues': request.POST,
        }
        if not validate_email(email):
            messages.error(request, 'Email is invalid!')
            return render(request, 'authentication/reset-password.html', context=context)

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            domain = get_current_site(request).domain
            link = reverse('new-password', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
            activate_url = 'http://'+ domain + link

            send_email(activate_url, user)
            messages.success(request, 'Check your email!')
        else:
            messages.error(request, 'Email is not registered!')
            return render(request, 'authentication/reset-password.html', context=context)
        
        return render(request, 'authentication/reset-password.html')
    

class ResetPasswordVerificationView(View):
    def get(self, request, uidb64, token):
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)
        #always check whether token has been re-used. PasswordTokenGenerator can do that. refer to chatgpt

        if not token_generator.check_token(user, token):
            return HttpResponse('<h1>Verification Link Expired</h1>')
        
        context = {
            'user': user,
            'uidb64': uidb64,
            'token': token,
        }
        
        print('Here')
        return render(request, 'authentication/new-password-form.html', context=context)
    
    def post(self, request, uidb64, token):
        password = request.POST['password']
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)

        if not token_generator.check_token(user, token):
            return HttpResponse('<h1>Verification Link Expired</h1>')

        user.set_password(password)  # Use set_password for proper hashing
        user.save()

        messages.success(request, 'Password has been reset successfully. You can now log in.')
        return redirect('login')