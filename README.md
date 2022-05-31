# Goldbach-Conjecture
## IR project

Group members & works: 
* zpq
  *  程序入口
  *  倒排索引+VSM
* kyq
  * 布尔查询
* wzq
  * 通配查询
* zjc
  * 短语查询
* 完成一个模块之后可以领新的锅并更新一下这个Readme

Environment: 
* **Linux**
* **Python**

Packages: 
* nltk?
* chardet?

**下周再开一次小会看看大家进度，大家加油**

**倒排索引和VSM已经好了，如果后续需要根据大家的方便修改保存的格式可以找我协商修改**

**Linux下使用rarfile需要使用sudo apt install unrar**

**为了方便pull和push，我设置忽略掉了一些内容(见.gitignore)**

**为了方便调试，大家可以手动保留Reuters中的1-45共25个文档，并修改InvertedIndex.py中的DOCS为25**



2022.5.31. kyq

布尔检索好了x

目前没发现问题x

可以使用 AND/OR/NOT/AND NOT/OR NOT/括号

AND/OR/AND NOT/ OR NOT不能出现在句首，NOT可以

以上都不能出现在句尾

单词和单词不能连续出现x
