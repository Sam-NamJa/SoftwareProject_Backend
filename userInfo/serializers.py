from rest_framework import serializers
from .models import UserInfo


class UserInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['user_UID',
                  'user_name',
                  'user_age',
                  'user_level',
                  'user_type',
                  'user_purpose',
                  'user_time',
                  'user_number',
                  'created_at',
                  'updated_at',
                  ]