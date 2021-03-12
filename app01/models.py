from django.db import models
from datetime import datetime
# Create your models here.

class UserTitle(models.Model):
#女为F，男为M
    GENDER = [
        (0,"未知"),
        (1,"男"),
        (2,"女")
    ]

    STATE = [
        (0,"初次爬取"),
        (1,"ksVideo"),
        (2,"ksLive"),
        (3,"ksVideo+ksLive")
    ]

    USERIMG = "https://tx2.a.yximgs.com/uhead/AB/2020/08/17/09/BMjAyMDA4MTcwOTM2MDNfMjQ0NzAyMDZfMV9oZDM4Nl8xODU=_s.jpg"

    userID = models.CharField(max_length=256,unique=True,verbose_name="用户id")
    userName = models.CharField(max_length=256,verbose_name="用户名")
    createTime = models.DateTimeField(default=datetime.now,verbose_name="创建时间")

    stateUser = models.IntegerField(choices=STATE,verbose_name="用户信息状态",default=0)

    ksID = models.CharField(max_length=128,verbose_name="快手id",default="xxxxxxxxxxxxxx")
    user_text = models.CharField(max_length=2560,verbose_name="用户简述",default="xxxxxxxxxxxxx")
    gender = models.IntegerField(choices=GENDER,verbose_name="性别",default=0)
    fan = models.CharField(max_length=32,verbose_name="粉丝数",default="-1")
    xinzuo = models.CharField(max_length=32,verbose_name="星座",default="未知")
    cityName = models.CharField(max_length=32,verbose_name="地址",default="未知")
    follow = models.CharField(max_length=32,verbose_name="关注的数量",default="-1")
    photo = models.CharField(max_length=32,verbose_name="作品数量",default="-1")
    userImg = models.CharField(max_length=256,verbose_name="图片地址",default=USERIMG)


    def __str__(self):
        return self.userName

    class Mate:
        verbose_name = verbose_name_plural = "用户ID和名字"