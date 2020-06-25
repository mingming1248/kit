import requests
from bs4 import BeautifulSoup
import fake_useragent
import json

def get_root_dict():
    root_dict={}
    base_url="http://www.cgdict.com/index.php?app=cigen&ac=list&page="

    for i in range(8): #一共有8页，711个词根词缀
        page_url=f"{base_url}{i+1}"
        page_item=requests.get(page_url,headers={"User-Agent": fake_useragent.UserAgent().chrome})
        soup=BeautifulSoup(page_item.text,"html.parser")
        dict_root_div=soup.find("h2") #当前页面的几个词根都保存在h2标签中，页面内只有一个h2
        dict_roots=dict_root_div.contents #下行遍历所有子节点

        for item in dict_roots:
            if item!="\n": #子节点中包含换行，应该跳过
                root_dict[item.string]=item.get("href") #把词根当作字典的key，对应的hrer属性里的链接当作value
        
    print(len(root_dict)) #711个词根词缀
    
    with open("root_dict.json","w") as file: #保存起来
        json.dump(root_dict,file)


if "__main__"==__name__:
    get_root_dict()

