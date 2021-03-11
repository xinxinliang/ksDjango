# ksDjango
关于快手视频的django项目，之前使用爬虫，可以获取快手视频网站的视频，输入用户主页地址，就可以获取用户的视频地址、粉丝数、点赞数等。现在这个项目准备实现：随机获取用户id并且去重，然后根据id获取主页视频信息，将获取的内容展示到网页上。后期还可以开发用户注册登录系统，可以对视频点赞和关注，并且一键下载，最后还可以练习安卓或者微信小程序。嗯，这是我的设想，本项目只是用来学习，切勿商用。嗯，开始。

# 开发日志
## 2021.3.10
#### 前言
- 之前就在做这件事情的，pycharm开发django项目还是最方便的，网页版vscode还是不方便。
- 我在本地做到从快手官网的热门页面爬取用户id，还有爬取自己主页关注的主播，爬取一千多条以发送表单的形式存到数据库时出现问题，可能时太快了。
-  然后我发现自己知道怎么像按按键一样触发函数，只是通过路由，速度方面也不清楚，准备再回头学习一下再做项目的。
- 然后放了快半个月了，之前总是出现问题的python3.9换成了3.8，之前的项目不能用了，而且ksDiango名字也打错了，现在创建这个仓库开始新的开发
- pycharm上面的git用得不熟，还是本地慢慢推送吧。之前的笔记也先要整理一下。

## 2021.3.11
#### 准备操作
1. 创建工程。测试git使用成功。
- 配置失败，使用命令启动测试
```
python manage.py runserver
```
- 配置文件导入os,才启动成功
```
import os
```
2. 设置语言和时区
```
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'
```

3. 迁移数据库，创建超级用户

```
python manage.py migrate
python manage.py makemigrations
python manage.py createsuperuser
```

#### 本地迁移

> 我把之前写的工程迁移过来了，做了使用模板，导入boostrap，使用POST请求，爬取到的数据导入数据库。

1. 我现在数据导入数据库的时候，我做了个一秒的延迟，这样就可以正常导入post的数据了。
2. 在导入数据的时候要注意，cookie可能会改变，**start_data()**这个函数就是导入数据，后期要封装成了类，类中的cookie，用户名（个人页面，获取上面的关注主播）要通过HTML页面输入，这是会改变。
3. 然后再准备写脚本，获取热门页面的主播ID

#### 热门视频分析

1. 这个页面：https://video.kuaishou.com/brilliant
2. 第一栏时热榜视频，由50条。下面的是热门视频，**一直往下滑不到底**，没请求到的视频，包括用户id和名称。可以从这里入手，**注意延时，注意cookie的有效期**，如果失效了要进行处理，等待下一次输入新的cookie再进行。

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210311151201.png)

3. 这里估计可以获取很多的用户ID，然后还可以整理接口，再自己网页上仿照快手页面。

#### 写代码前的分析

1. 每次下拉传来新的数据，这个参数都是为1。第一次传过来的我没有分析。都按照1写吧

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210311152144.png)

2. 我用的是jupyterlab写的代码,这是我感慨是测试的，成功。获取到请求的数据了

- 这是必填的信息，header和json里面的数据怎么获取可以看我之前写的博客

