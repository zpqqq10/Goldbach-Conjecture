from InvertedIndex import build_Iindex
import utils
import nltk
def handler(query):
    word_list = word_split(query)
    result = phrasequery(query)
    utils.print_result(word_list, result, 'Phrase Query')

# 'of': {1: [60, 69, 144, 157, 178, 191, 209, 274], 6: [12, 22]}
def getinverted_index():
    inv,_ = build_Iindex()
    return inv

def word_split(text):
    res = []
    result = []
    # 标点符号和数字
    punc_digit = [',', '.', ';', ':', '&', '>', "'", '"', '`', '+', '(', ')', '[', ']', '{', '}',
                  '*', '?', '!', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for word in nltk.word_tokenize(text):
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

def phrasequery(query):
    inverted = getinverted_index()
    words = [word for word in word_split(query) if word in list(inverted.keys())]

    # print(words)

    tempDic = {}
    doc_return = []

    for word in words:
        word_doc_ids=inverted[word].keys()
        tempDic.setdefault(word,{})
        for ID in word_doc_ids:
            word_doc_position =  inverted[word][ID]
            tempDic[word].setdefault(ID,word_doc_position)

    # print(tempDic)

    if len(words)>1:
        minKey = {}
        for i in range(0,len(words)):
            tempKeys = tempDic[words[i]].keys()
            minKey.setdefault(i,tempKeys)
        minKeyNew = minKey[0]
        for i in range(1,len(words)):
            minKeyNew = [val for val in minKeyNew if val in minKey[i]]
        for key in minKeyNew:
            list1 = tempDic[words[0]][key]
            isAdd = []
            for position in list1:
                isAddForEach = []
                for j in range(1,len(words)):
                    if position+j not in tempDic[words[j]][key]:
                        isAddForEach.append(0)
                    else:
                        isAddForEach.append(1)
                if 0 in isAddForEach:
                    isAdd.append(0)
                else:
                    isAdd.append(1)
            if 1 in isAdd:
                doc_return.append(key)
    elif len(words)==1:
        doc_return = list(tempDic[words[0]].keys())
    results = []
    for doc_id in doc_return:
        if doc_id not in results:
            results.append(doc_id)
    return results