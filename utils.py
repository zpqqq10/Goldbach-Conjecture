import os
import json
from unittest import result
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
def get_all_docID():
    filelist = []
    files = os.listdir('Reuters/')
    for file in files:
        filelist.append(get_doc_ID(file))
    return sorted(filelist)

# 从文档名中截取文档 ID

def get_doc_ID(file):
    return int(file[:-5])

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

# load the inverted index
# return a list of docID
def load_doclist(word):
    result = []
    with open(os.path.join('jsons', 'InvertedIndex.json'), 'r', encoding='utf-8') as f:
        dictionary = json.load(f)
        index = dictionary[word]
        for docID in index.keys():
            result.append(int(docID))
    return result

# load the compressed posting list of a word
# return the same thing as *load_index*, a list of docID
def load_cprs_doclist(word):
    result = []
    with open(os.path.join('jsons', 'CompressedInvertedIndex.json'), 'r', encoding='utf-8') as f:
        dictionary = json.load(f)
        arr = dictionary[word]
        id = 0
        for item in arr:
            if type(item) is int:
                # sum up delta
                id += item
                result.append(id)
    return result

# load the inverted index with postions
# return a list of docID with postion info
def load_doclist_withp(word):
    result = {}
    with open(os.path.join('jsons', 'InvertedIndex.json'), 'r', encoding='utf-8') as f:
        dictionary = json.load(f)
        index = dictionary[word]
        for docID in index:
            result[int(docID)] = index[docID]
    return result

# load the compressed posting list of a word
# return the same thing as *load_index*, a list of docID with postion info
def load_cprs_doclist_withp(word):
    result = {}
    with open(os.path.join('jsons', 'CompressedInvertedIndex.json'), 'r', encoding='utf-8') as f:
        dictionary = json.load(f)
        arr = dictionary[word]
        id = 0
        for item in arr:
            if type(item) is int:
                # sum up delta
                id += item
            else :
                result[id] = item
    return result

# load a document vector
# return {} if the document ID is invalid
def load_docvec(docID): 
    result = {}
    with open(os.path.join('jsons', 'VSM.json'), 'r', encoding='utf-8') as f:
        vsm = json.load(f)
        if str(docID) in vsm.keys(): 
            result = vsm[str(docID)]
        else :
            result = {}
    return result

# load a document sum of (tf, idf, tf*idf) (tf is always nearly 1)
# return [] if the document ID is invalid
def load_docsum(docID): 
    result = []
    with open(os.path.join('jsons', 'VSMSum.json'), 'r', encoding='utf-8') as f:
        vsm = json.load(f)
        if str(docID) in vsm.keys(): 
            result = vsm[str(docID)]
        else :
            result = []
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

# pass two document vectors
# return the cosine distance
def cos_dist(vec1, vec2): 
    terms1 = list(vec1.keys())
    terms2 = list(vec2.keys())
    v1 = {}
    v2 = {}
    # if is a list
    if type(vec1[terms1[0]]) is list:
        # use tf*idf
        for term in terms1: 
            v1[term] = vec1[term][2]
        for term in terms2: 
            v2[term] = vec2[term][2]
    else: 
        v1 = vec1
        v2 = vec2
    v = dict(v1, **v2)
    # calculate
    qd = 0      # sum of qd
    q_2 = 0     # sum of q^2
    d_2 = 0     # sum of d^2
    for term in v.keys():
        l = []
        if term in terms1: 
            l.append(v1[term])
        else: 
            l.append(0)
        if term in terms2: 
            l.append(v2[term])
        else: 
            l.append(0)
        v[term] = l
    # cosine
    for term in v.keys(): 
        qd += sum(v[term])
        q_2 += v[term][0] ** 2
        d_2 += v[term][1] ** 2
    
    return qd / (q_2 * d_2)

if __name__ == '__main__':

    # print(load_cprs_doclist('bahia') == load_doclist('bahia'))
    # print(load_doclist_withp('bahia') == load_cprs_doclist_withp('bahia'))
    # print(load_docsum(5))
    print(cos_dist(load_docvec(22), load_docvec(21521)))