```python
import requests
import json
import os
# 爬取个人主页关注用户的id和naame
URL = "https://video.kuaishou.com/graphql"

headers = {
    "accept":"*/*",
    "Content-Length":"<calculated when request is sent>",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "content-type": "application/json",
    "Cookie": r'kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; did=web_ec874916e390b9741609686125a0452e; didv=1613879531823; client_key=65890b29; ktrace-context=1|MS43NjQ1ODM2OTgyODY2OTgyLjc1MjgyMjUyLjE2MTU0NDI5NDQ0MzYuMTU2OTE=|MS43NjQ1ODM2OTgyODY2OTgyLjIxMjcxODY4LjE2MTU0NDI5NDQ0MzYuMTU2OTI=|0|graphql-server|webservice|false|NA; userId=427400950; kuaishou.server.web_st=ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqABUkHhV7V4kZgEsKH5ujlHNWEHV_KRDoBGhvSztjMMB54VfcpY6EJgzK_b3ZYFhM0obMSTVBDc7Csb-KuDKQpR8sobH5ozd82kEMIV5eb3S0QSJBxAemnSYimqR5IskD_IGA06cph50uA_oH2OftW2tSpaBuXl3vyYhFv6aS_24d8z0n9WILEo5JcTI0QpDdmDoRnXxHc_x7JHIR3s1pBlBhoSzFZBnBL4suA5hQVn0dPKLsMxIiDp66EsPPenAZG6MBgmJkQL2mrCKEDn1OPcTisxS6wffSgFMAE; kuaishou.server.web_ph=cb43dea88ab3a4c31dd231f2dc9cc29b8680',
    "Host": "video.kuaishou.com",
    "Origin": "https://video.kuaishou.com",
    "Referer": "https://video.kuaishou.com/brilliant",  # 这里要更改
    "User-Agent": "PostmanRuntime/7.26.8"
}

payload = {"operationName":"brilliantTypeDataQuery","variables":{"hotChannelId":"00","page":"brilliant","pcursor":"1"},"query":"fragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    id\n    duration\n    caption\n    likeCount\n    realLikeCount\n    coverUrl\n    photoUrl\n    coverUrls {\n      url\n      __typename\n    }\n    timestamp\n    expTag\n    animatedCoverUrl\n    distance\n    videoRatio\n    liked\n    stereoType\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  __typename\n}\n\nfragment photoResult on PhotoResult {\n  result\n  llsid\n  expTag\n  serverExpTag\n  pcursor\n  feeds {\n    ...feedContent\n    __typename\n  }\n  webPageArea\n  __typename\n}\n\nquery brilliantTypeDataQuery($pcursor: String, $hotChannelId: String, $page: String, $webPageArea: String) {\n  brilliantTypeData(pcursor: $pcursor, hotChannelId: $hotChannelId, page: $page, webPageArea: $webPageArea) {\n    ...photoResult\n    __typename\n  }\n}\n"}
```

- 请求页面，输出返回的结果

```
def get_data2():
    res = requests.post(URL, headers=headers, json=payload)
    res.encoding="utf-8"
    m_json = res.json()  #字典格式
    print(m_json)

```

```
if __name__ == "__main__":
    get_data2()
```

2. 我得到了自己想要的数据，然后对有用信息进行筛选。接下来的代码，参考之前写的很容易写出来

```
def get_data2():
    res = requests.post(URL, headers=headers, json=payload)
    res.encoding="utf-8"
    m_json = res.json()  #字典格式
    
    #----------筛选信息------------#
    feeds_list = m_json["data"]["brilliantTypeData"]["feeds"]
    
    for feeds in feeds_list:
        Userid = feeds["author"]["id"]
        Username = feeds["author"]["name"]
        print("%s-----------%s"%(Userid,Username))
        
    print(m_json)
```

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210311153612.png)

> 发现：我把上面的代码运行了两次，得到不同的结果

3. 然后循环获取，因为每个pcursor是一样的，直接循环这个函数就可以了。成功

```
if __name__ == "__main__":
    for i in range(10):
        get_data2()
```

> 思考：如果像我之前想得那样，这些数据存储到数据库中，我的腾讯云学生服务器会不会装不下。

4. 接下来，对存入数据库的用户进行页面展示，这段代码先添加到django中。

> 数据库：有点不明白用户与关注主播，点赞视频之间的主键关系，去看看书再来继续django

#### 接下来

> 看来之前model相关的知识，知道主键怎么用。现在有个问题用户界面的相片没有处理。

1. 我观察了一下，两个地址出现的作品数量不一样

- https://live.kuaishou.com/profile/3x4t9upcrqpvpzk，live开头出现的用户页面会出现图片，也就是所有作品
- https://video.kuaishou.com/profile/3x4t9upcrqpvpzk，video开头的不会出现图片，视频也出现得不完整。
- 但是我详细的看请求的接口是以video开头的，可能是cookie不同

2. 我再**cookie字段中添加了Max-Age=86400**这个属性，测试跑代码是成功的，不知道有没有效果
3. 上面的那句话**是错的，确实不同**，开头是live，结尾是快手ID号，估计这种难度大一些，还是尝试一下。

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210311191256.png)

5. **成功**，我填写相应的信息，请求live界面想video一样成功

