from django.db import models
from datetime import datetime
# Create your models here.

class UserTitle(models.Model):
    userID = models.CharField(max_length=256,unique=True,verbose_name="用户id")
    userName = models.CharField(max_length=256,verbose_name="用户名")
    createTime = models.DateTimeField(default=datetime.now,verbose_name="创建时间")

    def __str__(self):
        return self.userName

    class Mate:
        verbose_name = verbose_name_plural = "用户ID和名字"