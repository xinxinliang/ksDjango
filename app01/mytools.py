import requests
import time
from app01 import KSCOOKIE,THECOOKIE
import re
'''参数说明
endResult
-2:第一次请求就失败
-1:请求到了，但里面没数据
0:爬取数据不完整
'''



# 获取video界面的视频信息
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

    endResult = []
    endStatus = -1
    def __init__(self,userID,myCookie,tDelay=5):
        userdetailSpider.headers["Referer"] = "https://video.kuaishou.com/profile/"+userID
        userdetailSpider.payload["variables"]["userId"] = userID
        userdetailSpider.headers["Cookie"] = myCookie
        self.tDelay = tDelay


    def get_data(self):
        #--------------请求页面--------------#
        try:
            time.sleep(self.tDelay)
            res = requests.post(userdetailSpider.URL, headers=userdetailSpider.headers, json=userdetailSpider.payload)
            res.encoding = "utf-8"
            m_json = res.json()  # 字典格式

            #-------------诗筛选数据-------------#
            #*******************************************************************#
            # 这个result参数判断请求是否正确，如果不是1请求失败，后面继续执行会报错，程序结束
            # print(m_json["data"]["visionProfilePhotoList"]["result"])
            feeds_list = m_json["data"]["visionProfilePhotoList"]["feeds"]
            if len(feeds_list) != 0:
                # print("请求成功，开始筛选数据")
                pass
            else:
                # print("请求数据失败，无法筛选，程序终止")
                # print("请求到了，没有数据")
                return -1




            # 获取pcursor并且填写到下一次的header中
            pcursor = m_json["data"]["visionProfilePhotoList"]["pcursor"]
            userdetailSpider.payload["variables"]["pcursor"] = pcursor

            #-------------具体提取数据----------#写到这里想起了，我应该是通过live获取视频信息
            # result = {}     #信息存储在字典中

            print("开始筛选数据")
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
                # print(result)
                del result
                #-----------待会再这里编写存储到数据库的函数--------------

            #print(m_json)
            #print(feeds_list)
            #print(pcursor)

            if pcursor == "no_more":
                return 0
        except:
            # print("页面请求错误，请检查cookie是否过期，id是否正确")
            return -2


    def start_spider(self):
        while(1):
            temp = userdetailSpider.get_data(self)
            self.endStatus = temp
            if temp == 0:
                print("顺利爬取完成,程序终止")
                break
            if temp == -1:
                print("爬取失败，不完整,程序终止")
                break
            if temp == -2:
                print("请求失败,程序终止")
                break


# 输出快手ID和cookie,获取live界面的视频信息
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

    payload = {"operationName":"publicFeedsQuery","variables":{"principalId":"tuziya555","pcursor":"","count":24},"query":"query publicFeedsQuery($principalId: String, $pcursor: String, $count: Int) {\n  publicFeeds(principalId: $principalId, pcursor: $pcursor, count: $count) {\n    pcursor\n    live {\n      user {\n        id\n        avatar\n        name\n        __typename\n      }\n      watchingCount\n      poster\n      coverUrl\n      caption\n      id\n      playUrls {\n        quality\n        url\n        __typename\n      }\n      quality\n      gameInfo {\n        category\n        name\n        pubgSurvival\n        type\n        kingHero\n        __typename\n      }\n      hasRedPack\n      liveGuess\n      expTag\n      __typename\n    }\n    list {\n      id\n      thumbnailUrl\n      poster\n      workType\n      type\n      useVideoPlayer\n      imgUrls\n      imgSizes\n      magicFace\n      musicName\n      caption\n      location\n      liked\n      onlyFollowerCanComment\n      relativeHeight\n      timestamp\n      width\n      height\n      counts {\n        displayView\n        displayLike\n        displayComment\n        __typename\n      }\n      user {\n        id\n        eid\n        name\n        avatar\n        __typename\n      }\n      expTag\n      isSpherical\n      __typename\n    }\n    __typename\n  }\n}\n"}
    def __init__(self,userId,myCookie):
        self.headers["Referer"] = "https://live.kuaishou.com/profile/"+userId
        self.payload["variables"]["principalId"] = userId
        self.headers["Cookie"] = myCookie

    endResult = []
    endStatus = -1
    def get_data(self):
        try:
            myTest = updateCookie()
            myTest.updateCo()
            self.headers["Cookie"] = myTest.theResult
            time.sleep(5)
            res = requests.post(self.URL, headers=self.headers, json=self.payload)
            res.encoding = "utf-8"
            m_json = res.json()  # 字典格式

            # if m_json["data"]["visionProfilePhotoList"]["result"] == 1:
            #     # print("请求成功，开始筛选数据")
            #     pass
            # else:
            #     # print("请求数据失败，无法筛选，程序终止")
            #     # print("请求到了，没有数据")
            #     return -1

            feeds_list = m_json["data"]["publicFeeds"]["list"]
            pcursor = m_json["data"]["publicFeeds"]["pcursor"]
            self.payload["variables"]["pcursor"] = pcursor
            # print(m_json)
            # print(len(feeds_list))
            if len(feeds_list) == 0:
                return -1
            #-------------筛选数据---------------#

            for feeds in feeds_list:
                result = {}
                result["caption"] = feeds["caption"]
                # 播放量，点赞数，评论数
                result["displayView"] = feeds["counts"]["displayView"]
                result["displayLike"] = feeds["counts"]["displayLike"]
                result["displayComment"] = feeds["counts"]["displayComment"]
                # 相册，可能为空，可能为列表
                result["imgUrls"] = feeds["imgUrls"]
                result["liveID"] = feeds["id"]
                # print(result)
                self.endResult.append(result)
                del result

            if pcursor == "no_more":
                return 0
        except:
            print("页面请求错误，请检查cookie是否过期，id是否正确")
            return -2



    def start_spider(self):
        while(1):
            temp = self.get_data()
            self.endStatus = temp
            if temp == 0:
                break
            if temp ==-1:
                print("数据不完整，程序终止")
                break
            if temp == -2:
                break
