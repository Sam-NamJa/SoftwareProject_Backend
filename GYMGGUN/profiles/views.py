from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from rest_framework.parsers import JSONParser
from django.shortcuts import get_object_or_404
from django.db.models import Q
from GYMGGUN.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, IMAGE_URL
from django.forms.models import model_to_dict

import accounts.models as ac
import json, boto3, base64, string, random

from django.core.serializers.json import DjangoJSONEncoder

default_image = "https://gymggun.s3.ap-northeast-2.amazonaws.com/None/default.png"

def image_download(host_id, image): # 사진 다운받는 함수
    # header, data = image.split(';base64,')
    # data_format, ext = header.split('/')
    n = 50
    rand_str = ""
    for i in range(n):
        rand_str += str(random.choice(string.ascii_uppercase + string.digits))
    file_data = base64.b64decode(image)
    file_name = rand_str + ".png"
    s3r = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    key = "%s" % (host_id)
    s3r.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key=key + '/%s' % (file_name), Body=file_data, ContentType=".png")
    return IMAGE_URL + "%s/%s" % (host_id, file_name)


@csrf_exempt
def get_profile(request, UID):
    if request.method == 'GET':
        uid_obj = ac.AccountList.objects.get(UID=UID)
        try:
            obj = Profiles.objects.get(UID=uid_obj)
        except Profiles.DoesNotExist:
            obj = Profiles.objects.create(UID=uid_obj, profileImg=default_image, backgroundImg=default_image)
        obj_data = {
            "UID": UID,
            "name": obj.name,
            "subTitle": obj.subTitle,
            "subscribeNum": obj.subscribeNum,
            "profileImg": obj.profileImg,
            "backgroundImg": obj.backgroundImg
        }
        pf_obj = json.dumps(obj_data)
        return HttpResponse(pf_obj)
    else:
        return JsonResponse({'msg': 'error'}, status=400)


@csrf_exempt
def modify_profile(request, UID):
    host_id = request.GET.get('host_id')
    if request.method == "PUT":
        pf_data = json.loads(request.body)
        uid_obj = ac.AccountList.objects.get(UID=UID)
        obj = Profiles.objects.filter(UID=uid_obj)
        if pf_data['name'] is None:
            name = obj.values('subTitle')
        else:
            name = pf_data['name']
        if pf_data['subTitle'] is None:
            subTitle = obj.values('subTitle')
        else:
            subTitle = pf_data['subTitle']
        if pf_data['profileImg'] == "":
            profileImg = default_image
        else:
            profileImg = image_download(host_id, pf_data['profileImg'])
        if pf_data['backgroundImg'] == "":
            backgroundImg = default_image
        else:
            backgroundImg = image_download(host_id, pf_data['backgroundImg'])
        obj.update(name=name, subTitle=subTitle,
                   profileImg=profileImg, backgroundImg=backgroundImg)
        return JsonResponse({'수정': '성공'}, status=201)
    else:
        return JsonResponse({'에러': 'error'}, status=400)


@csrf_exempt
def makes_portfolios(request):
    if request.method == 'POST':
        pt_data = json.loads(request.body)
        uid_obj = ac.AccountList.objects.get(UID=pt_data['portfolioWriter'])
        pt_title = pt_data['title']
        pt_writer_profile = Profiles.objects.filter(UID=uid_obj).values('profileImg')
        pt_content = pt_data['content']
        host_id = request.GET.get('host_id')
        image = pt_data['file']
        image_url = image_download(host_id, image)
        Portfolios.objects.create(title=pt_title, portfolioWriter=uid_obj
                                  , portfolioWriterProfile=pt_writer_profile,
                                  content=pt_content, contentImage=image_url)
        return JsonResponse({'생성': '성공'}, status=201)
    else:
        return JsonResponse({'에러': 'error'}, status=400)


@csrf_exempt
def get_portfolios(request, uid):
    if request.method == 'GET':
        try:
            uid_obj = ac.AccountList.objects.get(UID=uid)
            obj_data = [
                {
                    "title": obj.title,
                    "portfolioWriter": uid,
                    "portfolioWriterProfile": obj.portfolioWriterProfile,
                    "content": obj.content,
                    "contentImage": obj.contentImage,
                    "date": obj.date,
                    "likeN": obj.likeN,
                    "commentN": obj.commentN,
                    "postN": obj.postN
                } for obj in Portfolios.objects.filter(portfolioWriter=uid_obj)]
            pt_obj = json.dumps(obj_data, cls=DjangoJSONEncoder)
            return HttpResponse(pt_obj)
        except:
            return HttpResponse(status=204)
    else:
        return JsonResponse({'msg': 'error'}, status=400)


