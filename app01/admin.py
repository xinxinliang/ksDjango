from django.contrib import admin

from app01.mytools import ksLiveSpider,ksVideoSpider,userdetailSpider,userdetailLiveSpider,updateCookie
from ksDjango.settings import currentData
# Register your models here.
from .models import UserTitle,UserVideo,UserPhoto
import time
from app01 import KSCOOKIE,THECOOKIE


class UserTitleAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ["userName","stateUser","ksID","photo"]
    # 过滤器
    list_filter = ["stateUser"]
    # 搜索器
    search_fields = ["userName"]
    # 分页
    list_per_page = 50

    # 执行的动作需要这两个参数,第二个为.query.QuerySet对象，就是选中的数据，通过for循环，通过.调用属性
    def myksVideo(self,request,queryset):
        for qu in queryset:
            ksVideo = ksVideoSpider(qu.userID,KSCOOKIE)
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
            # 任何状态都可以执行
            if qu.stateUser == 2:
                qu.stateUser = 3
            else:
                qu.stateUser = 1
            # print(result)
            UserTitle.objects.filter(userID=qu.userID).update(user_text=qu.user_text,gender=qu.gender,userImg=qu.userImg,stateUser=qu.stateUser)

        #print(request,type(queryset))
    myksVideo.short_description = "添加ksVideo字段"

    def myksLive(self,request,queryset):
        for qu in queryset:
            ksLive = ksLiveSpider(qu.userID,KSCOOKIE)
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

    def myvideoMP4(self,request,queryset):
        theUpdateCookie = updateCookie()
        theUpdateCookie.updateCo()
        print(theUpdateCookie.theResult)
        for qu in queryset:
            thevideo = userdetailSpider(qu.userID,theUpdateCookie.theResult)
            thevideo.start_spider()
            # 只有爬取到完整的数据才能写入数据库
            if thevideo.endStatus is not 0:
                break

            results = thevideo.endResult

            ttUser = UserTitle.objects.get(userID=qu.userID)

            # 只有状态3才能入库
            if ttUser.stateUser is not 3:
                break
            for result in results:

                if result["animatedCoverUrl"] == None:
                    result["animatedCoverUrl"] = "一直没有"
                print(result["videoID"])
                # 数据库添加数据不需要延迟
                # time.sleep(1)
                # 如果再UserVideo中查早到相同，如果数据多了会非常消耗性能
                if UserVideo.objects.filter(videoID=result["videoID"]):
                    continue
                temp = UserVideo.objects.create(videoID = result["videoID"],
                                        caption = result["caption"],
                                        coversUrl = result["coversUrl"],
                                        videoPath = result["videoPath"],
                                        realLikeCount = result["realLikeCount"],
                                        animatedCoverUrl=result["animatedCoverUrl"],
                                         theUser = ttUser)
                temp.save()
                del temp
            ttUser.stateUser = 4
            ttUser.save()
            del ttUser
            del theUpdateCookie

    myvideoMP4.short_description = "添加视频video"

    def myPhoto(self,request,queryset):
        for qu in queryset:
            ttUser = UserTitle.objects.get(userID=qu.userID)
            # 只有状态4才能入库
            if ttUser.stateUser is not 4:
                break

            thisuserID = ttUser.ksID
            thevideo = userdetailLiveSpider(thisuserID,KSCOOKIE)
            thevideo.start_spider()

            if thevideo.endStatus is not 0:
                break

            results = thevideo.endResult


            for result in results:
                # 判断imgUrls字段为空，补充视频信息
                # 补充剩余信息的主播视频，photo也添加进去了
                if len(result["imgUrls"]) == 0:
                    ttUser.displayView = result["displayView"]
                    ttUser.displayComment = result["displayComment"]
                    # print(result["liveID"])
                else:
                    # time.sleep(1)
                    photoUrl = ','.join(result["imgUrls"])
                    if UserPhoto.objects.filter(photoID=result["liveID"]):
                        continue
                    temp = UserPhoto.objects.create(photoID = result["liveID"],
                                                caption = result["caption"],
                                                displayView = result["displayView"],
                                                displayLike = result["displayLike"],
                                                displayComment = result["displayComment"],
                                                imgUrls = photoUrl,
                                                thephotoUser = ttUser)
                    temp.save()
                    del temp

            # 状态5表示完成，对比作品是否缺失。如果需要重新开始就执行1，2状态
            # 无法获取ksID的用户将无法执行这个动作
            ttUser.stateUser = 5
            ttUser.save()
            del ttUser

    myPhoto.short_description = "添加相册photo"

    actions = [myksVideo,myksLive,myvideoMP4,myPhoto]
    # Action选项都是在页面上方显示
    actions_on_top = True
    # Action选项都是在页面下方显示
    actions_on_bottom = False
    # 是否显示选择个数
    actions_selection_counter = True

class UserVideoAdmin(admin.ModelAdmin):
    list_display = ["theUser","videoID"]

class PhotoUserAdmin(admin.ModelAdmin):
    list_display = ["thephotoUser","photoID"]
admin.site.register(UserTitle,UserTitleAdmin)


admin.site.register(UserVideo,UserVideoAdmin)

admin.site.register(UserPhoto,PhotoUserAdmin)