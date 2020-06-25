# Anki词根词缀卡牌

## 感谢`cgdict.com`提供的词根词缀列表
`http://www.cgdict.com/index.php?app=cigen&ac=list`

## 流程
- 首先用request和beautifulsoup获取711个词根词缀所在的页面，将其保存为json文件
- 接着用request和beautifulsoup获取每个词根词缀所在页的内容，包括词根意思、单词意思、例句，每一个都保存为json文件
- 然后读取每一个json文件，将其写入txt中，用`\t`做分割，便于anki识别
- 最后导入Anki中。预设了4个字段，分别为词根、词根意思、单词意思、例句

## 注意
有两个词根mus和pos的例句太多了，我做了删减

可以直接下载apkg包，也可以下载txt文件自己导入