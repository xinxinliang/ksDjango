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