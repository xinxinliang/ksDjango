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

## 2021.3.12

#### 获取主播信息

> 今天把django相关的书看了一下，之前表之间一对多，多对多上面有写道，可能自己之前没注意。然后，感觉对django了解得差不多了。看了一下面试的题目，结果几乎不会，至少是一般书上是没有的。

1. 今天本来按照思路写很顺利的，但开始就出现了**问题**：我就算是扫码登录后查看live开头的主播页面，看不到作品，然后跑userdetailLiveSpider对象不成功，像是网络问题。
2. 好吧，网页上可以访问了，看看我的这个对象有什么问题，上面一个对象运行是成功的。
3. 目前估计是cookie问题，live开头的cookie有效时间比较短，我尝试更换cookie。
4. 不是cookie问题，我再去官网刷新没有数据，先不管了，写获取主播信息的逻辑

5. 请求头的信息相同，不同的就是payload，还是单独写个类

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210312163849.png)

6. 这个cookie和之前的不一样，要重新复制一个，不然显示为登录。这是成功的信息

```
{'data': {'sensitiveUserInfo': {'kwaiId': 'synsyn520521', 'originUserId': '943759388', 'constellation': '双子座', 'cityName': '山东 济宁市', 'counts': {'fan': '115.8w', 'follow': '151', 'photo': '66', 'liked': None, 'open': 66, 'playback': 0, 'private': None, '__typename': 'CountInfo'}, '__typename': 'User'}}}

```

7. 现在写提取信息的逻辑

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210312165408.png)

8. 代码。

```
class ksLiveSpider():
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

    payload = {"operationName":"sensitiveUserInfoQuery","variables":{"principalId":"3xkm67762d5fwzc"},"query":"query sensitiveUserInfoQuery($principalId: String) {\n  sensitiveUserInfo(principalId: $principalId) {\n    kwaiId\n    originUserId\n    constellation\n    cityName\n    counts {\n      fan\n      follow\n      photo\n      liked\n      open\n      playback\n      private\n      __typename\n    }\n    __typename\n  }\n}\n"}
    def __init__(self,userId,myCookie):
        self.headers["Referer"] = "https://live.kuaishou.com/profile/"+userId
        self.payload["variables"]["principalId"] = userId
        self.headers["Cookie"] = myCookie
    def get_data(self):
        try:
            res = requests.post(self.URL, headers=self.headers, json=self.payload)
            res.encoding = "utf-8"
            m_json = res.json()  # 字典格式
            print(m_json)

            result = {}
            #---------提取有用数据--------#

            result["ksId"] = m_json["data"]["sensitiveUserInfo"]["kwaiId"]
            result["xinzuo"] = m_json["data"]["sensitiveUserInfo"]["constellation"]
            result["cityName"] = m_json["data"]["sensitiveUserInfo"]["cityName"]
            result["fan"] = m_json["data"]["sensitiveUserInfo"]["counts"]["fan"]
            result["follow"] = m_json["data"]["sensitiveUserInfo"]["counts"]["follow"]
            # 作品数
            result["photo"] = m_json["data"]["sensitiveUserInfo"]["counts"]["photo"]

            print(result)

        except:
            print("页面请求错误，请检查cookie是否过期，id是否正确")
if __name__ == "__main__":
    theCookie = "kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; clientid=3;Max-Age=8640000; did=web_ec874916e390b9741609686125a0452e; didv=1613879531823; client_key=65890b29; userId=427400950; kuaishou.server.web_st=ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqABQrFWsr52Mhp5GfcmignSLoddGbbCBCTAkyedrcLkHqxI9IIdilOuxFUWwhS41WnVKwFJ0Win96_M-frAXGNXXDx78d0FjGOylLgeVtcXUGsIkgyxVkopf2IR_Pvps61IaXw1XTHZOdTrwQkDIdwESPDssQTuW9XNIfjJK9e88ZgJYNJI5bK5n38Zm37kl8omE8R8E8ZhL87TgGpaRZq3XRoSTdCMiCqspRXB3AhuFugv61B-IiBO8gZCTy1dvCTjyGg0IEN6MrmkUACDgSB3T2BYkkBQ-SgFMAE; kuaishou.server.web_ph=dfcba445b9b7f619411fdced6b1e61d6f207"
    theUserID = "3xkm67762d5fwzc"
    ksCookie = "clientid=3; did=web_ec874916e390b9741609686125a0452e; didv=1613879531823; client_key=65890b29; kpn=GAME_ZONE; userId=427400950; userId=427400950; kuaishou.live.bfb1s=ac5f27b3b62895859c4c1622f49856a4; kuaishou.live.web_st=ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgAfwzFw_Kb2uHnKBQgQQ9-nhGuO2rbpCerVYO54A3KmQUQ6JOiQO-mLFbcwABZ9A-Fl2X5WxQ9yuXHLsMV-RsuZygWUnugryt27cp6rgKzgLI7y6ar8R1RdP6CUPp1JTjbgZ6uzAdhQdayNbiM-isllV5Yyj9bb4IK_LPqzxYDjf_uy0QRa_YxWiMtTUPQd8CFinqBXb7gj-o9HNOZG_v1y0aEk2hY_LIikBot7IUVtJ3ydB6KCIgmvgxlD_4Ac99qgHpdvBfsxGugwTfosyEsfq-BaaFMG0oBTAB; kuaishou.live.web_ph=ae0615d67633a6c0debe8d4668be19e1d446"
    test = ksLiveSpider(theUserID,ksCookie)
    test.get_data()
```

#### 修改model

1. 接下来修改model中的字段。这是之前字段

```
class UserTitle(models.Model):
    userID = models.CharField(max_length=256,unique=True,verbose_name="用户id")
    userName = models.CharField(max_length=256,verbose_name="用户名")
    createTime = models.DateTimeField(default=datetime.now,verbose_name="创建时间")
```

