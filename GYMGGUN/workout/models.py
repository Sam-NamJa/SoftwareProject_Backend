from django.db import models

class PlanList(models.Model):
    planName = models.CharField(max_length=40, primary_key=True)
    UID = models.CharField(max_length=20)
    like = models.SmallIntegerField(default=0)
    download = models.SmallIntegerField(default=0)
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
    UID = models.CharField(max_length=20)
    # UID = models.ForeignKey('account.AccountList', on_delete=models.CASCADE, db_column='UID')
    planName = models.ForeignKey(PlanList, on_delete=models.CASCADE)
    dayCount = models.SmallIntegerField(default=1)
    workoutName = models.CharField(max_length=20)
    set = models.SmallIntegerField(blank=True, null=True)
    times = models.SmallIntegerField(blank=True, null=True)
    weight = models.SmallIntegerField(blank=True, null=True)
    isComplete = models.SmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.planName

    class Meta:
        db_table = 'WorkoutList'
        ordering = ['updated_at']

class SetList(models.Model):
    UID = models.CharField(max_length=20)

