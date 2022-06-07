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

Work: 
- [x] 倒排索引
- [x] VSM
- [x] 索引压缩
- [x] 布尔查询
- [ ] 通配查询
- [x] 短语查询
- [x] 拼写矫正 （速度比较慢）
- [x] 词典索引 （因为python的字典就是哈希索引的，因此也可以说已经实现了基于hash的词典索引）
- [ ] 同义词
- [x] TopK （比较简单，暂未实现堆）

Environment: 
* **Linux**
* **Python**

Packages: 
* nltk?
* chardet?

TODO：
* zpq：在`utils.py`中增加一个`word_split()`函数，用来将Query分成词表
* zpq：尝试引入词性工具，增加_ - 's .的处理
* kyq：搞一下同义词
* zjc：用堆实现TopK，传入字典，传出列表（列表元素为`(docID, score)`），不清楚的话找我
* 所有人：在自己电脑上把`main.py`跑起来，如果nltk提示找不到包，百度一下解决这个问题，大概流程就是去网站上下载包，然后把包放到报错的目录下（nltk找不到包的报错是寻找了以下哪些哪些路径，没有找到包），我晚上找一找我看得链接放上来

# 大家都加快进度赶一赶！先做出能跑的东西再考虑优化效果！