2. 着重要添加一个**状态字段**。

> 想起了**头像地址**字段，需要再viedo页面获取

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210312171042.png)

- 之前热门页面可以获取到头像地址，也就是再加入用户id和name的时候，eid是用户id，id不知道是什么。

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210312171334.png)

- 从个人关注页面获取id和name时候也可以获取头像地址，那么只要再第一步工作的时候存储到其中就可以了。
- 性别字段就看视频自己判断吧

3. 好吧，live开头请求的数据连caption都没有，还是准备再爬取video用户界面的信息

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210312190118.png)

4. 筛选吧。写吐了，今天上了**软件工程**，看来真的很重要。

```
{'data': {'visionProfile': {'result': 1, 'hostName': 'webservice-bjxy-rs9150.idcyz.hb1.kwaidc.com', 'userProfile': {'ownerCount': {'fan': '128.9w', 'photo': None, 'follow': 438, 'photo_public': 68, '__typename': 'VisionUserProfileOwnerCount'}, 'profile': {'gender': 'F', 'user_name': '南希阿-', 'user_id': '3xcidpetejrcagy', 'headurl': 'https://tx2.a.yximgs.com/uhead/AB/2020/08/17/09/BMjAyMDA4MTcwOTM2MDNfMjQ0NzAyMDZfMV9oZDM4Nl8xODU=_s.jpg', 'user_text': '谢谢你在世界的角落里找到我', 'user_profile_bg_url': '//s2-10623.kwimgs.com/kos/nlav10623/vision_images/profile_background.5bc08b1bf4fba1f4.svg', '__typename': 'VisionUserProfileUser'}, 'isFollowing': True, '__typename': 'VisionUserProfile'}, '__typename': 'VisionProfileResult'}}}

```

5. 代码

```
# 获取video页面的主播信息
class ksVideoSpider():
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
    payload = {"operationName":"visionProfile","variables":{"userId":"3xcidpetejrcagy"},"query":"query visionProfile($userId: String) {\n  visionProfile(userId: $userId) {\n    result\n    hostName\n    userProfile {\n      ownerCount {\n        fan\n        photo\n        follow\n        photo_public\n        __typename\n      }\n      profile {\n        gender\n        user_name\n        user_id\n        headurl\n        user_text\n        user_profile_bg_url\n        __typename\n      }\n      isFollowing\n      __typename\n    }\n    __typename\n  }\n}\n"}
    def __init__(self, userID, myCookie):
        userdetailSpider.headers["Referer"] = "https://video.kuaishou.com/profile/"+userID
        userdetailSpider.payload["variables"]["userId"] = userID
        userdetailSpider.headers["Cookie"] = myCookie

    def get_data(self):
        try:
            res = requests.post(self.URL, headers=self.headers, json=self.payload)
            res.encoding = "utf-8"
            m_json = res.json()  # 字典格式
            print(m_json)

            result = {}
            #---------提取有用数据--------#
            result["user_text"] = m_json["data"]["visionProfile"]["userProfile"]["profile"]["user_text"]
            result["gender"] = m_json["data"]["visionProfile"]["userProfile"]["profile"]["gender"]
            result["userImg"] = m_json["data"]["visionProfile"]["userProfile"]["profile"]["headurl"]

            print(result)

        except:
            print("页面请求错误，请检查cookie是否过期，id是否正确")
if __name__ == "__main__":
    theCookie = "kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; clientid=3;Max-Age=8640000; did=web_ec874916e390b9741609686125a0452e; didv=1613879531823; client_key=65890b29; userId=427400950; kuaishou.server.web_st=ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqABQrFWsr52Mhp5GfcmignSLoddGbbCBCTAkyedrcLkHqxI9IIdilOuxFUWwhS41WnVKwFJ0Win96_M-frAXGNXXDx78d0FjGOylLgeVtcXUGsIkgyxVkopf2IR_Pvps61IaXw1XTHZOdTrwQkDIdwESPDssQTuW9XNIfjJK9e88ZgJYNJI5bK5n38Zm37kl8omE8R8E8ZhL87TgGpaRZq3XRoSTdCMiCqspRXB3AhuFugv61B-IiBO8gZCTy1dvCTjyGg0IEN6MrmkUACDgSB3T2BYkkBQ-SgFMAE; kuaishou.server.web_ph=dfcba445b9b7f619411fdced6b1e61d6f207"
    theUserID = "3xkm67762d5fwzc"
    ksCookie = "clientid=3; did=web_ec874916e390b9741609686125a0452e; didv=1613879531823; client_key=65890b29; kpn=GAME_ZONE; userId=427400950; userId=427400950; kuaishou.live.bfb1s=ac5f27b3b62895859c4c1622f49856a4; kuaishou.live.web_st=ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgAfwzFw_Kb2uHnKBQgQQ9-nhGuO2rbpCerVYO54A3KmQUQ6JOiQO-mLFbcwABZ9A-Fl2X5WxQ9yuXHLsMV-RsuZygWUnugryt27cp6rgKzgLI7y6ar8R1RdP6CUPp1JTjbgZ6uzAdhQdayNbiM-isllV5Yyj9bb4IK_LPqzxYDjf_uy0QRa_YxWiMtTUPQd8CFinqBXb7gj-o9HNOZG_v1y0aEk2hY_LIikBot7IUVtJ3ydB6KCIgmvgxlD_4Ac99qgHpdvBfsxGugwTfosyEsfq-BaaFMG0oBTAB; kuaishou.live.web_ph=ae0615d67633a6c0debe8d4668be19e1d446"
    test = ksVideoSpider(theUserID,ksCookie)
    test.get_data()

```

6. 目前写了四个类了，互相补充可以得出完整的主播信息，把数据库字段填写完成。

