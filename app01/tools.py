import requests
import json
import os
import time
from app01.models import UserTitle
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
    "Referer": "https://video.kuaishou.com/profile/3xsms2z7ft9fmhg",
    "User-Agent": "PostmanRuntime/7.26.8"
}

payload = {"operationName":"visionProfileUserList","variables":{"ftype":1},"query":"query visionProfileUserList($pcursor: String, $ftype: Int) {\n  visionProfileUserList(pcursor: $pcursor, ftype: $ftype) {\n    result\n    fols {\n      user_name\n      headurl\n      user_text\n      isFollowing\n      user_id\n      __typename\n    }\n    hostName\n    pcursor\n    __typename\n  }\n}\n"}


def get_data():
    res = requests.post(URL, headers=headers, json=payload)
    res.encoding = "utf-8"
    m_json = res.json()  # 字典格式

    fols_list = m_json["data"]["visionProfileUserList"]["fols"]

    pcursor = m_json["data"]["visionProfileUserList"]["pcursor"]
    payload["variables"]["pcursor"] = pcursor

    for fols in fols_list:
        userID = fols["user_id"]
        userName = fols["user_name"]
        # 提交请求把数据填到数据库
        add_data(userID,userName)
        # 需要设置延迟
        time.sleep(1)
        print("userID:%s-------userName:%s" % (userID, userName))
    if pcursor == "no_more":
        return 0



def add_data(userID,userName):
    if not UserTitle.objects.filter(userID=userID):
        UserTitle.objects.create(userID=userID, userName=userName)
        print("ID为%s的用户存入数据库成功++++++++++++++"%(userID))
    else:
        print("ID为%s的用户已经存在数据库---------------" % (userID))


def start_data():
    while (1):
        temp = get_data()
        if temp == 0:
            break
    print("---------------------当前用户地址完成-------------------")

if __name__ == "__main__":
    start_data()