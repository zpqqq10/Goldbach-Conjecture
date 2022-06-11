import utils
import nltk
import TopK
from BooleanQuery import build_or

def handler(query):
    word_list = utils.word_split(query)
    mat = utils.get_all_lists(word_list)
    result = []
    for wl in mat:
        res = phrasequery(wl)
        res = [int(r) for r in res]
        result = build_or(result, res)
    # proecess result
    # result = [int(res) for res in result]
    result = TopK.TopK_sort(result)
    utils.print_result(word_list, result, 'Phrase Query')

# 'of': {1: [60, 69, 144, 157, 178, 191, 209, 274], 6: [12, 22]}
def getinverted_index():
    inv = utils.get_JSON('InvertedIndex')
    return inv

def phrasequery(word_list):
    inverted = getinverted_index()
    words = [word for word in word_list if word in list(inverted.keys())]

    # print(words)

    tempDic = {}
    doc_return = []

    for word in words:
        word_doc_ids=inverted[word].keys()
        tempDic.setdefault(word,{})
        for _id in word_doc_ids:
            word_doc_position =  inverted[word][_id]
            tempDic[word].setdefault(_id,word_doc_position)

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
    