from django.db import models

# Create your models here.
class UserInfo(models.Model):
    user_UID = models.CharField(max_length=100,default='')

    user_name = models.CharField(max_length=10)  # 이름
    user_age = models.CharField(max_length=100)  # 나이
    user_level = models.CharField(max_length=40)  # 운동수준
    user_type = models.CharField(max_length=40)
    user_purpose = models.CharField(max_length=40)
    user_time = models.CharField(max_length=20)
    user_number = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'UserInfo'
        ordering = ('user_UID',) #UID순에 따라 저장되도록