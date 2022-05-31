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
from operator import itemgetter

from django.core.serializers.json import DjangoJSONEncoder

background_default_image = "https://gymgguns.s3.ap-northeast-2.amazonaws.com/None/background_default.jpg"
profile_default_image = "https://gymgguns.s3.ap-northeast-2.amazonaws.com/None/profile_default.png"


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
        name = ac.UsersInfo.objects.get(UID=UID)
        try:
            obj = Profiles.objects.get(UID=uid_obj)
        except Profiles.DoesNotExist:
            obj = Profiles.objects.create(UID=uid_obj, name=model_to_dict(name)['user_name'],
                                          profileImg=profile_default_image, backgroundImg=background_default_image)
        obj_data = {
            "UID": UID,
            "name": obj.name,
            "subTitle": obj.subTitle,
            "subscribeNum": obj.subscribeNum,
            "profileImg": obj.profileImg,
            "backgroundImg": obj.backgroundImg,
            "subscribed": bool(ProfileSubscribeList.objects.filter(ss_user=UID,
                                                                   pro_user=UID).exists())
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
        if (pf_data['name'] == "") is False:
            name = pf_data['name']
            obj.update(name=name)
            ac.UsersInfo.objects.filter(UID=uid_obj).update(user_name=name)
        if (pf_data['subTitle'] == "") is False:
            subTitle = pf_data['subTitle']
            obj.update(subTitle=subTitle)
        if (pf_data['profileImg'] == "") is False:
            profileImg = image_download(host_id, pf_data['profileImg'])
            obj.update(profileImg=profileImg)
        if (pf_data['backgroundImg'] == "") is False:
            backgroundImg = image_download(host_id, pf_data['backgroundImg'])
            obj.update(backgroundImg=backgroundImg)
        # obj.update(name=name, subTitle=subTitle, profileImg=profileImg, backgroundImg=backgroundImg)
        return JsonResponse({'수정': '성공'}, status=201)
    else:
        return JsonResponse({'에러': 'error'}, status=400)


@csrf_exempt
def makes_portfolios(request):
    if request.method == 'POST':
        pt_data = json.loads(request.body)
        uid_obj = ac.AccountList.objects.get(UID=pt_data['portfolioWriter'])
        pt_title = pt_data['title']
        # pt_writer_profile = Profiles.objects.filter(UID=uid_obj).values('profileImg')
        pt_content = pt_data['content']
        host_id = request.GET.get('host_id')
        image = pt_data['file']
        image_url = image_download(host_id, image)
        Portfolios.objects.create(title=pt_title, portfolioWriter=uid_obj,
                                  content=pt_content, contentImage=image_url)
        return JsonResponse({'생성': '성공'}, status=201)
    else:
        return JsonResponse({'에러': 'error'}, status=400)


@csrf_exempt
def get_portfolios(request, uid):
    if request.method == 'GET':
        try:
            uid_obj = ac.AccountList.objects.get(UID=uid)
            name = ac.UsersInfo.objects.get(UID=uid)
            obj_data = [
                {
                    "title": obj.title,
                    "portfolioWriter": uid,
                    "portfolioWriterName": model_to_dict(name)['user_name'],
                    "content": obj.content,
                    "contentImage": obj.contentImage,
                    "date": obj.created_string,
                    "likeN": obj.likeN,
                    "commentN": obj.commentN,
                    "postN": obj.postN,
                    "liked": bool(PortfolioLikeList.objects.filter(like_user=uid,
                                                                   liked_port=obj.postN).exists())
                } for obj in Portfolios.objects.filter(portfolioWriter=uid_obj)]
            pt_obj = json.dumps(obj_data, cls=DjangoJSONEncoder)
            return HttpResponse(pt_obj)
        except:
            return HttpResponse([])
    else:
        return JsonResponse({'msg': 'error'}, status=400)


def portfolios_get(postN):
    # print(postN)
    obj = Portfolios.objects.get(postN=postN)
    obj_data = {
        "portfolioWriter": model_to_dict(ac.AccountList.objects.get(UID=obj.portfolioWriter))['UID'],
        "portfolioWriterName": model_to_dict(ac.UsersInfo.objects.get(UID=obj.portfolioWriter))['user_name'],
        "title": obj.title,
        "portfolioWriterProfile": model_to_dict(Profiles.objects.get(UID=obj.portfolioWriter))['profileImg'],
        "content": obj.content,
        "contentImage": obj.contentImage,
        "date": obj.created_string,
        "likeN": obj.likeN,
        "commentN": obj.commentN,
        "postN": obj.postN,
        "liked": bool(PortfolioLikeList.objects.filter(like_user=obj.portfolioWriter,
                                                       liked_port=obj.postN).exists())
    }
    # print(obj_data)
    return obj_data


@csrf_exempt
def get_click_portfoilo(request, postN):
    if request.method == 'GET':
        obj = Portfolios.objects.get(postN=postN)
        obj_data = {
            "portfolioWriter": model_to_dict(ac.AccountList.objects.get(UID=obj.portfolioWriter))['UID'],
            "portfolioWriterName": model_to_dict(ac.UsersInfo.objects.get(UID=obj.portfolioWriter))['user_name'],
            "title": obj.title,
            "portfolioWriterProfile": model_to_dict(Profiles.objects.get(UID=obj.portfolioWriter))['profileImg'],
            "content": obj.content,
            "contentImage": obj.contentImage,
            "date": obj.created_string,
            "likeN": obj.likeN,
            "commentN": obj.commentN,
            "postN": obj.postN,
            "liked": bool(PortfolioLikeList.objects.filter(like_user=request.user.username,
                                                           liked_port=obj.postN).exists())
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
        pf = Portfolios.objects.get(postN=data['postN'])
        pf.commentN += 1
        pf.save()
        commentWriterProfile = Profiles.objects.filter(UID=uid_obj).values('profileImg')
        commentN = PortfolioComments.objects.create(commentWriter=uid_obj, commentWriterProfile=commentWriterProfile
                                ,comContent=data['comContent'], postN=data_postN)
        c = {'commentN': commentN.commentN}
        return HttpResponse(json.dumps(c))
    else:
        return JsonResponse({'에러': 'error'}, status=400)


@csrf_exempt
def get_comments(request, postN):
    if request.method == 'GET':
            data_postN = Portfolios.objects.get(postN=postN)
            obj_data = [{
                "commentWriter": model_to_dict(ac.AccountList.objects.get(UID=obj.commentWriter))['UID'],
                "commentWriterName": model_to_dict(ac.UsersInfo.objects.get(UID=obj.commentWriter))['user_name'],
                "commentWriterProfile": model_to_dict(Profiles.objects.get(UID=obj.commentWriter))['profileImg'],
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
        pc = get_object_or_404(PortfolioComments, pk=commentN)
        pf = get_object_or_404(Portfolios, pk=pc.postN_id)
        pf.commentN -= 1
        print(pf.commentN)
        pf.save()
        pc.delete()
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


@csrf_exempt
def subscribe_profile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ss_user = data['ss_user']
        pro_user = data['pro_user']
        profile = get_object_or_404(Profiles, UID=pro_user)

        check_subscribe_profile = ProfileSubscribeList.objects.filter(ss_user=ss_user, pro_user=pro_user)
        if check_subscribe_profile:
            ProfileSubscribeList.objects.get(ss_user=ss_user, pro_user=pro_user).delete()
            profile.subscribeNum -= 1
            profile.save()
            return JsonResponse({'msg': '구독 취소'}, status=201)
        else:
            s_user = ac.AccountList.objects.get(UID=ss_user)
            p_user = ac.AccountList.objects.get(UID=pro_user)
            ProfileSubscribeList.objects.create(ss_user=s_user, pro_user=p_user)
            profile.subscribeNum += 1
            profile.save()
            return JsonResponse({'msg': '구독!~'}, status=201)
    else:
        return JsonResponse({'msg': 'error'}, status=400)


@csrf_exempt
def like_portfolio(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        like_user = data['like_user']
        liked_port = data['postN']
        portfolio = get_object_or_404(Portfolios, postN=liked_port)

        check_like_portfolio = PortfolioLikeList.objects.filter(like_user=like_user, liked_port=liked_port)
        if check_like_portfolio:
            PortfolioLikeList.objects.get(like_user=like_user, liked_port=liked_port).delete()
            portfolio.likeN -= 1
            portfolio.save()
            return JsonResponse({'msg': '포트폴리오 좋아요 취소'}, status=201)
        else:
            l_user = ac.AccountList.objects.get(UID=like_user)
            l_port = Portfolios.objects.get(postN=liked_port)
            PortfolioLikeList.objects.create(like_user=l_user, liked_port=l_port)
            portfolio.likeN += 1
            portfolio.save()
            return JsonResponse({'msg': '포트폴리오 좋아요!~'}, status=201)
    else:
        return JsonResponse({'msg': 'error'}, status=400)


@csrf_exempt
def subscribe_tab(request, uid):
    if request.method == 'GET':
        portfolio_list = []
        for user in ProfileSubscribeList.objects.filter(ss_user=uid):
            portfolio_count = Portfolios.objects.filter(portfolioWriter=user.pro_user).count()
            portfolios = Portfolios.objects.filter(portfolioWriter=user.pro_user).values('postN')
            for count in range(portfolio_count):
                # print(portfolios[count])
                portfolio_list.append(portfolios_get(portfolios[count]['postN']))
        # print(type(portfolio_list[0]))
        portfolio_list = sorted(portfolio_list, key=itemgetter('postN'), reverse=True)
        # print(portfolio_list)
        portfolios_json = json.dumps(portfolio_list)
        return HttpResponse(portfolios_json)
    else:
        return JsonResponse({'msg': 'error'}, status=400)


@csrf_exempt
def image_name(request, uid):
    if request.method == 'GET':
        p = get_object_or_404(Profiles, UID=uid)
        required_list = {
            'name': p.name,
            'profileImg': p.profileImg
        }
        required_list_json = json.dumps(required_list)
        return HttpResponse(required_list_json)
    else:
        return JsonResponse({'msg': 'error'}, status=400)
