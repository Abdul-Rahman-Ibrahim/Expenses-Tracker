from django.shortcuts import render
from django.views import View

class SignupView(View):
    def get(self, request):
        return render(request, 'authentication/signup.html')
    