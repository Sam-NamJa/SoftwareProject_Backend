import json

from django.contrib import auth
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse

from django.contrib.auth.models import User
from .models import *


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        uid = data['UID']
        print(uid)
        try:
            AccountList.objects.get(UID=uid)
            return JsonResponse({'msg': 'already signup'}, status=400)
        except AccountList.DoesNotExist: # 번호인증 전 UID 저장
            person = User.objects.create_user(username=uid, password=uid)
            user = AccountList.objects.create(user=person, UID=uid)
            UsersInfo.objects.create(UID=user.UID)
            return JsonResponse({'msg': 'success to signup'}, status=201)
    else:
        return JsonResponse({'msg': 'request method error'}, status=400)


@csrf_exempt
def phone(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        uid = data['UID']
        try:
            noob = AccountList.objects.get(UID=uid)
            print(noob.UID)
            if noob.user_authentication == 0:
                AccountList.objects.filter(UID=uid).update(user_authentication=1)
                return JsonResponse({'msg': 'phone authentication success'}, status=201)
            return JsonResponse({'msg': 'already phone authentication'}, status=201)
        except AccountList.DoesNotExist:
            return JsonResponse({'msg': 'not exist user'}, status=400)
    else:
        return JsonResponse({'msg': 'request method error'}, status=400)


@csrf_exempt
def login(request):
    if request.user.is_authenticated:
        return JsonResponse({'msg': '이미 로그인되어 있습니다.'}, status=400)

    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        uid = data['UID']
        try:
            person = AccountList.objects.get(UID=uid)
            # print(person.UID)
            user = auth.authenticate(username=uid, password=uid)
            if person.user_authentication == 1:
                if person.user_info_input == 1:
                    if user is not None:
                        auth.login(request, user)
                        print('login user : ' + uid)
                        return JsonResponse({'msg': 'login success!!'}, status=200)
                else:
                    return JsonResponse({'msg': 'info URL plz'}, status=400)
            else:
                return JsonResponse({'msg': 'phone URL plz'}, status=400)
        except AccountList.DoesNotExist:
            return JsonResponse({'msg': 'signup URL plz'}, status=400)
    else:
        return JsonResponse({'msg': 'request method error'}, status=400)


@csrf_exempt
def logout(request): #로그아웃
    if request.user.is_authenticated:
        auth.logout(request)
        return JsonResponse({"message": "logout success"}, status=200)
    else:
        return JsonResponse({"message": "already logout"}, status=400)


@csrf_exempt
def info(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        uid = data['UID']
        account = AccountList.objects.filter(UID=uid)
        user = UsersInfo.objects.filter(UID=uid)
        try:
            user_name = data['user_name']
            user_age = int(data['user_age'])
            user_level = data['user_level']
            user_type = data['user_type']
            user_purpose = data['user_purpose']
            workout_time = int(data['workout_time'])
            workout_per_week = int(data['workout_per_week'])

            user.update(user_name=user_name)
            user.update(user_age=user_age)
            user.update(user_level=user_level)
            user.update(user_type=user_type)
            user.update(user_purpose=user_purpose)
            user.update(workout_time=workout_time)
            user.update(workout_per_week=workout_per_week)
            user.update(updated_at=timezone.localtime())
            account.update(user_info_input=1)
            return JsonResponse({'msg': 'info save success'}, status=201)
        except AccountList.DoesNotExist:
            return JsonResponse({'msg': 'not exist user'}, status=400)
    else:
        return JsonResponse({'msg': 'request method error'}, status=400)
