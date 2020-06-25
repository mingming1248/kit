import requests
from bs4 import BeautifulSoup
import fake_useragent
import json
import os
import threading

#多线程方式，会被对方网站屏蔽

def root_page_parser(root,link,left_for_download):

        root_page=requests.get(link,headers={"User-Agent": fake_useragent.UserAgent().random})
        soup=BeautifulSoup(root_page.text,"html.parser")
        root_explains=soup.find_all("div",class_="wdef") 

        #页面最多有5个wdef，分别对应词根、词义、衍生词、近义词、例句，有的项目有缺失
        #衍生词、近义词格式不规范，就不提取了
        cegen_list=[]
        ciyi_list=[]
        liju_list=[]

        #第一个是做词根时的意思，不会缺失
        cegens=root_explains[0].find_all("ol") #做词根时可能有多个意思，每一个ol标签都包含一个

        for cegen in cegens:
            meaning=cegen.li.p.strong.get_text() #词根的意思
            examples=[] #词根的例子

            try:    #有的词根没有例子，直接跳过，except无需处理
                examples_tag=cegen.li.ul.find_all("li") #词根例子所在的tag
            
                for example_tag in examples_tag:
                    strings=example_tag.stripped_strings #获取所有的字符串，这是一个生成器
                    for s in strings:
                        examples.append(s) #将词根的例子添加到列表中
            except AttributeError:
                pass

            finally:
                cegen_list.append([meaning,examples]) #将词根的意思和对应的例子作为子列表放入cegens_list

        #第二个是做单词时的意思，有可能缺失
        if len(root_explains)>1:
            ciyis=root_explains[1].find_all("p") #做单词时可能有多个意思，每一个p标签都包含一个
            
            for ciyi in ciyis:
                strings=ciyi.stripped_strings
                for s in strings:
                    ciyi_list.append(s) #提取词义很简单，只需要将p标签中的文本拿出来即可

        #如果wdef有2个以上（不超过5个），最后一个是例句。有可能缺失
        if len(root_explains)>2:
            lijus=root_explains[-1].find_all("li") #例句有多个，每一个li标签都包含一个

            for liju in lijus:
                strings=liju.stripped_strings
                for s in strings:
                    liju_list.append(s) #提取例句很简单，只需要将li标签中的文本拿出来即可
        
 
        with open(f"{root}.json","w",encoding="utf8") as file:
            root_dict={}
            root_dict[root]=[cegen_list,ciyi_list,liju_list]
            json.dump(root_dict,file,ensure_ascii=False) #dump会用ascii保存

        mutex.acquire()
        left_for_download-=1
        print(f"{left_for_download}")
        mutex.release()


if __name__=="__main__":
    
    with open("root_dict.json","r") as file:
        root_dict=json.load(file)

    # root_dict={"bene":"http://www.cgdict.com/index.php?app=cigen&ac=word&w=bene",
    #             "amphi":"http://www.cgdict.com/index.php?app=cigen&ac=word&w=amphi",#没有例句
    #             "ad":"http://www.cgdict.com/index.php?app=cigen&ac=word&w=ad" #词根没有举例
    #             } #测试使用
    
    left_for_download=len(root_dict)

    #给多线程准备的
    mutex=threading.Lock()
    thread_list=[]

    if not os.path.exists("download"):
        os.mkdir("download")

    os.chdir("download")

    for root,link in root_dict.items():
        if os.path.exists(f"{root}.json"):#如果之前下载过就不下载了
            mutex.acquire()
            left_for_download-=1
            print(f"{left_for_download}")
            mutex.release()
            continue
        
        #之前没有的才加入多线程下载
        thread_list.append(threading.Thread(target=root_page_parser,args=(root,link,left_for_download)))
        
    for t in thread_list:
        t.start()

    for t in thread_list:
        t.join()
    
    print("over!")
        
 