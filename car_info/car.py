import os
import json
import requests
from bs4 import BeautifulSoup

import fake_useragent

param={ #作为request的参数，只需要定义UA即可，如果还不行，就补充其他参数
    "User-Agent":fake_useragent.UserAgent().chrome
}

base_url="https://www.pcauto.com.cn/zt/chebiao/"
country_list=["guochan","riben","deguo","faguo","yidali","yingguo","meiguo","hanguo","qita"]

def get_car_info(car_name,car_url):#获取单一品牌的汽车标识和介绍
    res=requests.get(car_url,params=param)
    res.encoding = "GBK" #网页编码格式是gb2312
    soup=BeautifulSoup(res.text,"html.parser")

    article=soup.find_all("div",class_="article")[0] #只用找到正文所在的div块就行了，只有一个
    info=article.stripped_strings #获取正文的文本，返回的是一个列表

    with open(f"{car_name}.txt","w",encoding="utf-8") as f:
        for s in info:#info是列表，所以不能一下write
            f.write(s+"\n")
    
    image_url=article.find_all("img")[0].get("src") #正文中也只有一张图片，就是品牌标志

    image=requests.get("https:"+image_url,params=param)

    with open(f"{car_name}.jpg","wb") as f:#注意图片是二进制的，必须以wb方式打开，不能少了b
        f.write(image.content)


def get_country_car_list(full_url):#获取某一国的所有汽车品牌列表，用json保存
    res=requests.get(full_url,params=param)
    res.encoding = "GBK"
    soup=BeautifulSoup(res.text,"html.parser")

    car_list=soup.find_all("i",class_="iTit") #品牌名和链接在iTit块中
    
    car_dict={}
    for car in car_list:
        car_name=car.string
        car_url=car.a.get("href")
        car_dict[f"{car_name}"]="https:"+car_url#字典中添加一项

    with open(f"{country}.json",'w',encoding="utf-8") as f:
        json.dump(car_dict,f)

    for car_name,car_url in car_dict.items():
        get_car_info(car_name,car_url)#将字典中的每一项传递给子函数，用来获取该品牌的详细信息


if __name__=="__main__":
    for country in country_list:

        if not os.path.exists(country):
            os.mkdir(country)#按照国家建立子目录
        os.chdir(country)

        full_url=base_url+country
        get_country_car_list(full_url)

        os.chdir("..")