```
# -*- coding: utf-8 -*-

#请求mp4地址
import requests
import json
URL = "https://live.kuaishou.com/m_graphql"
headers = {
    "accept":"*/*",
    "Content-Length":"<calculated when request is sent>",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "content-type": "application/json",
    "Cookie": r'clientid=3; did=web_ec874916e390b9741609686125a0452e; didv=1613879531823; client_key=65890b29; kpn=GAME_ZONE; userId=427400950; kuaishou.live.bfb1s=7206d814e5c089a58c910ed8bf52ace5; userId=427400950; kuaishou.live.web_st=ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgAYm9VZdJaOIjsJDqPoO-yLNw4ZuZul234nekkYMdMsNjIq-i5skiOlVnLhFSPv5PTbrQ45yitiFEkQMGUCDxpsbRcsDpHI0CDZfflQeD9Z14cuQ8x2YJORv-1Pz8JM4-_qmBhAxjVHJ8OSs4kMHRKpCvZja6UUYbXLunFhKT5fyhx1HViPCmuVjBcsSxZEtEpvponSa3DjtkZU2KQ3M9pUoaEm-zwBmcbUA4lm5ejQnh9kVjySIgjJsh3xaj6ckXgLNLF3iPjKs6sC7d1lWqH0SZbWeHTREoBTAB; kuaishou.live.web_ph=ed6156f0bc66780438d593dfc3b3f8fa6f63',
    "Host": "live.kuaishou.com",
    "Origin": "https://live.kuaishou.com",
    "Referer": "https://live.kuaishou.com/profile/JTYYA13-",
    "User-Agent": "PostmanRuntime/7.26.8"
}
payload = {"operationName":"publicFeedsQuery","variables":{"principalId":"JTYYA13-","pcursor":"1.602058185281E12","count":24},"query":"query publicFeedsQuery($principalId: String, $pcursor: String, $count: Int) {\n  publicFeeds(principalId: $principalId, pcursor: $pcursor, count: $count) {\n    pcursor\n    live {\n      user {\n        id\n        avatar\n        name\n        __typename\n      }\n      watchingCount\n      poster\n      coverUrl\n      caption\n      id\n      playUrls {\n        quality\n        url\n        __typename\n      }\n      quality\n      gameInfo {\n        category\n        name\n        pubgSurvival\n        type\n        kingHero\n        __typename\n      }\n      hasRedPack\n      liveGuess\n      expTag\n      __typename\n    }\n    list {\n      id\n      thumbnailUrl\n      poster\n      workType\n      type\n      useVideoPlayer\n      imgUrls\n      imgSizes\n      magicFace\n      musicName\n      caption\n      location\n      liked\n      onlyFollowerCanComment\n      relativeHeight\n      timestamp\n      width\n      height\n      counts {\n        displayView\n        displayLike\n        displayComment\n        __typename\n      }\n      user {\n        id\n        eid\n        name\n        avatar\n        __typename\n      }\n      expTag\n      isSpherical\n      __typename\n    }\n    __typename\n  }\n}\n"}        
```

```
def get_data():
    res = requests.post(URL, headers=headers, json=payload)
    res.encoding="utf-8"
    m_json = res.json()  #字典格式   
    print(m_json)

get_data()
```

6. 提取照片信息

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210311192308.png)

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210311192343.png)

- 可以看出以列表形式存储

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210311192416.png)

7. ok,我再把数据库字段和主键创建好，然后把爬虫的代码封装为类，就可以构建网页了
8. 好吧，我之前获取的是用户id，不是快手id。可以先爬取用户id主页信息，获取快手id，然后再通过快手id爬取全面的视频信息和照片。

#### 爬虫代码封装成类

1. 具体分析了一下详细信息

| 字段              | 内容                    | 备注 |
| ----------------- | ----------------------- | ---- |
| animateCoverUrl   | 视频预览的动画          | 0    |
| **caption**       | 视频文案                | 1    |
| **coversUrl**     | 封面图片地址            | 1    |
| **viedoID**       | 视频id                  | 1    |
| **likeCount**     | 简略点赞数              | 1    |
| **photoUrl**      | 视频地址，默认第一个cdn | 1    |
| **realLikeCount** | 详细点赞数              | 1    |
|                   |                         |      |



![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210311201453.png)

2. 这是我暂时提取数据后的结果,然后再需要循环获取所有

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210311205241.png)

3. 代码写好了，输入cookie和用户id，可以获取全部的视频信息

