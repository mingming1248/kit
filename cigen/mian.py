from root_dict_download import get_root_dict
from root_page_parser import root_page_parser
from json_2_txt import json_2_txt
import os
import shutil

if __name__ == "__main__":
    get_root_dict() #首先获取所有词根和链接，放入字典中，保存为json文件
    root_page_parser() #打开每一个词根的页面，获取词根、词义、例句，每个词根保存成一个json文件
    json_2_txt() #读取所有的json文件，转换成anki可以识别的格式

    if not os.path.exists("txt"):
        os.mkdir("txt")

    for f in os.listdir(): #将所有txt文件移动到txt目录中
        if ".txt" in f:
            shutil.move(f,f"./txt/{f}")

    