```
class UserTitle(models.Model):
#女为F，男为M
    GENDER = [
        (0,"未知"),
        (1,"男"),
        (2,"女")
    ]

    STATE = [
        (0,"初次爬取"),
        (1,"测试")
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
```

> 刚开始把ksID设置了uinque=True，结果migrate的时候报错，改回来了makemigrations再migrate还是保存，我把app01中的3.12创建的几个文件删除了，再执行命令一遍就成功了。要是以前遇到这样的问题，可能是删除数据库了。

7. 这个博客讲解了**给admin添加动作**：https://blog.csdn.net/weixin_41863685/article/details/83820230

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210312194747.png)

8. 完成了简单的测试，现在可以把对象加入到其中了。

```
from django.contrib import admin

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
    def mytest(self,request,queryset):
        for qu in queryset:
            print(qu.userName)
        print(request,type(queryset))

    mytest.short_description = "测试"

    actions = [mytest,]

    # Action选项都是在页面上方显示
    actions_on_top = True
    # Action选项都是在页面下方显示
    actions_on_bottom = False

    # 是否显示选择个数
    actions_selection_counter = True

admin.site.register(UserTitle,UserTitleAdmin)
```

9. 我再setting文件中创建了一个类，来存储cookie信息，便于修改和使用。

#### 填补信息

1. 类的输出

- ksLiveSpider(theUserID,ksCookie)

```
{'ksId': 'synsyn520521', 'xinzuo': '双子座', 'cityName': '山东 济宁市', 'fan': '115.9w', 'follow': '151', 'photo': '65'}
```

- ksVideoSpider(theUserID,ksCookie)

```
{'user_text': '谢谢你在世界的角落里找到我', 'gender': 'F', 'userImg': 'https://tx2.a.yximgs.com/uhead/AB/2020/08/17/09/BMjAyMDA4MTcwOTM2MDNfMjQ0NzAyMDZfMV9oZDM4Nl8xODU=_s.jpg'}
```

2. 状态设置

| state | 描述                           |
| ----- | ------------------------------ |
| 0     | 初次爬取，只有username和userid |
| 1     | ksvideo                        |
| 2     | kslive                         |
| 3     | ksvideo+kslive                 |
|       |                                |

> 目前状态相关的逻辑不完美，比如为3执行ksvideo就变成了状态1，代表还要进行kslive，但是kslive字段已经添加了，使用时注意没必要给状态3执行动作。

3. 两个逻辑我是这样写的，但是这样好像不能改变数据库中相关的数据

```
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

        #print(request,type(queryset))
    myksVideo.short_description = "添加ksVideo字段"

    def myksLive(self,request,queryset):
        cData = currentData()
        for qu in queryset:
            ksLive = ksLiveSpider(qu.userID,cData.ksCookie)
            result = ksLive.get_data()
            #-----填写数据-------------#
            qu.ksID = result["ksID"]
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

        #print(request,type(queryset))
    myksLive.short_description = "添加ksLive字段"
```

4. 我分别再函数中调用model筛选和更新数据的函数，成功实现功能

```
UserTitle.objects.filter(userID=qu.userID).update(user_text=qu.user_text,gender=qu.gender,userImg=qu.userImg,stateUser=qu.stateUser)
```

```
UserTitle.objects.filter(userID=qu.userID).update(ksID=qu.ksID,
                                                  xinzuo=qu.xinzuo,
                                                  cityName=qu.cityName,
                                                  fan=qu.fan,
                                                  follow=qu.follow,
                                                  photo=qu.photo,
                                                  stateUser=qu.stateUser)
```

5. 测试成功，但是我有的个数据添加live不成功，报错没有ksID字段。但不影响其他数据的添加。

- 我单独提取了id到mytool中测试,输出总没有提取到ksID，所以报错

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210312230648.png)

- 进行判断一下就可以了

```
            if qu.ksID == None:
                qu.ksID = "无法获取ksID"
            UserTitle.objects.filter(userID=qu.userID).update(ksID=qu.ksID,
                                                              xinzuo=qu.xinzuo,
                                                              cityName=qu.cityName,
                                                              fan=qu.fan,
                                                              follow=qu.follow,
                                                              photo=qu.photo,
                                                              stateUser=qu.stateUser)
```

6 今天就到这了，明天和室友一起去景点旅游。

> 明天把功能录一个演示视频。
>
> 实现后端功能，是通过按钮触发js的函数，然后想后端的接口post实现相应的功能。这是再《跟老齐学django》上看到的。

## 2021.3.13

> 今天下雨了，不出去玩了

#### IP问题

1. 我早上跑了一下`userdetailSpider(theUserID,theCookie)`,刚开始是好的，然后就**返回None**
2. 然后我就去浏览器总刷新，刷新不出来视频。我怀疑是**由于访问得太快，暂时的封锁了IP**
3. 还有None问题，如果不处理就会一直请求并且返回None。这个问题就是我之前提到的result，为1代表成功
4. 果然是暂时性的，我没有更改cookie，再去怕代码成功了，但还是要加上延时函数。这叫请求太快，亲求失败吧。
5. 我把延时函数删除了，跑了几次都是成功的，只好先这样写着。

```
            if m_json["data"]["visionProfilePhotoList"]["result"] == 1:
                print("请求成功，开始筛选数据")
            else:
                print("请求数据失败，无法筛选，程序终止")
                return -1
```

#### 筛选数据

1. 这是视频信息