```
import requests
import json

class userdetailSpider():
    URL = "https://video.kuaishou.com/graphql"

    # header中需要更改cookie和Referer
    headers = {
        "accept": "*/*",
        "Content-Length": "<calculated when request is sent>",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "content-type": "application/json",
        # 我添加的时间属性Max-Age=8640000
        "Cookie": r'kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3;Max-Age=8640000; did=web_ec874916e390b9741609686125a0452e; didv=1613879531823; client_key=65890b29; userId=427400950; kuaishou.server.web_st=ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqABQrFWsr52Mhp5GfcmignSLoddGbbCBCTAkyedrcLkHqxI9IIdilOuxFUWwhS41WnVKwFJ0Win96_M-frAXGNXXDx78d0FjGOylLgeVtcXUGsIkgyxVkopf2IR_Pvps61IaXw1XTHZOdTrwQkDIdwESPDssQTuW9XNIfjJK9e88ZgJYNJI5bK5n38Zm37kl8omE8R8E8ZhL87TgGpaRZq3XRoSTdCMiCqspRXB3AhuFugv61B-IiBO8gZCTy1dvCTjyGg0IEN6MrmkUACDgSB3T2BYkkBQ-SgFMAE; kuaishou.server.web_ph=dfcba445b9b7f619411fdced6b1e61d6f207',
        "Host": "video.kuaishou.com",
        "Origin": "https://video.kuaishou.com",
        "Referer": "https://video.kuaishou.com/profile/3xcidpetejrcagy",
        "User-Agent": "PostmanRuntime/7.26.8"
    }
    # 这里的userID也要更改
    payload = {"operationName": "visionProfilePhotoList",
               "variables": {"userId": "3xcidpetejrcagy", "pcursor": "", "page": "profile"},
               "query": "query visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      type\n      author {\n        id\n        name\n        following\n        headerUrl\n        headerUrls {\n          cdn\n          url\n          __typename\n        }\n        __typename\n      }\n      tags {\n        type\n        name\n        __typename\n      }\n      photo {\n        id\n        duration\n        caption\n        likeCount\n        realLikeCount\n        coverUrl\n        coverUrls {\n          cdn\n          url\n          __typename\n        }\n        photoUrls {\n          cdn\n          url\n          __typename\n        }\n        photoUrl\n        liked\n        timestamp\n        expTag\n        animatedCoverUrl\n        __typename\n      }\n      canAddComment\n      currentPcursor\n      llsid\n      status\n      __typename\n    }\n    hostName\n    pcursor\n    __typename\n  }\n}\n"}

    def __init__(self,userID,myCookie):
        userdetailSpider.headers["Referer"] = "https://video.kuaishou.com/profile/"+userID
        userdetailSpider.payload["variables"]["userId"] = userID
        userdetailSpider.headers["Cookie"] = myCookie


    def get_data(self):
        #--------------请求页面--------------#
        try:
            res = requests.post(userdetailSpider.URL, headers=userdetailSpider.headers, json=userdetailSpider.payload)
            res.encoding = "utf-8"
            m_json = res.json()  # 字典格式

            #-------------诗筛选数据-------------#
            #*******************************************************************#
            # 这个result参数判断请求是否正确，如果不是1请求失败，后面继续执行会报错，程序结束
            # print(m_json["data"]["visionProfilePhotoList"]["result"])
            feeds_list = m_json["data"]["visionProfilePhotoList"]["feeds"]

            # 获取pcursor并且填写到下一次的header中
            pcursor = m_json["data"]["visionProfilePhotoList"]["pcursor"]
            userdetailSpider.payload["variables"]["pcursor"] = pcursor

            #-------------具体提取数据----------#写到这里想起了，我应该是通过live获取视频信息
            result = {}     #信息存储在字典中
            for feeds in feeds_list:
                result["caption"] = feeds["photo"]["caption"]
                result["coversUrl"] = feeds["photo"]["coverUrl"]
                result["videoID"] = feeds["photo"]["id"]
                result["videoPath"] = feeds["photo"]["photoUrl"]
                result["likeCount"] = feeds["photo"]["likeCount"]
                result["realLikeCount"] = feeds["photo"]["realLikeCount"]
                print(result)
                #-----------待会再这里编写存储到数据库的函数--------------

            #print(m_json)
            #print(feeds_list)
            print(pcursor)

            if pcursor == "no_more":
                return 0
        except:
            print("页面请求错误，请检查cookie是否过期，id是否正确")

    def start_spider(self):
        while(1):
            temp = userdetailSpider.get_data(self)
            if temp == 0:
                break



if __name__ == "__main__":
    theCookie = "kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; clientid=3;Max-Age=8640000; did=web_ec874916e390b9741609686125a0452e; didv=1613879531823; client_key=65890b29; userId=427400950; kuaishou.server.web_st=ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqABQrFWsr52Mhp5GfcmignSLoddGbbCBCTAkyedrcLkHqxI9IIdilOuxFUWwhS41WnVKwFJ0Win96_M-frAXGNXXDx78d0FjGOylLgeVtcXUGsIkgyxVkopf2IR_Pvps61IaXw1XTHZOdTrwQkDIdwESPDssQTuW9XNIfjJK9e88ZgJYNJI5bK5n38Zm37kl8omE8R8E8ZhL87TgGpaRZq3XRoSTdCMiCqspRXB3AhuFugv61B-IiBO8gZCTy1dvCTjyGg0IEN6MrmkUACDgSB3T2BYkkBQ-SgFMAE; kuaishou.server.web_ph=dfcba445b9b7f619411fdced6b1e61d6f207"
    theUserID = "3xkm67762d5fwzc"

    test = userdetailSpider(theUserID,theCookie)
    test.start_spider()
```

