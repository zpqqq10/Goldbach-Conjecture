import utils
from nltk.corpus import wordnet
from BooleanQuery import build_or
import TopK
def handler(query):
    syn = get_sys_list(query)
    res = Sys_query(syn)
    
    res = [int(r) for r in res]
    result = []
    result = build_or(result, res)
    result = TopK.TopK_sort(result)

    print("Words you may want to use:") 
    print(syn)

    utils.print_result(syn,result,"Synonym Query")

# 获取同义词的函数
def get_sys_list(word):
    inverted = utils.get_JSON('InvertedIndex')
    synonym = [word]
    # 在wordnet里查询word的同义词
    wordnet_set = wordnet.synsets(word)
    # 数据格式类似于 [Synset('hello.n.01')]
    for syn in wordnet_set:
        # 使用 syn.lemmas 查看同义词
        for w in syn.lemmas():
            if w.name() in list(inverted.keys()) and w.name() != word:
                synonym.append(w.name())
    return synonym

def Sys_query(syn_list):
    result = []
    dict_syn_doc = {}
    inverted = utils.get_JSON('InvertedIndex')
    for word in syn_list:
        # dict_syn_doc.setdefault(word,[])
        for doc in inverted[word].keys():
            # dict_syn_doc[word].append(doc)
            if doc not in result:
                result.append(doc)
    return result