from django.http import JsonResponse, HttpResponse
# from django.shortcuts import render

# Create your views here.
from rest_framework.parsers import JSONParser
from .models import UserInfo
from .serializers import UserInfoSerializers
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def info(request):
    if request.method == 'GET':
        query_set = UserInfo.objects.all()
        serializer = UserInfoSerializers(query_set, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        user_info = JSONParser().parse(request)
        serializer = UserInfoSerializers(data=user_info)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def info_detail(request, pk):
    try:
        user = UserInfo.objects.get(pk=pk)
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UserInfoSerializers(user)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserInfoSerializers(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=204)