# 获取live页面的主播信息
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

            # print(result)
            return result

        except:
            print("页面请求错误，请检查cookie是否过期，id是否正确")

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

            # print(result)
            return result

        except:
            print("页面请求错误，请检查cookie是否过期，id是否正确")

# 从热门界面随机获取userID
class getUserIDRandom():
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
        "Referer": "https://video.kuaishou.com/brilliant",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57"
    }
    # 这里的userID也要更改
    payload = {"operationName":"brilliantTypeDataQuery","variables":{"hotChannelId":"00","page":"brilliant","pcursor":"1"},"query":"fragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    id\n    duration\n    caption\n    likeCount\n    realLikeCount\n    coverUrl\n    photoUrl\n    coverUrls {\n      url\n      __typename\n    }\n    timestamp\n    expTag\n    animatedCoverUrl\n    distance\n    videoRatio\n    liked\n    stereoType\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  __typename\n}\n\nfragment photoResult on PhotoResult {\n  result\n  llsid\n  expTag\n  serverExpTag\n  pcursor\n  feeds {\n    ...feedContent\n    __typename\n  }\n  webPageArea\n  __typename\n}\n\nquery brilliantTypeDataQuery($pcursor: String, $hotChannelId: String, $page: String, $webPageArea: String) {\n  brilliantTypeData(pcursor: $pcursor, hotChannelId: $hotChannelId, page: $page, webPageArea: $webPageArea) {\n    ...photoResult\n    __typename\n  }\n}\n"}
    endResult = []
    def __init__(self, myCookie,myDelay=1):
        userdetailSpider.headers["Cookie"] = myCookie
        self.myDelay = myDelay
    def get_data(self):
        try:
            time.sleep(self.myDelay)
            res = requests.post(self.URL, headers=self.headers, json=self.payload)
            res.encoding = "utf-8"
            m_json = res.json()  # 字典格式
            print(m_json)
            feed_list = m_json["data"]["brilliantTypeData"]["feeds"]
            if len(feed_list) == 0:
                print("爬取数据不完整")
                return -1

            for feed in feed_list:
                result = {}
                result["userID"] = feed["author"]["id"]
                result["userName"] = feed["author"]["name"]
                self.endResult.append(result)
                del result
            print("爬取成功")
            return 1
        except:
            print("请求出错")
            return -2