#### 再写获取live页面的信息

1. 慢着，我又有个发现，我之前以为是live开头的要用快手id结尾，我把https://video.kuaishou.com/profile/3xcidpetejrcagy·，这个连接的video改为了live，就可以获取详细页面信息，全面的，那么这个函数先不写。
2. 还是继续写下去把，不好改（筛选信息要重写）。直接live+用户id，因为我发现video+用户id界面提取不到ksID,所以
3. 这是live开头请求到的数据

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210311222248.png)

- 相册是一个数组

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210311222236.png)

- 这个是视频

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210311222339.png)

4. 写得代码请求数据成功，现在写筛选数据的逻辑

> 我擦，我写着写着发现里面没有视频地址，没有发现联系。
>
> https://txmov2.a.yximgs.com/bs2/newWatermark/Mzc5MDA0MzYwMjQ_zh_4.mp4

5. 我再分析了一下，ksID：Nx277777。一共68个作品，video中61个视频，live中7个相册，是对的。我去测试一下别人

> userID：3xcidpetejrcagy，6个相册，60个视频，一共66个做作品，是对头的。（我全都要）

#### 声明：本项目是作为学习使用，如有侵权立刻删除，切勿商用，后果自负

6. 然后viedo爬取视频，live爬取相册，把那个动态图也加上去。

