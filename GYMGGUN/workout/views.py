import json

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.db.models import Q

from .models import *
import accounts.models as ac


def hashtag_get(plan):
    tag = []
    if plan.hashTagChest:
        tag.append(plan.hashTagChest)
    if plan.hashTagBack:
        tag.append(plan.hashTagBack)
    if plan.hashTagLeg:
        tag.append(plan.hashTagLeg)
    if plan.hashTagShoulder:
        tag.append(plan.hashTagShoulder)
    if plan.hashTagArm:
        tag.append(plan.hashTagArm)
    if plan.hashTagAir:
        tag.append(plan.hashTagAir)
    return tag


# @login_required
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
        plan.update(planDay=day)
        return JsonResponse({'msg': 'plan 생성'}, status=201)
    else:
        return JsonResponse({'msg': 'error'}, status=400)


# @login_required
@csrf_exempt
def plan_get(request, plan_name):
    if request.method == 'GET':
        plan = get_object_or_404(PlanList, pk=plan_name)
        uid = plan.UID
        tag = hashtag_get(plan)
        plan_detail = {'UID': model_to_dict(uid)['UID'],
                       'hashTagList': tag,
                       'planName': plan.planName,
                       'routineList': [
                           {'workoutList': [
                               {'setList': [
                                   {'count': eachSet.count,
                                    'weight': eachSet.weight
                                    }
                                   for eachSet in SetList.objects.filter(planName=plan_name, workoutName=workout.workoutName)
                                    ],
                                   'setNum': workout.setNum,
                                   'workoutName': workout.workoutName
                                }
                               for workout in WorkoutList.objects.filter(dayCount=day+1, planName=plan_name)
                           ]
                           }
                           for day in range(plan.planDay)
                       ]
                       }
        # print(type(plan_detail['UID']))
        plan_json = json.dumps(plan_detail)
        return HttpResponse(plan_json)
    else:
        return JsonResponse({'msg': 'error'}, status=400)


@csrf_exempt
def plan_get_uid(request, uid):
    if request.method == 'GET':
        plan_list = [
            {
                'planName': plan.planName,
                'hashTagList': hashtag_get(plan),
                'likeNum': plan.likeNum,
                'downloadNum': plan.downloadNum,
                'commentNum': plan.commentNum
            }
            for plan in PlanList.objects.filter(UID=uid)
        ]
        plan_json = json.dumps(plan_list)
        # print(type(plan_json))
        return HttpResponse(plan_json)
    else:
        return JsonResponse({'msg': 'error'}, status=400)


@csrf_exempt
def plan_get_hashtag(request, hashtag):
    if request.method == 'GET':
        plan_list = [
            {
                'planName': plan.planName,
                'hashTagList': hashtag_get(plan),
                'likeNum': plan.likeNum,
                'downloadNum': plan.downloadNum,
                'commentNum': plan.commentNum
            }
            for plan in PlanList.objects.filter(Q(hashTagChest=hashtag) | Q(hashTagBack=hashtag) |
                                                Q(hashTagLeg=hashtag) | Q(hashTagShoulder=hashtag) |
                                                Q(hashTagArm=hashtag) | Q(hashTagAir=hashtag))
        ]
        plan_json = json.dumps(plan_list)
        return HttpResponse(plan_json)
    else:
        return JsonResponse({'msg': 'error'}, status=400)
