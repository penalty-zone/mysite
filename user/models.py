from django.db import models

from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20, verbose_name="昵称")

    def __str__(self):
        return '<Profile: {} for {}>'.format(self.nickname, self.user.username)


def get_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        # profile.nickname  其实存在一种反向的链接，只要本MODELS中与另一个模型的主键关联，则那个模型会拥有
        # 当前MODELS中那个类的小写名
        return profile.nickname
    else:
        return '----------------未定义昵称'

def get_nickname_or_username(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        # profile.nickname  其实存在一种反向的链接，只要本MODELS中与另一个模型的主键关联，则那个模型会拥有
        # 当前MODELS中那个类的小写名
        return profile.nickname
    else:
        return self.username

User.get_nickname = get_nickname
User.get_nickname_or_username = get_nickname_or_username
