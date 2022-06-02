import os
import json
from nltk import word_tokenize

CANCEL = '\033[0m'
RED = '\033[1;31m'
GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[1;34m'
PURPLE = '\033[1;35m'
CYAN = '\033[1;36m'
WHITE = '\033[1;37m'
WHITE_ = '\033[0m'
CLEAR = '\033[1;1H\033[2J'

# TODO:
# - 修改文件
# - nltk 词干还原
# - 优化词表过滤规则

# 10788 documents and 32333 indexes in total!

# write data to a json
def write_to_json(data, file):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f) 

# 获取语料库的所有文件列表, 返回形式[1, 3, 9, ...]
def get_all_doc():
    filelist = []
    files = os.listdir('./Reuters/')
    for file in files:
        filelist.append(get_doc_ID(file))
    return sorted(filelist)

# 从文档名中截取文档 ID
def get_doc_ID(file):
    id = os.path.splitext(file)[0]
    return int(id)

# 处理语料库文档的内容
def process_doc_content(file):
    # 处理 ASCII 格式的语料
    with open(file, 'r', encoding='ISO-8859-1') as f:
        content = f.read()
    res = []
    result = []
    # 标点符号和数字
    punc_digit = [',', '.', ';', ':', '&', '>', "'", '"', '`', '+', '(', ')', '[', ']', '{', '}',
                  '*', '?', '!', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for word in word_tokenize(content):
        # 转换为小写
        word = word.lower()
        # 处理标点符号并忽略's
        for c in punc_digit:
            if word != "'s": 
                word = word.replace(c, '')
        # 处理空字符串
        if len(word) == 0 or word[0] == '-':
            continue
        # 处理 March/April 中的 / ：分成两个单词
        if word.find('/') > 0:
            res = word.split('/')
            for w in res:
                result.append(w)
            continue
        result.append(word)
    return result

# 读取一个json文件，输入的文件名不用带后缀
def get_JSON(filename):
    result = {}
    with open(os.path.join('jsons', filename+'.json'), 'r', encoding='utf-8') as f:
        result = json.load(f)
    return result

# ! 要用的话得修改一下
# # load the file.  Change it latter
# def loadLocationIndex(word):
#     f = open('index.json', encoding='utf-8')
#     dictionary = json.load(f)
#     index = dictionary[word]
#     return index


# load the file
def load_index(word):
    result = []
    with open(os.path.join('jsons', 'InvertedIndex.json'), 'r', encoding='utf-8') as f:
        dictionary = json.load(f)
        index = dictionary[word]
        for item in index:
            result.append(int(item))
    return result

# print filenames and the titles in terminal
# output the content to *output*
def print_result(wordlist, doclist, mode):
    output = open('output', 'w')
    print('################## {} Result ##################'.format(mode))
    for docID in doclist:
        title = ''
        body = ''
        # read title and body
        with open(os.path.join('Reuters', str(docID) + '.html'), 'r') as f:
            title = f.readline()
            body = f.read()
        # find title
        # find body
        print(BLUE+str(docID)+'.html: '+WHITE_+title, end='')
        output.write(title)
        output.write(body)
        output.write('----------------------------------------\n')
    output.close()

if __name__ == '__main__':
    print(get_JSON('VSM'))
