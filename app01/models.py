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
        (0,"0初次爬取"),
        (1,"1ksVideo"),
        (2,"1ksLive"),
        (3,"2ksVideo+ksLive"),
        (4,"3videoMP4"),
        (5,"4vieo+liveMP4")
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

class UserVideo(models.Model):
    STATE = [
        (1,"默认ksVideo"),
        (2,"ksVideo+ksLive")
    ]
    # 当被参照删除时，自己也被删除
    theUser = models.ForeignKey(UserTitle,on_delete=models.CASCADE)

    videoID = models.CharField(max_length=128,default="xxxxxxxxxxxxxx",verbose_name="视频id")
    caption = models.CharField(max_length=512,default="暂无",verbose_name="视频描述")
    coversUrl = models.CharField(max_length=512,default="xxxxxxxxxxx",verbose_name="视频封面")
    videoPath = models.CharField(max_length=512,default="xxxxxxxxxxxxx",verbose_name="视频地址")
    realLikeCount = models.CharField(max_length=64,default="xxxxxxxxxxx",verbose_name="具体点赞数量")
    animatedCoverUrl = models.CharField(max_length=512,default="xxxxxxxx",verbose_name="封面动画")

    stateVideo = models.IntegerField(choices=STATE,default=1,verbose_name="状态")

    displayView = models.CharField(max_length=64,default="-1",verbose_name="播放量")
    displayComment = models.CharField(max_length=64,default="-1",verbose_name="评论数")

    def __str__(self):
        return self.videoID

    class Mate:
        verbose_name = verbose_name_plural = "视频信息"


class UserPhoto(models.Model):
    thephotoUser = models.ForeignKey(UserTitle,on_delete=models.CASCADE)

    photoID = models.CharField(max_length=128,verbose_name="相册id",default="xxxxxxxx")
    caption = models.CharField(max_length=512,verbose_name="相册描述",default="暂无")
    displayView = models.CharField(max_length=32,verbose_name="播放量",default="-1")
    displayLike = models.CharField(max_length=32,verbose_name="点赞数",default="-1")
    displayComment = models.CharField(max_length=32,verbose_name="评论数",default="-1")



    imgUrls = models.CharField(max_length=5000,default=" ")


    def __str__(self):
        return self.photoID

    class Mate:
        verbose_name = verbose_name_plural = "相册信息"