```
{'caption': '锦上添花我不需要 雪中送炭你做不到', 'coversUrl': 'https://tx2.a.yximgs.com/upic/2018/03/24/19/BMjAxODAzMjQxOTIyNDVfMTA1MjM4MjNfNTYwMzAxNTQwNF8xXzM=_B73ece8a2ba15635894bd1d22c88ab2ab.jpg?tag=1-1615596637-xpcwebprofile-0-c2teex2jjk-fe86cc6122e6e5cc&clientCacheKey=3xp87jw5zmeue69.jpg&di=75960068&bp=14734', 'videoID': '3xp87jw5zmeue69', 'videoPath': 'https://txmov2.a.yximgs.com/upic/2018/03/24/19/BMjAxODAzMjQxOTIyNDVfMTA1MjM4MjNfNTYwMzAxNTQwNF8xXzM=_b_B4e460c2dedc40be078e7a315389327f8.mp4?tag=1-1615596637-xpcwebprofile-0-nc4gujqkgj-65ff48b3ed0c2822&clientCacheKey=3xp87jw5zmeue69_b.mp4&tt=b&di=75960068&bp=14734', 'likeCount': '30', 'realLikeCount': 30, 'animatedCoverUrl': None}

```

2. 网页上我要是开启代理刷新就会出现数据。
3. live开头的请求视频好像会封锁ip，我准备再juoyterlab上试一下，结果进去不了，可能是家里的旧电脑又被怎么了。
4. 整理。创建视频表。

```
class UserVideo(models.Model):
    STATE = [
        (1,"默认ksVideo"),
        (2,"ksLive"),
        (3,"ksVideo+ksLive")
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

```

5. 然后改了一下类，把爬取到的数据以列表形式存取到endResult属性中。因为一般文件不能调用.model
6. 这个博客，演示了一对多怎么添加数据：https://www.cnblogs.com/wyhluckdog/p/11383234.html

- 这是我的尝试,失败

```
            for result in results:
                UserTitle.objects.get(userId = qu.userID).theUser.objects.create(videoID = result["videoID"],
                                                                                 caption = result["caption"],
                                                                                 coversUrl = result["coversUrl"],
                                                                                 videoPath = result["videoPath"],
                                                                                 realLikeCount = result["realLikeCount"],
                                                                                 animatedCoverUrl=result["animatedCoverUrl"],
                                                                                 )
```

7. 现在体验到了，网站数据一多，执行操作起来就很卡，删除所有数据不是马上的事情。

#### 添加video动作

1. 遇到了`animatedCoverUrl`字段报错，添加一个判断就可以了

```
                if result["animatedCoverUrl"] == None:
                    result["animatedCoverUrl"] = "一直没有"
```

2. 遇到状态没有改变的问题，把转台赋值语句写在for外面

```
 def myvideoMP4(self,request,queryset):
        cData = currentData()
        for qu in queryset:
            thevideo = userdetailSpider(qu.userID,cData.theCookie)
            thevideo.start_spider()
            results = thevideo.endResult

            ttUser = UserTitle.objects.get(userID=qu.userID)
            for result in results:

                if result["animatedCoverUrl"] == None:
                    result["animatedCoverUrl"] = "一直没有"
                print(result["videoID"])
                time.sleep(1)
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
```

3. 就是这样把，还有个问题没解决。填入的数据又很多时重复的。我增加了1秒的延迟还是不行
4. 现在去看一下原生的endResult的数值

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210313125302.png)

> 对象输出的数据是重复的，是爬虫的问题

5. 应该是我吧endResult属性写在了，\__init__中，而且初始化为空列表。
6. 应该是这个地方逻辑的问题

```
 #-------------具体提取数据----------#写到这里想起了，我应该是通过live获取视频信息
            result = {}     #信息存储在字典中
            for feeds in feeds_list:
                result["caption"] = feeds["photo"]["caption"]
                result["coversUrl"] = feeds["photo"]["coverUrl"]
                result["videoID"] = feeds["photo"]["id"]
                result["videoPath"] = feeds["photo"]["photoUrl"]
                result["likeCount"] = feeds["photo"]["likeCount"]
                result["realLikeCount"] = feeds["photo"]["realLikeCount"]
                result["animatedCoverUrl"] = feeds["photo"]["animatedCoverUrl"]
                self.endResult.append(result)
                print(result)
                #-----------待会再这里编写存储到数据库的函数--------------
```

7. 确实，改成这样就没问题了

```
            #-------------具体提取数据----------#写到这里想起了，我应该是通过live获取视频信息
            # result = {}     #信息存储在字典中
            for feeds in feeds_list:
                result = {}
                result["caption"] = feeds["photo"]["caption"]
                result["coversUrl"] = feeds["photo"]["coverUrl"]
                result["videoID"] = feeds["photo"]["id"]
                result["videoPath"] = feeds["photo"]["photoUrl"]
                result["likeCount"] = feeds["photo"]["likeCount"]
                result["realLikeCount"] = feeds["photo"]["realLikeCount"]
                result["animatedCoverUrl"] = feeds["photo"]["animatedCoverUrl"]
                self.endResult.append(result)
                print(result)
                del result
                #-----------待会再这里编写存储到数据库的函数--------------
```

8. 准备录演示视频的，过程中有一个主播，出现**视频没有爬取完全的问题**
9. 测试爬取是完整的，可能是我在执行动作的时候点击别的给终端了把。
10. 那个爬取全部视频的运行时间有些长，先不录视频了。

#### 完善Live对象

> 本来应该去做后台统计和获取热门页面的userid和name的，但是有些不甘心，想把获取相册的对象写完整，这样就可以产看是否否获取到了全部作品了。

1. 刷新了好几次页面，还是显示不了作品。
2. 然后尝试live+ksID，可以访问，那么，就需要调用库里面已经存储的ksID来进行相关逻辑的编写。
3. 成功，这是不包含相册的一条数据

```
{'caption': '“留下来 或者我跟你走”', 'displayView': '903.6w', 'displayLike': '48.1w', 'displayComment': '1.3w', 'imgUrls': [], 'liveID': '3xb7betx499z9um'}
```

4. 视频id和我从video界面获取的是一样的，如果每个都对比一下，会消耗性能，因为video界面可能不包含完整的live中的视频。（后期处理）

- 这是live请求关于相册筛选后的数据

