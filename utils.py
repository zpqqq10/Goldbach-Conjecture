from math import sqrt
import os
import json
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer

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

# top K
TOPK = 10

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

def word_split(text):
    res = []
    result = []
    # 标点符号和数字
    punc_digit = [',', '_', '.', ';', ':', '&', '>', "'", '"', '`', '+', '(', ')', '[', ']', '{', '}',
                  '*', '?', '!', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    tokens = word_tokenize(text)
    tokens = [token.lower() for token in tokens]
    for word in tokens:
        if word == "'s":
            result[-1] += 's'
            continue
        # 处理标点符号
        for c in punc_digit:
            word = word.replace(c, '')
        # 处理空字符串
        if len(word) == 0:
            continue
        if word.find('/') < 0 and word.find('-') < 0:
            result.append(word)
        # 处理/ - ：分成两个单词
        else: 
            res = word.split('/')
            for w in res:
                r = w.split('-')
                for t in r:
                    if t != '': 
                        result.append(t)
        
    return result

# 处理语料库文档的内容
def process_doc_content(file):
    # 处理 ASCII 格式的语料
    with open(file, 'r', encoding='ISO-8859-1') as f:
        content = f.read()
    return word_split(content)

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
        index = dictionary.get(word, {})
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
        index = dictionary.get(word, {})
        for docID in index:
            result[int(docID)] = index[docID]
    return result

# load the compressed posting list of a word
# return the same thing as *load_index*, a list of docID with postion info
def load_cprs_doclist_withp(word):
    result = {}
    with open(os.path.join('jsons', 'CompressedInvertedIndex.json'), 'r', encoding='utf-8') as f:
        dictionary = json.load(f)
        arr = dictionary.get(word, {})
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
# doclist: [(docID, score), ...]
def print_result(wordlist, doclist, mode):
    output = open('output', 'w')
    show = 0
    # print(doclist)
    if type(doclist) is dict:
        doclist = doclist.items()
    print('################## {} Result ##################'.format(mode))
    print(BLUE+str(len(doclist))+WHITE_+' documents in total: ')
    for doc in doclist:
        docID = doc[0]
        score = doc[1]
        title = ''
        # body = ''
        # read title and body
        with open(os.path.join('Reuters', str(docID) + '.html'), 'r', encoding='ISO-8859-1') as f:
            title = f.readline()
            # body = f.read()
        # find title
        # find body
        if show < TOPK:
            print(BLUE+str(docID)+'.html: '+'\t'+ '%.6f'%score +WHITE_ + '\t'+title, end='')
        output.write(str(docID) + '.html: '+'\t'+ '%.6f'%score + '\t'+ title + '\n')
        # output.write(body)
        # output.write('----------------------------------------\n')
        show += 1
    output.close()

# pass two document vectors
# return the cosine distance
def cos_dist(vec1, vec2): 
    terms1 = list(vec1.keys())
    terms2 = list(vec2.keys())
    if len(terms1) == 0 or len(terms2) == 0: 
        return 0
    v1 = {}
    v2 = {}
    # if is a list
    if type(vec1[terms1[0]]) is list:
        # use tf*idf
        for term in terms1: 
            v1[term] = vec1[term][2]
    else: 
        v1 = vec1
    if type(vec2[terms2[0]]) is list:
        # use tf*idf
        for term in terms2: 
            v2[term] = vec2[term][2]
    else: 
        v2 = vec2
    # normalization
    n = 0
    for term in v1: 
        n += v1[term] **2
    if n > 1:
        n = sqrt(n)
        for term in v1:
            v1[term] /= n
    n = 0
    for term in v2: 
        n += v2[term] **2
    if n > 1:
        n = sqrt(n)
        for term in v2:
            v2[term] /= n
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
    # result
    return qd / (q_2 * d_2)

# load wordlist of a stem
# return a list of word
def load_wordlist(stem):
    result = []
    with open(os.path.join('jsons', 'Stem2Word.json'), 'r', encoding='utf-8') as f:
        stems = json.load(f)
        result = stems.get(stem, [])
    return result

def get_stem(word): 
    lemmatizer = WordNetLemmatizer()
    s = ''
    if word[-3:] == 'ing' or word[-2:] == 'ed':
            # continuous tense or past tense
        s = lemmatizer.lemmatize(word, 'v')
    else:
        s = lemmatizer.lemmatize(word)
    return s

# return all possible word lists
def get_all_lists(wordlist):
    extended = []
    for i in range(len(wordlist)): 
        s = get_stem(wordlist[i])
        l = load_wordlist(s)
        if l != []: 
            extended.append(l)
    mat = recurse([], extended, 0, len(extended))
    # print(mat)
    return mat

def recurse(mat, extended, level, depth): 
    if depth == 1:
        for w in extended[level]: 
            mat.append([w])
    elif level == depth - 1: 
        l = mat.pop()
        for w in extended[level]: 
            mat.append(l + [w])
    elif level == 0:
        for w in extended[level]:
            mat.append([w])
            mat = recurse(mat, extended, level + 1, depth)
    else: 
        l = mat.pop()
        for w in extended[level]: 
            mat.append(l + [w])
            mat = recurse(mat, extended, level + 1, depth)
    return mat
        

if __name__ == '__main__':

    # print(load_cprs_doclist('bahia') == load_doclist('bahia'))
    # print(load_doclist_withp('bahia') == load_cprs_doclist_withp('bahia'))
    # print(load_docsum(5))
    # print(cos_dist(load_docvec(22), load_docvec(21521)))
    
    # token = word_split("26-FEB-1987 doctors government'S dlrs tonne aug playing dentist's U.S.")
    # cnt = 0
    # ind = 0
    # print(token)
    # for t in token:
    #     if t == "'s":
    #         token[token.index("'s")-1] += 's'
    #         token.remove("'s")
    #     # ind += 1
    # # for i in range(cnt):
    # #     token.remove("'s")
    # print(token)
    # lem = []
    # lemmatizer = WordNetLemmatizer()
    # for t in token:
    #     if t[-3:] == 'ing':
    #         lem.append(lemmatizer.lemmatize(t, 'v'))
    #     else:
    #         lem.append(lemmatizer.lemmatize(t))
    # # token = [lemmatizer.lemmatize(t) for t in token]
    # print(lem)
    
    # process_doc_content('Reuters/20208.html')
    print(get_all_lists(['technology', 'vying', 'education']))
