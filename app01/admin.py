from django.contrib import admin

from app01.mytools import ksLiveSpider,ksVideoSpider
from ksDjango.settings import currentData
# Register your models here.
from .models import UserTitle



class UserTitleAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ["userName","stateUser"]
    # 过滤器
    list_filter = ["stateUser"]
    # 搜索器
    search_fields = ["userName"]
    # 分页
    list_per_page = 50

    # 执行的动作需要这两个参数,第二个为.query.QuerySet对象，就是选中的数据，通过for循环，通过.调用属性
    def myksVideo(self,request,queryset):
        cData = currentData()
        for qu in queryset:
            ksVideo = ksVideoSpider(qu.userID,cData.ksCookie)
            result = ksVideo.get_data()
            #-----填写数据-------------#
            qu.user_text = result["user_text"]
            if result["gender"] == "F":
                qu.gender = 2
            elif result["gender"] == "M":
                qu.gender = 1
            else:
                qu.gender = 0
            qu.userImg = result["userImg"]
            #---------完成----------#
            if qu.stateUser == 2:
                qu.stateUser = 3
            else:
                qu.stateUser = 1
            # print(result)
            UserTitle.objects.filter(userID=qu.userID).update(user_text=qu.user_text,gender=qu.gender,userImg=qu.userImg,stateUser=qu.stateUser)

        #print(request,type(queryset))
    myksVideo.short_description = "添加ksVideo字段"

    def myksLive(self,request,queryset):
        cData = currentData()
        for qu in queryset:
            ksLive = ksLiveSpider(qu.userID,cData.ksCookie)
            result = ksLive.get_data()
            #-----填写数据-------------#
            qu.ksID = result["ksId"]
            qu.xinzuo = result["xinzuo"]
            qu.cityName = result["cityName"]
            qu.fan = result["fan"]
            qu.follow = result["follow"]
            qu.photo = result["photo"]

            #---------完成----------#
            if qu.stateUser == 1:
                qu.stateUser = 3
            else:
                qu.stateUser = 2
            # print(result)
            if qu.ksID == None:
                qu.ksID = "无法获取ksID"
            UserTitle.objects.filter(userID=qu.userID).update(ksID=qu.ksID,
                                                              xinzuo=qu.xinzuo,
                                                              cityName=qu.cityName,
                                                              fan=qu.fan,
                                                              follow=qu.follow,
                                                              photo=qu.photo,
                                                              stateUser=qu.stateUser)
        #print(request,type(queryset))
    myksLive.short_description = "添加ksLive字段"

    actions = [myksVideo,myksLive]
    # Action选项都是在页面上方显示
    actions_on_top = True
    # Action选项都是在页面下方显示
    actions_on_bottom = False
    # 是否显示选择个数
    actions_selection_counter = True

admin.site.register(UserTitle,UserTitleAdmin)