```
{'caption': '不知不觉又长大了一岁，生日快乐🎂', 'displayView': '31w', 'displayLike': '1.1w', 'displayComment': '1949', 'imgUrls': ['http://tx2.a.yximgs.com/ufile/atlas/MTI3MjAyMjYyXzc1MTAzNjU0ODA=_0.webp', 'http://tx2.a.yximgs.com/ufile/atlas/MTI3MjAyMjYyXzc1MTAzNjU0ODA=_1.webp', 'http://tx2.a.yximgs.com/ufile/atlas/MTI3MjAyMjYyXzc1MTAzNjU0ODA=_2.webp', 'http://tx2.a.yximgs.com/ufile/atlas/MTI3MjAyMjYyXzc1MTAzNjU0ODA=_3.webp', 'http://tx2.a.yximgs.com/ufile/atlas/MTI3MjAyMjYyXzc1MTAzNjU0ODA=_4.webp', 'http://tx2.a.yximgs.com/ufile/atlas/MTI3MjAyMjYyXzc1MTAzNjU0ODA=_5.webp', 'http://tx2.a.yximgs.com/ufile/atlas/MTI3MjAyMjYyXzc1MTAzNjU0ODA=_6.webp', 'http://tx2.a.yximgs.com/ufile/atlas/MTI3MjAyMjYyXzc1MTAzNjU0ODA=_7.webp'], 'liveID': '3xmm5g93pqgd8tc'}
```

> 忘记了播放量是个很重要的数据，还是要重新遍历一遍，然后添加字段

5. 这篇博客介绍了存储数组：https://zhuanlan.zhihu.com/p/88145941
6. 删除了migrations里面的刚才创建数据库迁移的文件,出现问题

```
django.db.utils.OperationalError: table "app01_userphoto" already exists
```

- 参考这里解决的：https://blog.csdn.net/roy8666/article/details/104634195

7. 我创建的那个列表字段是填写数字的，没注意。我进源文件看了一下，好像还可以添加多个图片

```
def get_available_image_extensions():
    try:
        from PIL import Image
    except ImportError:
        return []
    else:
        Image.init()
        return [ext.lower()[1:] for ext in Image.EXTENSION]


def validate_image_file_extension(value):
    return FileExtensionValidator(allowed_extensions=get_available_image_extensions())(value)
```

8. 直接当作字符串存起来，也好分割成列表。
9. 这是创建的的model

```
class UserPhoto(models.Model):
    photoID = models.CharField(max_length=128,verbose_name="相册id",default="xxxxxxxx")
    caption = models.CharField(max_length=512,verbose_name="相册描述",default="暂无")
    displayView = models.CharField(max_length=32,verbose_name="播放量",default="-1")
    displayLike = models.CharField(max_length=32,verbose_name="点赞数",default="-1")
    displayComment = models.CharField(max_length=32,verbose_name="评论数",default="-1")



    imgUrls = models.CharField(max_length=5000,default=" ")


    def __str__(self):
        # print(self.videoID)
        return self.photoID

    class Mate:
        verbose_name = verbose_name_plural = "相册信息"
```

10. 上面忘记添加了主键，我添加后报错

```
django.db.utils.OperationalError: no such column: app01_userphoto.theUser_id
```

> 差点真的删除或者迁移数据库，解决办法是添加字段，但这个很奇怪，不知道怎么添加。然后我注释主键字段，访问成功。原来里面还有条数据，估计就是这条数据没有主键导致报错。

11. 还是报这个错误。

12. 解决了，我之前这个字段是theUser，和上面的是相同的，改一下名字就好了。

```
    thephotoUser = models.ForeignKey(UserTitle,on_delete=models.CASCADE)
```

13. 数据库里面添加字段，**不需要使用延时**

```
http://tx2.a.yximgs.com/ufile/atlas/9e53e8ba157f445c88009a4dce85fe16_0.webphttp://tx2.a.yximgs.com/ufile/atlas/9e53e8ba157f445c88009a4dce85fe16_1.webphttp://tx2.a.yximgs.com/ufile/atlas/9e53e8ba157f445c88009a4dce85fe16_2.webphttp://tx2.a.yximgs.com/ufile/atlas/9e53e8ba157f445c88009a4dce85fe16_3.webphttp://tx2.a.yximgs.com/ufile/atlas/9e53e8ba157f445c88009a4dce85fe16_4.webp
```

14. 要添加分割符号,测试时候才发现的

```
photoUrl = ','.join(result["imgUrls"])
```

