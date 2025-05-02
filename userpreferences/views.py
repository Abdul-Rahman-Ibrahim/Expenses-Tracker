import json
import os
from django.shortcuts import render, redirect
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.contrib import messages
from .models import UserPreference

@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
@method_decorator(never_cache, name='dispatch')
class IndexView(View):
    def get(self, request):
        currency_data = []
        json_path = os.path.join(settings.BASE_DIR, 'currencies.json')
        with open(json_path, 'r') as file:
            content = json.load(file)
        for key, value in content.items():
            currency_data.append({'name': key, 'value': value})
        # import pdb
        # pdb.set_trace()
        user_preferences = None
        if UserPreference.objects.filter(user=request.user).exists():
            user_preferences = UserPreference.objects.get(user=request.user)
            
        
        return render(request, 'preferences/index.html', context={'currencies': currency_data, 'user_preferences': user_preferences})


class PreferenceView(View):
        
    def post(self, request):
        user_preference_exist = UserPreference.objects.filter(user=request.user).exists()

        currency = request.POST.get('currency')
        if user_preference_exist:
            user_preferences = UserPreference.objects.get(user=request.user)
            user_preferences.preference = currency
            user_preferences.save()
            messages.success(request, 'Preference saved')
            # print(user_preferences.preference)
            # print(currency)
            return redirect('general')
        
        UserPreference.objects.create(user=request.user, preference=currency)
        user_preferences = UserPreference.objects.get(user=request.user)
        # print(user_preferences.preference)
        # print(currency)
        messages.success(request, 'Preference saved')
        return redirect('general')


# @never_cache
# @login_required(login_url='/authentication/login')
# def index_view(request):
#     return render(request, 'preferences/index.html')
