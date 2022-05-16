import json

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required

from .models import *

@login_required
@csrf_exempt
def planSet(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        planName = data['planName']
        UID = data['UID']
        PlanList.objects.create(planName=planName, UID=UID)

        plan = PlanList.objects.filter(planName=planName)
        hashTagList = data['hashTagList']
        for hashTags in hashTagList:
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

        routineList = data['routineList']
        day = 0
        planName2 = PlanList.objects.get(planName=planName)
        for routine in routineList:
            day += 1
            for workout in routine:
                new = WorkoutList.objects.create(planName=planName2, UID=UID)
                wID = new.workoutID
                workoutInfo = WorkoutList.objects.filter(workoutID=wID)
                workoutInfo.update(dayCount=day)
                workoutList = workout['workoutList']
                for eachSet in workoutList:
                    workoutName = workout['workoutName']
                    set = int(workout['setNum'])
                times = int(workout['count'])
                weight = int(workout['weight'])
                workoutInfo.update(workoutName=workoutName)
                workoutInfo.update(set=set)
                workoutInfo.update(times=times)
                workoutInfo.update(weight=weight)
        return JsonResponse({'msg': 'plan생성'}, status=201)
    else:
        return JsonResponse({'msg': 'error'}, status=400)