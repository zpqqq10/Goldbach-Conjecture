# Goldbach-Conjecture
## IR project

## 注意：统一一点规范
* 多写点注释
* python文件名采用每个词首字母大写，无下划线的形式
* 函数名用下划线_分割单词
* 每个模块的最顶级函数取名为`handler()`，可以直接在`main.py`中调用`xxx.handler(query)`（参考目前完成的布尔检索模块）
* 如果还没下载语料库的，直接跑`main.py`即可自动下载解压（在校网下），途中可能会提示一些包没安装，根据报错安装一下（其中*rarfile*用`sudo apt install unrar`，别的用pip）
* 建议字符串用单引号括
* `utils.py`里面有一些编写模块时需要用到的函数，名字与往年其他人作业的可能不同


Group members & works: 
* zpq
  *  程序入口
  *  倒排索引+VSM
  *  索引压缩
* kyq
  * 布尔查询
  * 拼写矫正
* wzq
  * 通配查询
  * 词典索引（基于B-树）
* zjc
  * 短语查询
  * 同义词
  * TopK
* 尽量根据模块的关联度和工作量分配了所有的锅

Environment: 
* **Linux**
* **Python**

Packages: 
* nltk?
* chardet?


### zpq

倒排索引和VSM已经好了，如果后续需要根据大家的方便修改保存的格式可以找我协商修改

Linux下使用rarfile需要使用sudo apt install unrar

为了方便pull和push，我设置忽略掉了一些内容(见.gitignore)

为了方便调试，大家可以手动保留Reuters中的1-45共25个文档，并修改InvertedIndex.py中的DOCS为25

**任务全部分配好了，大家赶紧加油干吧**



### 2022.5.31. kyq

布尔检索好了x

目前没发现问题x

可以使用 AND/OR/NOT/AND NOT/OR NOT/括号

AND/OR/AND NOT/ OR NOT不能出现在句首，NOT可以

以上都不能出现在句尾

单词和单词不能连续出现x

2022.6.6 kyq

非常简单的拼写矫正 T T

改了utils.py里的 `load_cprs_doclist_withp`，`load_doclist_withp`，`load_doclist` 里的`dictionary.get(word, {})`部分，get不到内容时要返回空的{}

最近各种麻烦事缠身，这两天尽量再换个快的做法 TOT