```
http://tx2.a.yximgs.com/ufile/atlas/MTI3MjAyMjYyXzE2NjAyMDc0NjI3XzE1NjYyODAxNTQ5MTc=_0.webp,http://tx2.a.yximgs.com/ufile/atlas/MTI3MjAyMjYyXzE2NjAyMDc0NjI3XzE1NjYyODAxNTQ5MTc=_1.webp,http://tx2.a.yximgs.com/ufile/atlas/MTI3MjAyMjYyXzE2NjAyMDc0NjI3XzE1NjYyODAxNTQ5MTc=_2.webp,http://tx2.a.yximgs.com/ufile/atlas/MTI3MjAyMjYyXzE2NjAyMDc0NjI3XzE1NjYyODAxNTQ5MTc=_3.webp,http://tx2.a.yximgs.com/ufile/atlas/MTI3MjAyMjYyXzE2NjAyMDc0NjI3XzE1NjYyODAxNTQ5MTc=_4.webp,http://tx2.a.yximgs.com/ufile/atlas/MTI3MjAyMjYyXzE2NjAyMDc0NjI3XzE1NjYyODAxNTQ5MTc=_5.webp,http://tx2.a.yximgs.com/ufile/atlas/MTI3MjAyMjYyXzE2NjAyMDc0NjI3XzE1NjYyODAxNTQ5MTc=_6.webp,http://tx2.a.yximgs.com/ufile/atlas/MTI3MjAyMjYyXzE2NjAyMDc0NjI3XzE1NjYyODAxNTQ5MTc=_7.webp,http://tx2.a.yximgs.com/ufile/atlas/MTI3MjAyMjYyXzE2NjAyMDc0NjI3XzE1NjYyODAxNTQ5MTc=_8.webp,http://tx2.a.yximgs.com/ufile/atlas/MTI3MjAyMjYyXzE2NjAyMDc0NjI3XzE1NjYyODAxNTQ5MTc=_9.webp,http://tx2.a.yximgs.com/ufile/atlas/MTI3MjAyMjYyXzE2NjAyMDc0NjI3XzE1NjYyODAxNTQ5MTc=_10.webp,http://tx2.a.yximgs.com/ufile/atlas/MTI3MjAyMjYyXzE2NjAyMDc0NjI3XzE1NjYyODAxNTQ5MTc=_11.webp,http://tx2.a.yximgs.com/ufile/atlas/MTI3MjAyMjYyXzE2NjAyMDc0NjI3XzE1NjYyODAxNTQ5MTc=_12.webp,http://tx2.a.yximgs.com/ufile/atlas/MTI3MjAyMjYyXzE2NjAyMDc0NjI3XzE1NjYyODAxNTQ5MTc=_13.webp,http://tx2.a.yximgs.com/ufile/atlas/MTI3MjAyMjYyXzE2NjAyMDc0NjI3XzE1NjYyODAxNTQ5MTc=_14.webp,http://tx2.a.yximgs.com/ufile/atlas/MTI3MjAyMjYyXzE2NjAyMDc0NjI3XzE1NjYyODAxNTQ5MTc=_15.webp,http://tx2.a.yximgs.com/ufile/atlas/MTI3MjAyMjYyXzE2NjAyMDc0NjI3XzE1NjYyODAxNTQ5MTc=_16.webp,http://tx2.a.yximgs.com/ufile/atlas/MTI3MjAyMjYyXzE2NjAyMDc0NjI3XzE1NjYyODAxNTQ5MTc=_17.webp,http://tx2.a.yximgs.com/ufile/atlas/MTI3MjAyMjYyXzE2NjAyMDc0NjI3XzE1NjYyODAxNTQ5MTc=_18.webp
```

15. 现在思考问题，重复执行动作，会不会重复添加了数据，如果是被覆盖了，也是会给数据库增加压力。后期如果数据不完整，需要重新爬取，**需要一个判断操作**。
16. 还有个问题，**个别用户无法获取ksID**，可能需要自己手动添加

## 2021.3.19

#### *添加静态问题问题

> 由于django在**调试**模式下**不能加载静态文件**，导入静态文件不能一般导入，可以使用外部链接。

- setting.py

```
STATICFILES_DIRS = [os.path.join(BASE_DIR,"static"),
]
STATIC_URL = '/static/'
```

- 好吧，我没有配置成功。一般就是这个方式导入吧

```
{% load static %}
{% block title %}管理页面{% endblock title %}
{% block style %}<link rel="stylesheet" type="text/css" href="{% static 'css/showAdmin.css' %}">{% endblock %}
```

- 我看了一下之前写的博客，还是不知道。不纠结了，直接写在内部

## 2021.3.20

#### *获取指定字段的全部数据

- 使用这条语句,返回QuerySet类型。开始是循环提取添加到指定的列表中，这样非常消耗性能。

```
    allCover = UserVideo.objects.values("coversUrl")
```

> 参考博客：https://blog.csdn.net/weixin_33893473/article/details/86278284

#### 继续

1. 遇到了有的视频封面大小不一样的问题

2. 观察了一下，live界面的视频左右两边会有一些空白，vi'deo是刚好填充好，还是按照live页面的样式写吧。

   > 获取图片原始尺寸：https://blog.csdn.net/x550392236/article/details/78723297

3. 再想想，**live界面没有展示的视频，肯定是不好按照那种尺寸展示的视频**

4. 那么，还是先做主播主页的页面吧。

#### 统计数据库中的video和photo

1. 统计每个用户的video数量

```
def showAdmin(request):
    allUser = UserTitle.objects.values("userName","userID")
    for uID in allUser:
        theUsr= UserTitle.objects.get(userID=uID["userID"])
        myVideo = UserVideo.objects.filter(theUser=theUsr.id)
        print(uID)
        print(len(myVideo))

    return render(request,'pages/showAdmin.html',{"result":allUser})
```

> 这些逻辑后面要使用接口触发，不然一进这个视图就触发一次，太消耗时间。

```
http://tx2.a.yximgs.com/ufile/atlas/NTE5MzQ5NDg0MTc0OTc3NzcxOV8xNjE1NjI4ODcwNjA0_0.webp,http://tx2.a.yximgs.com/ufile/atlas/NTE5MzQ5NDg0MTc0OTc3NzcxOV8xNjE1NjI4ODcwNjA0_1.webp,http://tx2.a.yximgs.com/ufile/atlas/NTE5MzQ5NDg0MTc0OTc3NzcxOV8xNjE1NjI4ODcwNjA0_2.webp,http://tx2.a.yximgs.com/ufile/atlas/NTE5MzQ5NDg0MTc0OTc3NzcxOV8xNjE1NjI4ODcwNjA0_3.webp,http://tx2.a.yximgs.com/ufile/atlas/NTE5MzQ5NDg0MTc0OTc3NzcxOV8xNjE1NjI4ODcwNjA0_4.webp,http://tx2.a.yximgs.com/ufile/atlas/NTE5MzQ5NDg0MTc0OTc3NzcxOV8xNjE1NjI4ODcwNjA0_5.webp,http://tx2.a.yximgs.com/ufile/atlas/NTE5MzQ5NDg0MTc0OTc3NzcxOV8xNjE1NjI4ODcwNjA0_6.webp,http://tx2.a.yximgs.com/ufile/atlas/NTE5MzQ5NDg0MTc0OTc3NzcxOV8xNjE1NjI4ODcwNjA0_7.webp
```

