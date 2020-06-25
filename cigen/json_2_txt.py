import os
import json

def to_txt(start,end,file_list):
    with open(f"../anki_{start}_{end}.txt","w",encoding="utf8") as f:
        num=end-start

        for js in file_list[start:end]: #遍历所有文件
            print(num,js)

            with open(js,"r",encoding="utf8") as js_file:
                str=""
                num-=1

                root_dict=json.load(js_file)
                root=list(root_dict.keys())[0] #每一个文件的key，只有一个
                value=list(root_dict.values())[0] #每一个文件的value，只有一个

                #词根部分
                str=str+root

                for cigen in value[0]:
                    cigen_meaning=cigen[0]

                    str=str+"\t"+cigen_meaning

                    for liju in cigen[1]:#<br />是anki识别的换行符，html标签
                        str=str+"<br />"+liju.replace("\n","") #例句里面可能有换行符，用空格替换

                #词义部分   
                str=str+"\t"+"***"*5
                
                for ciyi in value[1]:
                    str=str+"<br />"+ciyi.replace("\n","")
                
                #例句部分
                str=str+"\t"+"***"*5

                for liju in value[2]:
                    str=str+"<br />"+liju.replace("\n","")

                str=str+"\n" #每一个词根作为一行，用\n分割
                f.write(str)
                #print(str)


def json_2_txt():
    os.chdir("download")
    file_list=os.listdir()

    #file_list=["arm.json"] #测试使用

    total=len(file_list)

    for i in range(7):#分成多个文件，避免单个文件过大
        to_txt(i*100,(i+1)*100,file_list) 
    to_txt(700,total,file_list) 
    
    os.chdir("../")


if __name__=="__main__":
    json_2_txt()