import requests
import time
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
    def __init__(self,userID,myCookie,tDelay=3):
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
            if m_json["data"]["visionProfilePhotoList"]["result"] == 1:
                # print("请求成功，开始筛选数据")
                pass
            else:
                # print("请求数据失败，无法筛选，程序终止")
                # print("请求到了，没有数据")
                return -1


            feeds_list = m_json["data"]["visionProfilePhotoList"]["feeds"]

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
            time.sleep(1)
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
            # print(feeds_list)
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
        "User-Agent": "PostmanRuntime/7.26.8"
    }
    # 这里的userID也要更改
    payload = {"operationName":"brilliantTypeDataQuery","variables":{"hotChannelId":"00","page":"brilliant","pcursor":"1"},"query":"fragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    id\n    duration\n    caption\n    likeCount\n    realLikeCount\n    coverUrl\n    photoUrl\n    coverUrls {\n      url\n      __typename\n    }\n    timestamp\n    expTag\n    animatedCoverUrl\n    distance\n    videoRatio\n    liked\n    stereoType\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  __typename\n}\n\nfragment photoResult on PhotoResult {\n  result\n  llsid\n  expTag\n  serverExpTag\n  pcursor\n  feeds {\n    ...feedContent\n    __typename\n  }\n  webPageArea\n  __typename\n}\n\nquery brilliantTypeDataQuery($pcursor: String, $hotChannelId: String, $page: String, $webPageArea: String) {\n  brilliantTypeData(pcursor: $pcursor, hotChannelId: $hotChannelId, page: $page, webPageArea: $webPageArea) {\n    ...photoResult\n    __typename\n  }\n}\n"}
    endResult = []
    def __init__(self, myCookie):
        userdetailSpider.headers["Cookie"] = myCookie

    def get_data(self):
        try:
            res = requests.post(self.URL, headers=self.headers, json=self.payload)
            res.encoding = "utf-8"
            m_json = res.json()  # 字典格式
            # print(m_json)
            stateResult = m_json["data"]["brilliantTypeData"]["result"]
            if stateResult != 1:
                return -1
            feed_list = m_json["data"]["brilliantTypeData"]["feeds"]

            for feed in feed_list:
                result = {}
                result["userID"] = feed["author"]["id"]
                result["userName"] = feed["author"]["name"]
                self.endResult.append(result)
                del result
        except:
            print("请求出错")

if __name__ == "__main__":
    theCookie = "kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; clientid=3;Max-Age=8640000; did=web_ec874916e390b9741609686125a0452e; didv=1613879531823; client_key=65890b29; userId=427400950; kuaishou.server.web_st=ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqABQrFWsr52Mhp5GfcmignSLoddGbbCBCTAkyedrcLkHqxI9IIdilOuxFUWwhS41WnVKwFJ0Win96_M-frAXGNXXDx78d0FjGOylLgeVtcXUGsIkgyxVkopf2IR_Pvps61IaXw1XTHZOdTrwQkDIdwESPDssQTuW9XNIfjJK9e88ZgJYNJI5bK5n38Zm37kl8omE8R8E8ZhL87TgGpaRZq3XRoSTdCMiCqspRXB3AhuFugv61B-IiBO8gZCTy1dvCTjyGg0IEN6MrmkUACDgSB3T2BYkkBQ-SgFMAE; kuaishou.server.web_ph=dfcba445b9b7f619411fdced6b1e61d6f207"
    theUserID = "3xriu7h3usw65fu"
    ksUserID = "HBL66888"
    #userdetailLiverCookie = "clientid=3; did=web_ec874916e390b9741609686125a0452e; didv=1613879531823; client_key=65890b29; kpn=GAME_ZONE; userId=427400950; userId=427400950; kuaishou.live.bfb1s=477cb0011daca84b36b3a4676857e5a1; kuaishou.live.web_st=ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgAdzAK_gR4Ij6ikaIFBnhSOQxjHjg4FMAJvD1I-Yb6wkeKkKmy1Y6CHVQVFHo9jkSGfI454cXJaxmHXgE3XD8TcB4HpCEJInTt3sr5OB036DE-W1vQO6_ZNcIcC7FBFZkYcphYw8fcoS7aTlggtrqEg1dZ1-9TWPUQeSV7YuGWRsPTAbyNVdVkRBbGzo05zoRDYpD7h7Sh4VRnVNWGQhehsEaEm-zwBmcbUA4lm5ejQnh9kVjySIgeeee0vVwC8b9JjYLJRhQYNFs4Yg7ugEhW9jEGgDPo_YoBTAB; kuaishou.live.web_ph=9a524ac5ba8b5428550c80f8aa3a8cbbbd98"
    ksCookie = "clientid=3; did=web_ec874916e390b9741609686125a0452e; didv=1613879531823; client_key=65890b29; kpn=GAME_ZONE; userId=427400950; userId=427400950; kuaishou.live.bfb1s=9b8f70844293bed778aade6e0a8f9942; kuaishou.live.web_st=ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgAe80TZ_u8McFZcsMijAFvmllcC7B7XWwf5RLpOBglOaq2_rSvyww6weHGzttGmZ3oakyVVQ6L29TShONEbMPwG2AjP9irZ84ImqAbKAGUh7vt6kV-aaqwXuxvDf1Fgp5HgO_gyUKRv0RkWZvaS4JJFZG8ymK3yv3_ggyixAiJkFwSDz-j-8MuKZzY8wHIiM6LHckuOfAxtXK4fsGbT7AOrsaEpGRdADNj0HroX-OzPO0ZFU2uiIgwshWG4pXfG_qa3Bi8FNVAkz-COuTODS33sqz2-lKebooBTAB; kuaishou.live.web_ph=ce412f4b5cc780c5c24246e904f86e93c634"
    # test = userdetailLiveSpider(theUserID,ksCookie)
    # test = ksLiveSpider(ksUserID,ksCookie)
    # test.get_data()
    # print(test.endResult)
    test = getUserIDRandom(theCookie)
    test.get_data()
    print(test.endResult)

