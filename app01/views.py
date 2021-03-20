from django.shortcuts import render,HttpResponse
from .models import UserTitle,UserVideo,UserPhoto
from .tools import start_data
from .mytools import getUserIDRandom
from ksDjango.settings import currentData
import json

def index(request):
    data = {"formUserID":"testID","formUserName":"testName","message":"没有提示"}
    if request.method == 'POST':
        print("---------------------------------------")
        data["formUserID"]=request.POST.get('formUserID')
        data["formUserName"] = request.POST.get('formUserName')
        if not UserTitle.objects.filter(userID=data["formUserID"]):
            UserTitle.objects.create(userID=data["formUserID"],userName=data["formUserName"])
            data["message"] = "用户存如数据库成功"
        else:
            data["message"] = "当前用户已存在数据库中"


    return render(request,"pages/index.html",data)

def tool(request):
    data ={
        "state":"当前没有执行脚本",
        "message":"请选择需要执行的脚本并且提交",
    }

    current = 1  #1表示当前没有执行脚本
    if request.method == 'POST' and current==1:
        current = 2 #2表示当前正在执行脚本，不能执行脚本，这里好像要设置为全局变量
        result = request.POST.get("inlineRadioOptions")
        data["message"] = "当前正在执行脚本"
        print("---------------tool------------------------")
        # 脚本1
        start_data()
        data["message"] = "脚本执行完毕"
        current = 1

    return render(request,"pages/tool.html",context=data)

def showAdmin(request):
    allUser = UserTitle.objects.values("userName","userID")
    i = 0
    for uID in allUser:
        # 获取数据库中实际视频数量
        theUsr= UserTitle.objects.get(userID=uID["userID"])
        myVideo = UserVideo.objects.filter(theUser=theUsr.id)
        allUser[i]["myVideoCount"] = len(myVideo)
        # 获取主播作品数量
        allUser[i]["realVideoCount"] = theUsr.photo
        # 获取数据库中相册数量
        myPhoto = UserPhoto.objects.filter(thephotoUser=theUsr.id)
        allUser[i]["myPhotoCount"] = len(myPhoto)
        i += 1

    return render(request,'pages/showAdmin.html',{"result":allUser})

def showVideo(request):
    allCover = UserVideo.objects.values("coversUrl")
    return render(request,'pages/showVideo.html',{"result":allCover})


def getUserRandom(request,counts):
    if request.method == 'POST':
        print("-----------")
    cDate = currentData()
    theGetScript = getUserIDRandom(cDate.theCookie)
    theGetScript.get_data()
    results = theGetScript.endResult
    messgae = json.dumps(results)
    # return render(request,results)
    return HttpResponse(messgae)

