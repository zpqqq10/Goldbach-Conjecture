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
  *  词条查询
* kyq
  * 布尔查询
  * 拼写矫正
* wzq
  * 通配查询
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
- [x] 拼写矫正
- [x] 词典索引
- [ ] 同义词
- [x] TopK
- [x] 词条查询 （基于余弦相似度）

Environment: 
* **Linux**
* **Python**

Packages: 
* nltk?
* chardet?

TODO：
* kyq：
  * 改进纠正（选做）
  * 改进布尔检索（选做）
* zjc：
  * 使用nltk的wordnet实现同义词查询
* wzq：
  * 继续完善通配查询
  * 根据提交要求，写说明文档，完成后发给zpq
* 所有人：
  * 在自己实现的查询中加入词干扩展的功能，首先对查询词进行lemmatize，再查Stem2Word.json得到候选词，对候选词的组合进行多次查询，对查询结果进行`build_or`（可以参考TermQuery.py的8-23行，选做，不懂的问zpq）
* 在自己电脑上把`main.py`跑起来，如果nltk提示找不到包，百度一下解决这个问题，大概流程就是去网站上下载包，然后把包放到报错的目录下（nltk找不到包的报错是寻找了以下哪些哪些路径，没有找到包），我晚上找一找我看得链接放上来
  * 从 http://www.nltk.org/nltk_data/ 下载缺少的包，把解压后的文件夹放到`~/nltk_data`（这个目录可能得手动新建，注意报错中黄色字的路径）
  * 现在需要安装的有：
    * `tokenizers/pubkt`
    * `corpora/omw-1.4`
    * `corpora/wordnet`

# 咱们尽量在考试周之前解决这个大作业！辛苦大家！
# SUMMARY
* 运行
  * 确认所有包安装完毕后直接运行main即可
  * 首次运行，程序会自动下载语料库并解压，计算生成各种json文件
* 倒排索引 + VSM
  * 首次运行时计算生成，并将结果保存为文件
  * 以-和/分割单词
  * 将所有token存为小写
  * 去除特殊符号和数字
  * 去除`'s`，并在其前一个单词后附加`s`
    * 如`Australia's`会经过nltk变成`['Australia', "'s"]`，程序再处理为`australias`
  * `CompressedInvertedIndex.json`：docID压缩后的倒排位置索引
  * `Dictionary.json`：词典
  * `InvertedIndex.json`：倒排位置索引
  * `Stem2Word.json`：词干及其在语料库中的衍生词
  * `VSM.json`：文档向量空间
  * `VSMSum.json`：每篇文档的tf，idf和以及tf*idf和（胜者表）
* 索引压缩
  * 实现了对docID的压缩
  * 考虑到语料库能提取的词较少，没有实现词典压缩
  * 变长编码：？
* 布尔查询
  * 支持与（AND）或（OR）非（NOT）
  * 同时支持与非（AND NOT）及或非（OR NOT）
  * 实现了docID列表的与或非合并
* 通配查询
  * **在做**
* 短语查询
  * 实现基于位置索引的短语查询
* 拼写矫正
  * 实现基于Levenshtein距离的拼写矫正
  * 当存在多个可能的正确单词时，选择出现频率最高者
* 词典索引
  * 实现了基于哈希的词典索引
* 同义词扩展
  * **在做**
* TopK
  * 实现基于堆和胜者表的TopK排序
  * 默认对查询进行TopK排序
  * 默认打印十个结果，全部结果放在output文件中
* 词条查询
  * 实现基于余弦相似度排序的词条查询
  * 只有一个词时，会返回词干能衍生出的所有词的结果
    * 暂未在别的查询下实现，对性能影响大
  * 多个词时，计算余弦相似度