```
# 输出快手ID和cookie
class userdetailLiveSpider():

    URL = "https://live.kuaishou.com/m_graphql"

    headers = {
        "accept": "*/*",
        "Content-Length": "<calculated when request is sent>",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "content-type": "application/json",
        # 我添加的时间属性Max-Age=8640000
        "Cookie": r'clientid=3;Max-Age=8640000; did=web_ec874916e390b9741609686125a0452e; didv=1613879531823; client_key=65890b29; kpn=GAME_ZONE; userId=427400950; kuaishou.live.bfb1s=7206d814e5c089a58c910ed8bf52ace5; userId=427400950; kuaishou.live.web_st=ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgAYm9VZdJaOIjsJDqPoO-yLNw4ZuZul234nekkYMdMsNjIq-i5skiOlVnLhFSPv5PTbrQ45yitiFEkQMGUCDxpsbRcsDpHI0CDZfflQeD9Z14cuQ8x2YJORv-1Pz8JM4-_qmBhAxjVHJ8OSs4kMHRKpCvZja6UUYbXLunFhKT5fyhx1HViPCmuVjBcsSxZEtEpvponSa3DjtkZU2KQ3M9pUoaEm-zwBmcbUA4lm5ejQnh9kVjySIgjJsh3xaj6ckXgLNLF3iPjKs6sC7d1lWqH0SZbWeHTREoBTAB; kuaishou.live.web_ph=ed6156f0bc66780438d593dfc3b3f8fa6f63',
        "Host": "live.kuaishou.com",
        "Origin": "https://live.kuaishou.com",
        "Referer": "https://live.kuaishou.com/profile/LY7452065",
        "User-Agent": "PostmanRuntime/7.26.8"
    }

    payload = {"operationName": "publicFeedsQuery",
               "variables": {"principalId": "JTYYA13-", "pcursor": "", "count": 24},
               "query": "query publicFeedsQuery($principalId: String, $pcursor: String, $count: Int) {\n  publicFeeds(principalId: $principalId, pcursor: $pcursor, count: $count) {\n    pcursor\n    live {\n      user {\n        id\n        avatar\n        name\n        __typename\n      }\n      watchingCount\n      poster\n      coverUrl\n      caption\n      id\n      playUrls {\n        quality\n        url\n        __typename\n      }\n      quality\n      gameInfo {\n        category\n        name\n        pubgSurvival\n        type\n        kingHero\n        __typename\n      }\n      hasRedPack\n      liveGuess\n      expTag\n      __typename\n    }\n    list {\n      id\n      thumbnailUrl\n      poster\n      workType\n      type\n      useVideoPlayer\n      imgUrls\n      imgSizes\n      magicFace\n      musicName\n      caption\n      location\n      liked\n      onlyFollowerCanComment\n      relativeHeight\n      timestamp\n      width\n      height\n      counts {\n        displayView\n        displayLike\n        displayComment\n        __typename\n      }\n      user {\n        id\n        eid\n        name\n        avatar\n        __typename\n      }\n      expTag\n      isSpherical\n      __typename\n    }\n    __typename\n  }\n}\n"}

    def __init__(self,userId,myCookie):
        self.headers["Referer"] = "https://live.kuaishou.com/profile/"+userId
        self.payload["variables"]["principalId"] = userId
        self.headers["Cookie"] = myCookie

    def get_data(self):
        try:
            res = requests.post(self.URL, headers=self.headers, json=self.payload)
            res.encoding = "utf-8"
            m_json = res.json()  # 字典格式

            feeds_list = m_json["data"]["publicFeeds"]["list"]
            pcursor = m_json["data"]["publicFeeds"]["pcursor"]
            self.payload["variables"]["pcursor"] = pcursor
            # print(m_json)

            #-------------筛选数据---------------#
            result = {}
            for feeds in feeds_list:
                result["caption"] = feeds["caption"]
                # 播放量，点赞数，评论数
                result["displayView"] = feeds["counts"]["displayView"]
                result["displayLike"] = feeds["counts"]["displayLike"]
                result["displayComment"] = feeds["counts"]["displayComment"]
                # 相册，可能为空，可能为列表
                result["imgUrls"] = feeds["imgUrls"]
                result["liveID"] = feeds["id"]
                print(result)
        except:
            print("页面请求错误，请检查cookie是否过期，id是否正确")
if __name__ == "__main__":
    theCookie = "kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; clientid=3;Max-Age=8640000; did=web_ec874916e390b9741609686125a0452e; didv=1613879531823; client_key=65890b29; userId=427400950; kuaishou.server.web_st=ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqABQrFWsr52Mhp5GfcmignSLoddGbbCBCTAkyedrcLkHqxI9IIdilOuxFUWwhS41WnVKwFJ0Win96_M-frAXGNXXDx78d0FjGOylLgeVtcXUGsIkgyxVkopf2IR_Pvps61IaXw1XTHZOdTrwQkDIdwESPDssQTuW9XNIfjJK9e88ZgJYNJI5bK5n38Zm37kl8omE8R8E8ZhL87TgGpaRZq3XRoSTdCMiCqspRXB3AhuFugv61B-IiBO8gZCTy1dvCTjyGg0IEN6MrmkUACDgSB3T2BYkkBQ-SgFMAE; kuaishou.server.web_ph=dfcba445b9b7f619411fdced6b1e61d6f207"
    theUserID = "3xkm67762d5fwzc"

    test = userdetailLiveSpider(theUserID,theCookie)
    test.get_data()
```

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210311230600.png)

7. 然后写一下循环，再合并一下，或重新构建一个展示相册的页面。

> 整合过程中，如果live中的id存在video的视频id，怎说明整合，如果没有就是相册，则添加。

#### 获取用户详细信息

1. userTitle表存储用户id和name以及创建时间，之前打算在创建userDetail，把userTitle当作主键，但其不是一对多的关系，还是增加字段。

> 好像可以在model中添加执行动作的函数。
>
> 添加视频信息时，要通过用户id主键接口添加

2. 观察需要提取的信息

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210311234500.png)

> ksID时一个很重要的信息，如果有需要再添加把。

3. 好吧，还是请求live开头的页面，把ksID也存起来

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210311234937.png)

> 星座和地址也存着把
>
> 建表的时候添加一个字段，来表示一些状态。

4. 我觉得还是先学习一下model中写函数，等下方便自己添加数据。

> https://www.cnblogs.com/shenjianping/p/11526538.html,这篇博客上面用到了多对多关系，使用

```
authors=models.ManyToManyField("Author")
```

- 这是我之前没有见到过的。主播和视频是一多的关系，使用主键。

5. 还是歇歇，看看书上面怎么搞的，下次再干。