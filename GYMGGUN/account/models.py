from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class AccountList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    UID = models.CharField(max_length=100, primary_key=True)  # 파이어베이스uid
    user_authentication = models.PositiveSmallIntegerField(blank=True, default=0)  # 번호인증 여부
    user_info_input = models.PositiveSmallIntegerField(blank=True, default=0)  # 상세정보 입력했는지

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.UID

    class Meta:
        db_table = 'AccountList'
        ordering = ['created_at']


class UsersInfo(models.Model):
    # UID와 운동 레벨을 제외하고 기본적으로 null값을 허용하겠음
    UID = models.CharField(max_length=100, primary_key=True)
    # 유저 이름
    user_name = models.CharField(max_length=20, null=True)
    # 나이제한0~200
    user_age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(150)], null=True)
    FRESHMAN = '헬생아'
    SOPHOMORE = '헬린이'
    JUNIOR = '헬스인'
    SENIOR = '헬창'
    USER_LEVEL_CHOICES = [
        ('헬생아', '헬생아'),
        ('헬린이', '헬린이'),
        ('헬스인', '헬스인'),
        ('헬창', '헬창')
    ]
    user_level = models.CharField(max_length=10, choices=USER_LEVEL_CHOICES, default=FRESHMAN)
    # 운동타입(ex 다이어트, 벌크업 등등~)
    user_type = models.CharField(max_length=10, null=True)
    # 유산소, 벌크업 등등
    user_purpose = models.CharField(max_length=10, null=True)
    # 한번 할 때 몇시간?
    workout_time = models.PositiveSmallIntegerField(null=True)
    # 일주일에 몇회??
    workout_per_week = models.PositiveSmallIntegerField(null=True)
    # user_profile_picture = models.ImageField() 유저 프로필 사진 받기?
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.UID

    class Meta:
        db_table = 'UsersInfo'
        ordering = ['updated_at']