# 这个类用来更新cookie
class updateCookie():
    URL = "https://id.kuaishou.com/pass/kuaishou/login/passToken?sid=kuaishou.server.web"
    headers = {
        "User-Agent": "PostmanRuntime/7.26.8",
        "Cookie": r"clientid=3; did=web_ec874916e390b9741609686125a0452e; didv=1613879531823; client_key=65890b29; userId=427400950; userId=427400950; passToken=ChNwYXNzcG9ydC5wYXNzLXRva2VuErAB09Fn22HHUFs4Muop_XipNpYKJcYFg9Jxuu1cpGUyrlyqwscZGXc02So9rJOGl-aV3Ad5POwpdoopjqlQ7wq35oV0B0mEwKqN-6i7NVeJKJTaNltILNf56B54DZgSGUtMri9iTzj0vtrvpCHEqn7L1rVYT-nGlKOOkFEYauGEOnmDnvjUc7QD2L1sSXzzc4NrUUZhi6O3-kyBsJsymw4a4JkMDJKliJ0QZTu7IYuvqcgaEq_TRjgPx0oylueuj07Lsb3GDSIgnerr8DS_ycF2jLwXujOPPMFSEyNXlE2yqH8OssiW5fQoBTAB",
    }

    URL2 = 'https://video.kuaishou.com/rest/infra/sts'
    headers2 = {
        "Connection": "keep-alive",
        "User-Agent": "PostmanRuntime/7.26.8",
        "Cookie": r"kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; did=web_ec874916e390b9741609686125a0452e; didv=1613879531823; client_key=65890b29; userId=427400950; kuaishou.server.web_st=ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqABssQl6l3ZcO5tFu_4shEFNlhh-s0CWRRIm36xWGDANPDx6QPnCbqh0mA-TYGd4vv2WrowlcuyPxKMOE1kdVg_AOuxtlRnpS7f8zMVPhZApB2r6ECnb4E_47FJYPeb90TLm5YVDLfYFHAVgpm75p738ANPRImWdfffvHiEqncJdn1gW7yu0CYtyWqdtQbbD2Mus8s7UWF76_yDR1eQsoV9ABoStEyT9S95saEmiR8Dg-bb1DKRIiBuycuMJFuiLwe5GcmxD88aQEj5tcH62oYBN1kzrniFkCgFMAE; kuaishou.server.web_ph=2b4ed626e5e599d8fb6b4d7bfb25ac557f0f"
    }
    theResult = ""
    def __init__(self):
        self.theCookie = THECOOKIE

    def updateCo(self):
        # 获取authtoken，作为参数请求新的cookie字段
        res = requests.post(self.URL, headers=self.headers)
        res.encoding = "utf-8"
        m_json = res.json()  # 字典格式
        # print(m_json["kuaishou.server.web.at"])

        # 获取新的cookie字段
        params = {
            "authToken": m_json["kuaishou.server.web.at"],
            "sid": "kuaishou.server.web"
        }
        res2 = requests.get(self.URL2, headers=self.headers, params=params)
        content = res2.text
        # print(content)
        # "kuaishou.server.web_st" "kuaishou.server.web_ph" 把这两个字段替换掉cookie中，"userId"这个字段一直是没变

        # 切分字符串，检查没有错误。这两个字段不用那么麻烦，把conten转换为json格式提取，这里先不改了
        tempCont = content.split(",")
        st = tempCont[1].split(":")[1].replace('"', '')
        ph = tempCont[3].split(":")[1].replace('"', '')

        cookie_1 = re.sub(r"server.web_st=(.*);", "server.web_st="+st+";", self.theCookie)
        # print(cookie_1)
        self.theResult = re.sub(r"web_ph=(.*)", "web_ph=" + ph, cookie_1)
        # print(theResult)
        # print(self.theCookie)




if __name__ == "__main__":
    theUserID = "3xriu7h3usw65fu"
    ksUserID = "DD666-com"
    #userdetailLiverCookie = "clientid=3; did=web_ec874916e390b9741609686125a0452e; didv=1613879531823; client_key=65890b29; kpn=GAME_ZONE; userId=427400950; userId=427400950; kuaishou.live.bfb1s=477cb0011daca84b36b3a4676857e5a1; kuaishou.live.web_st=ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgAdzAK_gR4Ij6ikaIFBnhSOQxjHjg4FMAJvD1I-Yb6wkeKkKmy1Y6CHVQVFHo9jkSGfI454cXJaxmHXgE3XD8TcB4HpCEJInTt3sr5OB036DE-W1vQO6_ZNcIcC7FBFZkYcphYw8fcoS7aTlggtrqEg1dZ1-9TWPUQeSV7YuGWRsPTAbyNVdVkRBbGzo05zoRDYpD7h7Sh4VRnVNWGQhehsEaEm-zwBmcbUA4lm5ejQnh9kVjySIgeeee0vVwC8b9JjYLJRhQYNFs4Yg7ugEhW9jEGgDPo_YoBTAB; kuaishou.live.web_ph=9a524ac5ba8b5428550c80f8aa3a8cbbbd98"
    ksCookie = "clientid=3; did=web_a84ab30c11148a28c973b207b8913792; client_key=65890b29; kpn=GAME_ZONE; kuaishou.live.web_st=ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgAaPpEYy-UYx_bkxtnQP7J3TlMsPWnJct2malDdboJd95f6gtrY4f8JsWcPGVjc8Kn524DATADJYAsQvPDzwhc-lqAUIj6JZ1djYndPRyPo79_aoWS5PTn7o5gEnhoVuz2aSsqf9H0vGkzZBUrgGioWgqEOhqYHUdzGd0bTHFXlaY6gTa3pzZEh4dpDZv0mI62yvP36R2dahKdVkOCcED5UoaEvrof_XznEP1qd2QsxhyybtifyIgnqYWGmSnhYUuKU6CH30N4ehu9EWTAZYaxtDzsnZs8YYoBTAB; kuaishou.live.web_ph=823c5ace4afa0a327168389d21c94d243c06; userId=427400950; kuaishou.live.bfb1s=3e261140b0cf7444a0ba411c6f227d88"
    test = updateCookie()
    test.updateCo()
    print(test.theCookie)
    print(test.theResult)




    # test = userdetailSpider(theUserID,THECOOKIE)
    # test = userdetailLiveSpider(ksUserID,KSCOOKIE)
    # print(KSCOOKIE)
    # test = ksLiveSpider(ksUserID,ksCookie)
    # test.start_spider()
    # print(test.endResult)

    # test = getUserIDRandom(theCookie)
    # test.get_data()
    # print(test.endResult)


