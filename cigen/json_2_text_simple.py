import os
import json

#只获取单词意思、词根意思，每个词根不超过3个案例

def to_txt():
    os.chdir("download")
    file_list=os.listdir()
    #file_list=["arm.json","dia.json","firm.json"] #测试使用
    num=len(file_list)

    with open(f"../anki.txt","w",encoding="utf8") as f:
        for js in file_list: #遍历所有文件
            print(num,js)

            with open(js,"r",encoding="utf8") as js_file:
                str="" #初始化str，str中不能出现\n，全部用html的<br />代替

                root_dict=json.load(js_file)
                root=list(root_dict.keys())[0] #每一个文件的key，只有一个
                value=list(root_dict.values())[0] #每一个文件的value，只有一个
                
                str=str+root #第一个字段，对应anki的正面
                
                #词根部分
                str=str+"\t做词根时的意思：<br />" #\t开始是第二个字段，对应anki反面第一部分
                for cigen in value[0]: #做词根时可能有多个意思，每一个都是value[0]的元素

                    # value[0]的每个元素又包含两个子元素，第一个是词根本意，第二个是词根例子
                    cigen_meaning=cigen[0] #取词根本意
                    str=str+cigen_meaning+"<br />eg："

                    if len(cigen[1])>6: #每个词根的例子只取3个以内，两个元素是一个例子
                        lizis=cigen[1][0:6]
                    else:
                        lizis=cigen[1]
                    
                    for lizi in lizis:
                        str=str+"<br />"+lizi.replace("\n"," ") #例句里面可能有换行符，用空格替换


                #词义部分   
                str=str+"\t"+"***"*5+"<br />做单词时的意思：" #\t开始是第四个字段，对应anki反面第二部分
                for ciyi in value[1]: #做单词时可能有多个意思，每一个都是value[1]的元素
                    str=str+"<br />"+ciyi.replace("\n"," ")

                str=str+"\n" #所有内容都提取到一行了，再添加\n表示结束
                f.write(str)
                num-=1

    
if __name__=="__main__":
    to_txt() 