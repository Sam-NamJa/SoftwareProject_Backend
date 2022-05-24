from rest_framework import serializers
from .models import *


class ProfilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profiles
        fields = ['uid', 'backgroundImg', 'profileImg', 'name', 'subTitle']


class PortfoliosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolios
        fields = ['uid', 'title', 'portfolioWriter', 'portfolioWriterProfile', 'content', 'contentImage']


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileComments
        fields = ['uid', 'commentWriter', 'comContent', 'postN', 'commentN']