@csrf_exempt
def get_click_portfoilo(request, postN):
    if request.method == 'GET':
        obj = Portfolios.objects.get(postN=postN)
        obj_data = {
            "portfolioWriter": model_to_dict(ac.AccountList.objects.get(UID=obj.portfolioWriter))['UID'],
            "title": obj.title,
            "portfolioWriterProfile": obj.portfolioWriterProfile,
            "content": obj.content,
            "contentImage": obj.contentImage,
            "date": obj.created_string,
            "likeN": obj.likeN,
            "commentN": obj.commentN,
            "postN": obj.postN
            }
        pt_obj = json.dumps(obj_data)
        return HttpResponse(pt_obj)
    else:
        return JsonResponse({'msg': 'error'}, status=400)


@csrf_exempt
def modify_portfolios(request, postN):
    if request.method == 'GET':
        obj = Portfolios.objects.get(postN=postN)
        obj_data = {
                    "title": obj.title,
                    "content": obj.content,
                    "contentImage": obj.contentImage
        }
        pt_obj = json.dumps(obj_data)
        return HttpResponse(pt_obj)
    elif request.method == 'PUT':
        pt_data = json.loads(request.body)
        obj = Portfolios.objects.filter(postN=postN)
        obj.update(title=pt_data['title'], content=pt_data['content'],  contentImage=pt_data['contentImage'])
        return JsonResponse({'업데이트': '성공'}, status=201)
    else:
        return JsonResponse({'에러': 'error'}, status=400)


@csrf_exempt
def delete_portfolios(request, postN):
    if request.method == 'DELETE':
        Portfolios.objects.get(postN=postN).delete()
        return JsonResponse({'삭제': '성공'}, status=201)
    else:
        return JsonResponse({'에러': 'error'}, status=400)


@csrf_exempt
def post_comments(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        uid_obj = ac.AccountList.objects.get(UID=data['commentWriter'])
        data_postN = Portfolios.objects.get(postN=data['postN'])
        commentWriterProfile = Profiles.objects.filter(UID=uid_obj).values('profileImg')
        PortfolioComments.objects.create(commentWriter=uid_obj, commentWriterProfile=commentWriterProfile
                                ,comContent=data['comContent'], postN=data_postN)
        return JsonResponse({'생성': '성공'}, status=201)
    else:
        return JsonResponse({'에러': 'error'}, status=400)


@csrf_exempt
def get_comments(request, postN):
    if request.method == 'GET':
            data_postN = Portfolios.objects.get(postN=postN)
            obj_data = [{
                "commentWriter": model_to_dict(ac.AccountList.objects.get(UID=obj.commentWriter))['UID'],
                "commentWriterProfile": obj.commentWriterProfile,
                "commentDate": obj.created_string,
                "comContent": obj.comContent,
                "commentN": obj.commentN
            }for obj in PortfolioComments.objects.filter(postN=data_postN)]
            ct_obj = json.dumps(obj_data, cls=DjangoJSONEncoder)
            return HttpResponse(ct_obj)
    else:
        return JsonResponse({'에러': 'error'}, status=400)


@csrf_exempt
def delete_comments(request, commentN):
    if request.method == 'DELETE':
        PortfolioComments.objects.get(commentN=commentN).delete()
        return JsonResponse({'삭제': '성공'}, status=201)
    else:
        return JsonResponse({'에러': 'error'}, status=400)


@csrf_exempt
def post_image(request):
    try:
        file = request.FILES.get('file')
        host_id = request.GET.get('host_id')
        s3r = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        key = "%s" % (host_id)

        # file._set_name(str(uuid.uuid4()))
        s3r.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key=key + '/%s' % (file), Body=file, ContentType='png')
        Image.objects.create(
            image=IMAGE_URL + "%s/%s" % (host_id, file)
        )
        return JsonResponse({"MESSGE": "SUCCESS"}, status=200)

    except:
        return JsonResponse({"ERROR": 'error'})