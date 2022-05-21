from django.db import models
from datetime import datetime, timedelta, timezone


class PlanList(models.Model):
    planName = models.CharField(max_length=40, primary_key=True)
    planDay = models.PositiveSmallIntegerField(default=0)
    UID = models.ForeignKey('accounts.AccountList', on_delete=models.CASCADE, db_column='UID')
    user = models.CharField(max_length=20, null=True)
    likeNum = models.PositiveSmallIntegerField(default=0)
    downloadNum = models.PositiveSmallIntegerField(default=0)
    commentNum = models.PositiveSmallIntegerField(default=0)
    hashTagChest = models.CharField(max_length=10, null=True)
    hashTagBack = models.CharField(max_length=10, null=True)
    hashTagLeg = models.CharField(max_length=10, null=True)
    hashTagShoulder = models.CharField(max_length=10, null=True)
    hashTagArm = models.CharField(max_length=10, null=True)
    hashTagAir = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.planName

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'PlanList'
        ordering = ['updated_at']


class WorkoutList(models.Model):
    workoutID = models.AutoField(primary_key=True)
    UID = models.ForeignKey('accounts.AccountList', on_delete=models.CASCADE, db_column='UID')
    planName = models.ForeignKey(PlanList, on_delete=models.CASCADE, db_column='planName', null=True)
    dayCount = models.SmallIntegerField(default=1)
    workoutName = models.CharField(max_length=20)
    setNum = models.SmallIntegerField(blank=True, null=True)
    isComplete = models.SmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.workoutName

    class Meta:
        db_table = 'WorkoutList'
        ordering = ['updated_at']


class SetList(models.Model):
    UID = models.ForeignKey('accounts.AccountList', on_delete=models.CASCADE, db_column='UID')
    planName = models.ForeignKey(PlanList, on_delete=models.CASCADE, db_column='planName')
    workoutName = models.CharField(max_length=20)
    setCount = models.PositiveSmallIntegerField(blank=True, null=True)
    count = models.PositiveSmallIntegerField(blank=True, null=True)
    weight = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.workoutName

    class Meta:
        db_table = 'SetList'


class DownloadList(models.Model):
    download_user = models.ForeignKey('accounts.AccountList', on_delete=models.CASCADE, db_column='download_user', null=True)
    planName = models.ForeignKey(PlanList, on_delete=models.CASCADE, db_column='plan')

    class Meta:
        db_table = 'DownloadList'


class LikeList(models.Model):
    like_user = models.ForeignKey('accounts.AccountList', on_delete=models.CASCADE, db_column='like_user')
    planName = models.ForeignKey(PlanList, on_delete=models.CASCADE, db_column='plan')

    class Meta:
        db_table = 'LikeList'


class Comment(models.Model):
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    UID = models.ForeignKey('accounts.AccountList', on_delete=models.CASCADE, db_column='UID')
    planName = models.ForeignKey(PlanList, on_delete=models.CASCADE, db_column='planName', null=True)

    def __str__(self):
        return self.comment

    class Meta:
        db_table = 'Comment'

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.date
        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.date.date()
            return str(time.days) + '일 전'
        else:
            return False