2. 获取图片数量的时候出现了多的，可能与爬虫逻辑有关

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210320184211.png)

3. 我查看了一下图片，名字和图片不匹配，确实是逻辑问题
4. 删除存储图片的数据，重新执行动作，数据可以被重复添加。

#### 进一步处理爬虫类和状态表示

> 执行爬虫脚本失败要终止，数据库不能存储到数据库。设计一个状态表示，不能重复存储数据。脚本还是设置延时参数，可以调节。

1. 我做了进一步的处理，请求到result=0，可能不是爬取太快的问题，其他问题。如果reslut=0，再自己浏览器中多刷新几次，直到出现作品，再执行代码result=1.

2. **爬取不完整就放弃**，或者**多次爬取相互补充**。后面数据更新了，自己也要对爬虫进行跟新。

3. 现在要决定一下工作，简单的就是爬取到数据，最后自己写脚本把需要的数据下载到本地。复杂的是写可持续爬虫的代码，官网跟新不修改代码就可以直接爬取过来。如果要作为找工作的项目，就还需要加入用户注册登录系统，可以点赞，关注。再复杂的是评论，上传视频等，这样一做就要考虑其他问题，如doss攻击，服务器内存等问题。代码逻辑新能问题就已经够呛了。

4. 延时设置为5秒，爬取一波是正常的。3秒也正常。然后设置爬取数据不完整，不存储到数据库。

5. ```
   userdetailLiveSpider()
   ```

> 这个类是获取live界面的视频信息，暂时测试延时可以不要。

6. 我设置5状态可以转变为1或者2状态，如果这样回头再执行一遍，应该会出现重复的问题。确实有，**还是入库前要判断一下**。
7. 进行了处理，多次运行出现问题，获取Photo时候获取不了，浏览器刷新也出现不了数据，使用IP代理就别了吧，实在不想就只要vide的视频。
8. 今天要处理的问题估计就没问题。重复运行提取数据就可以了，下一步做随机获取username和userID
9. 唉！真难，以为没有问题出现了死循环。
10. 我把火狐上面的cookie复制过来，可以后去photo

#### 随机获取userID

1. dict与json数据之间的转换：https://blog.csdn.net/qq_33689414/article/details/78307018

## 2021.3.21

#### js发送post

1. 参考博客：http://www.zzvips.com/article/64603.html
2. 然后我又找了个弹出框的插件，现在可以再弹出框填写数据，发送post请求。

```
        $("#openDialog1").dialog({
            id: "superDialog", //必填,必须和已有id不同
            title: "我的标题", //对话框的标题 默认值: 我的标题
            type: 0, //0 对话框有确认按钮和取消按钮 1 对话框只有关闭按钮
            easyClose: true, // 点击遮罩层也可以关闭窗口,默认值false
            form: [{
                description: "用户名",
                type: "text",
                name: "username",
                value: "tom"
            }, {
                description: "密码",
                type: "text",
                name: "password",
                value: "123456"
            }, {
                description: "姓名",
                type: "text",
                name: "name",
                value: "tom"
            }, {
                description: "年龄",
                type: "text",
                name: "age",
                value: "18"
            }], //form 是填充表单的数据,必填
            submit: function (data) {
                //data是表单收集的数据
                console.log(data);

                $.ajax({url: 'http://127.0.0.1:8000/api/getUserRandom/3/',
                        type: 'POST',
                        {#dataType: 'json',#}
                        data:data,
                        beforeSend: function (xhr, setting) {
                            xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}")},
                        success: function (msg) {
                            console.log(msg)},
                })
                //这个可自行删去
                if (true) {
                    alert("提交成功\n（你自己可以去掉这个alert）");
                    //清空表单数据 传递参数=上述指定的id值
                    clearAllData("superDialog");
                }

            }
        })
```

> `xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}")},`这一步很重要

3. 处理一下返回的数据为json格式

```
def getUserRandom(request,counts):
    if request.method == 'POST':
        print("-----------")
        cDate = currentData()
        theGetScript = getUserIDRandom(cDate.theCookie)
        theGetScript.get_data()
        results = theGetScript.endResult
        messgae = json.dumps(results)
        # return render(request,results)
        myRes = json.dumps({"result":2})
        return HttpResponse(myRes)
    else:
        myRes = json.dumps({"result": 1})
        return HttpResponse(myRes)
```

4. 出现上一次相应的数据也添加到下一次相应的数据中了。

> 我把result在函数外定义为全局变量还是不行。result每次的内容不会被清空，对象的endResult会被清空，我就直接把这个作为返回值

5. 还是这个问题，我赋值给返回值，把属性值都清空了都还是那样。

#### 又有问题

1. 获取精彩视频页面也会被限制，我去浏览器刷新也刷新不出视频。看来，看来一切不是那么如意。需要赶快结束这个项目，展示页面就重新开启一个项目把。这个项目就用来写爬虫，把数据存储到数据库。
2. 估计真的是要http代理了。尝试了一下，貌似不是封锁ip的问题。确实不是，我连接手机热点还是那个样子。
3. 我发现了，退出登录，然后再访问就是正常的。但是我复制cookie，代码还是无法获取信息。真是搞不懂。可能是某个账户对某个页面请求的次数太多就出现问题把。
4. 问题是现在不知道怎么恢复，填上退出登录的cookie页不行。

#### 睡了一觉

