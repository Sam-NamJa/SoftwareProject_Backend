from django.urls import path
from . import views


urlpatterns = [
    path('planSet', views.plan_set), # 플랜 작성 POST
    path('plan/share/', views.plan_share_all), # 플랜 공유 탭에 모든 플랜 전송 GET
    path('plan/all/', views.plan_get_all), # 다운로드한 플랜까지 합쳐서 보내주기
    path('planGet/<plan_name>', views.plan_get), # 플랜 이름으로 세부정보 보내줌 GET
    path('planGet', views.plan_get_uid), # uid로 로그인한 사람이 보유한 plan all GET
    path('planDel/<plan_name>', views.plan_del), # planName으로 삭제 DELETE
    path('planGetHashTag/<hashtag>', views.plan_get_hashtag), # 해쉬태그 버튼 누르면 그 해시태그가지고 있는 플랜들 전송 GET
    path('plan/like', views.like_plan), # plan like POST
    path('plan/download', views.download_plan), # plan download POST
    # path('plan/download/<uid>/UID', views.download_plan_get), # 해당 uid가 다운로드한 플랜들 전송 GET
    path('plan/comment', views.comment_plan), # 해당 플랜에 댓글 작성 POST
    path('plan/comment/<plan_name>', views.comment_plan_get), # plan에 달린 댓글들 모두 전송
]
