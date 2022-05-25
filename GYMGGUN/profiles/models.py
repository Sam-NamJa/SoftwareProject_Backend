from django.db import models
from datetime import datetime, timedelta, timezone

class Profiles(models.Model):
    UID = models.ForeignKey("accounts.AccountList", on_delete=models.CASCADE,
                            related_name='uid_profiles', primary_key=True, db_column='uid_pr')
    name = models.CharField(max_length=15, null=True)
    subTitle = models.CharField(max_length=100, null=True)
    subscribeNum = models.SmallIntegerField(default=0)
    profileImg = models.TextField(null=True) # 사진
    backgroundImg = models.TextField(null=True) # 사진
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'profiles'
        ordering = ['created']


class Portfolios(models.Model):
    title = models.CharField(max_length=50)# 제목
    portfolioWriter = models.ForeignKey("accounts.AccountList",
                                        on_delete=models.CASCADE, related_name='uid_portfolios', db_column='uid_por')
    portfolioWriterProfile = models.TextField(null=True) # 사진
    content = models.TextField(null=True)  # 내용
    contentImage = models.TextField(null=True) # 사진
    date = models.DateTimeField(auto_now_add=True)
    likeN = models.IntegerField(default=0) # 좋아요한 사람 리스트는 좋아요 구현되면 수정
    commentN = models.IntegerField(default=0)  # 댓글 갯수
    postN = models.AutoField(primary_key=True) # 게시물 번호 # 댓글 갯수

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'portfolios'
        ordering = ['date']

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


class ProfileComments(models.Model):
    commentWriter = models.ForeignKey("accounts.AccountList",
                                      on_delete=models.CASCADE, related_name='uid_comments', db_column='uid_cm')
    commentWriterProfile = models.TextField()
    commentDate = models.DateTimeField(auto_now_add=True)
    comContent = models.CharField(max_length=150) # 댓글 내용
    commentN = models.AutoField(primary_key=True)
    postN = models.ForeignKey(Portfolios, null=False, blank=False, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.commentN

    class Meta:
        db_table = 'comments'
        ordering = ['commentDate']

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.commentDate
        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.commentDate.date()
            return str(time.days) + '일 전'
        else:
            return False


class Image(models.Model):
    name = models.CharField(max_length=40, null=True)
    image = models.FileField(upload_to='contentImage/', null=True)
