import json

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers

from .models import *
import accounts.models as ac


@login_required
@csrf_exempt
def plan_set(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        plan_name = data['planName']
        uid = data['UID']
        get_uid = ac.AccountList.objects.get(UID=uid)
        PlanList.objects.create(planName=plan_name, UID=get_uid)
        plan = PlanList.objects.filter(planName=plan_name)
        hashtag_list = data['hashTagList']
        for hashTags in hashtag_list:
            if hashTags == '가슴':
                plan.update(hashTagChest=hashTags)
            elif hashTags == '등':
                plan.update(hashTagBack=hashTags)
            elif hashTags == '하체':
                plan.update(hashTagLeg=hashTags)
            elif hashTags == '어깨':
                plan.update(hashTagShoulder=hashTags)
            elif hashTags == '팔':
                plan.update(hashTagArm=hashTags)
            else:
                plan.update(hashTagAir=hashTags)

        routine_list = data['routineList']
        day = 0
        get_plan_name = PlanList.objects.get(planName=plan_name)
        for routine in routine_list:
            day += 1
            workout_list = routine['workoutList']
            for workout in workout_list:
                w_list = WorkoutList.objects.create(planName=get_plan_name, UID=get_uid)
                w_id = w_list.workoutID
                workout_info = WorkoutList.objects.filter(workoutID=w_id)
                workout_name = workout['workoutName']
                set_num = int(workout['setNum'])
                workout_info.update(dayCount=day, workoutName=workout_name, setNum=set_num)
                set_num = 0
                set_list = workout['setList']
                for eachSet in set_list:
                    s_list = SetList.objects.create(UID=get_uid, planName=get_plan_name,
                                                    workoutName=workout_name, setCount=set_num+1)
                    set_num += 1
                    set_id = s_list.id
                    set_info = SetList.objects.filter(id=set_id)
                    if 'cou nt' in eachSet:
                        count = int(eachSet['cou nt'])
                    else:
                        count = int(eachSet['count'])
                    if 'weig ht' in eachSet:
                        weight = int(eachSet['weig ht'])
                    else:
                        weight = int(eachSet['weight'])
                    set_info.update(count=count, weight=weight)
        return JsonResponse({'msg': 'plan 생성'}, status=201)
    else:
        return JsonResponse({'msg': 'error'}, status=400)


@csrf_exempt
def plan_get(request):
    if request.method == 'GET':
        data = json.loads(request.body)
        plan_name = data['planName']
        uid = data['UID']
        name = ac.UsersInfo.objects.get(UID=uid)
        a = [
            {'planName': plan.planName, 'userName': name.user_name, 'likeNum': plan.likeNum}
            for plan in PlanList.objects.all()
        ]
        aj = json.dumps(a)
        print(type(aj))
        print(aj)
        bj = json.loads(aj)
        print(type(bj))
        print(bj)
        return HttpResponse(aj)
    else:
        return JsonResponse({'msg': 'error'}, status=400)

