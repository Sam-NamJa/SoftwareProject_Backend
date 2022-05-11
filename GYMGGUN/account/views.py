import json

from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse, HttpResponse

from django.contrib.auth.models import User
from .models import Account

# Create your views here.
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        uid = data['UID']
        try:
            user = Account.objects.get(UID=uid)
        except Account.DoesNotExist: # 번호인증 전 UID 저장
            person = User.objects.create_user(username=uid, password=uid)
            Account.objects.create(user=person, UID=uid)
            return JsonResponse({'UID': "방금 가입함"}, status=201)
    else:
        return HttpResponse(status=400)

@csrf_exempt
def phone(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        uid = data['UID']
        try:
            Account.objects.get(UID=uid)
        except Account.DoesNotExist:
            person = User.objects.create_user(username=uid, password=uid)
            Account.objects.create(user=person, UID=uid)
            # 번호인증 전 UID 저장
            return JsonResponse({'UID': "방금 가입함"}, status=201)
    else:
        return JsonResponse({'msg : error'}, status=400)

@csrf_exempt
def login(request):
    if request.method == 'POST':