1. 我去睡了一觉，醒来后再去执行代码，成功可以获取信息。那么就可以继续进行了，其他获取不到数据可能也是这样就可以了，**不是cookie问题**，因为自己再下一次写代码的时候，执行爬虫脚本开始都是成功的。
2. 卧槽！我再mytools中测试类成功得到数据，在后端执行动作老是不成功，cookie更换得也是一样的。还有最后一个头像地址，正好看到一个错位的。真想放弃，都做到这里了。继续找原因吧。
3. 我去吃了个饭，星期天下午的菜真的不行。点了两个肉菜，肉不好吃把里面的青菜给吃了，还伴着油水把饭吃了。去买泡面的时候迷糊地多付了一元钱，拿了两根棒棒糖。
4. 我上来在测试的时候，后台动作添加video是成功的，感觉还好，我就觉得自己的代码写得没有问题，可能是测试的用户不同，添加photo有问题。
5. 使用result判断是否有数据出现错误，没有数据状态也改变了。直接使用长度来判断。
6. 在setting中调用类中的ksCookie的问题，我在mytools中调用也是获取不到数据。
7. 可能是全局变量引入的方式，我get到了再\__init__文件下面设置变量，这样引入就可以了

```
from app01 import KSCOOKIE
```

8. 成功，后端执行不成功，就是导入变量的问题。

#### 其他

1. 发现问题，获取photo的时候，需要每次更新cookie，就是从成功请求到数据的浏览器中获取。多增加一个用户都不行。

> 好吧，我说把kscookie复制到了THECOOKIE

2. 我不知道以前是怎么搞的，延时就可以使用一个cookie多次获取视频信息。

> 如果video+photo不等于应该作品数量，就需要再live界面获取视频，对比入库。这是可能遇到的问题，先写一下。

3. 我观察了一下，每次就是cookie中这个参数改变了。

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210321192129.png)

4. 确实，还是要想办法获取cookie。
5. 我以为这个工程要烂尾了，因为cookie最后的一个值我没有对比到。但是，我把上面的最上面请求的cookie复制过来还是可以运行。
6. 好吧，还是一次性的。我都怀疑自己之前是怎么做到使用延迟，可以多次复用。
7. 不行不行，还是对应请求的cookie好用。
8. 确实好用，就是不知道怎么获取。变的就是最后面的那条数值
9. 我还是按照这篇博客一步步地做把，说不定成功了，博客：https://blog.csdn.net/qq_43661709/article/details/113278957
10. 获取二维码成功，要不是博客中说要加data:image/png;base64,我恐怕怎么也想不出来。
11. 这个信息填在这里也多亏了这篇博客

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210321203138.png)

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210321203221.png)

12. 扫描的结果中提取了登录信息，响应后返回的是用户信息，然后携带登录信息登录。

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210321204036.png)

13. acceptResult请求获取qrtoken

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210321203958.png)



14. qrtoken的值再这个表单里被发送出去

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210321204228.png)

- 返回的信息

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210321204345.png)

15. 然后就是这个GET请求，携带的数据博客里面有解释

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210321205406.png)

16. 三个变动的参数，每次都要交替更换，通过这样一波操作来获取动态的cookie。

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210321205613.png)

17. 把这三个字段替换，然后作为下一次请求个人信息的cookie才有效。

#### 用户界面分析

1. 这是刷新一下，下滑一下发送的数据

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210321210348.png)

> 我猜测passToken和sts？依次更新了cookie，然后在请求数据。下面第一个graphql是登录用户的个人信息，第二个是第一页面视频列表，下面v？又跟新了依次cookie，然后用这个cookie就可以一直获取视频列表了。

2. 现在要知道passToken中的cookie中的passToken参数值怎么获取。

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210321211816.png)

> 我现在知道cookie是怎么获取的了，不是自己构建，而是根据响应数据中set-Cookie参数设定的。之前健康打卡系统就是没有使用上一次生成的cookie而失败的，不能自己构建。

3. cookie肯定是get请求获取的，因为我筛选的是XRH没有看到GET请求。好吧，全部里面也没有，无法获取。
4. 我使用这个gra中的cookie，可以爬取一个完整用户的视频。这个cookie可以获取到。有的不能，可能是最后依次请求到的数据为空，然后判断爬取信息不完整。

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210321222354.png)

5. 这样每次只能爬取一个用户的视频，然后再更新cookie。
6. 使用初次登录后更新cookie就可以获取数据。也是一次性的。现在要知道怎么更新。

#### psotman发现

1. 我用post模拟，到passToken的模拟才有效，前面的是token错误的返回值。

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210321225410.png)

2. ok，**模拟passtoken得到响应的"kuaishou.server.web.at“的值，作为下一次sts的params，然后sts就可以成功返回需要跟新的cookie三个字段，再和cookie固定的值凭借，就可以生成一个有效的cookie爬取一个主播的用户全部视频信息。**

3. ok，下次就就需要把cookie拼接起来，封装成类就可以了

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210321232253.png)

## 2021.3.24

#### updateCookie类

1. jupyterlab的相关的文件放在notebook/01/passToken下
2. 测试好了，写类的时候遇到一个问题，第一个替换我没有做处理，相关字段没有server.web_st=。但是替换另一个的时候也每做处理，最后却添加了server.web_st=。结果是想要的，但不知道为什么

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210324081339.png)

3. 不好意思，是代码写错了。

![](https://gitee.com/liangxinixn/blog002/raw/master/image01/20210324082430.png)

4. 写好了，执行爬取video的时候更新一下cookie
5. 准备体验一下成果的时候，发现失败，程序终止。回头看一下，原来是掉了分号

```
 "server.web_st="+st+";"
```

6. 我都想好了等下测试成功了怎么写什么，但是失败了。
7. 我尝试了删除类，每次请求都更新依次cookie，但还是失败。不知道为什么，难道请求的cookie与动作有关，或者前后cookie是由关联的。
8. 好吧，我先暂停一下，好好整理一下爬虫相关的代码。既然不用持续更新视频，执行依次得到结果，那么就可以不把获取视频的代码写在工程里面了。