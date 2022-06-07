import nltk
import utils
def handler(query,k=10):
    # query-> vector
    wordlist = word_split(query)
    # if len(wordlist) == 1:
    #     # only one word
    #     doclist = TopK.TopK_sort(utils.load_doclist(wordlist[0]))
    #     utils.print_result(wordlist, doclist, 'Term Query')
    # else:
    wordvec = {}
        # earn query vector
    for word in wordlist: 
        if word in wordvec:
            wordvec[word] += 1
        else:
            wordvec[word] = 1
    vsm = utils.get_JSON('VSM')
    inputdata = []
    for doc in vsm:
        inputdata.append((utils.cos_dist(wordvec, vsm[doc]),doc))
    
    result = TopK(inputdata,k)

    score = []
    docid = []
    for i in range(k):
        score_,docid_ = result[i]
        score.append(score_)
        docid.append(docid_)
    print(docid)
    print(score)
    # utils.print_result(wordlist, docid, 'Top K Query')


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


def TopK(query_cos_score,k):
    minheap = Heap(query_cos_score[0:k],k)
    minheap.Build_min_heap()
    for i in range(k,len(query_cos_score)):
        score_insert,_ = query_cos_score[i]
        score_heaptop,_ = minheap.top()
        if score_insert > score_heaptop:
            minheap.replace(query_cos_score[i])
    return minheap.Allnodes()

class Heap():
    # data: list of first K data
    def __init__(self,data=[],k=1) -> None:
        self.K = k
        # data (score,doc id)
        self.heap = data

    # let this heap a minheap with root n
    def siftdown(self,i):
        n = self.K
        t = 0
        while i*2+1<n:
            i_value,_ = self.heap[i]
            left_value,_ = self.heap[2*i+1]
            if i_value > left_value:
                t = i*2+1
            else: t = i
            t_value,_ = self.heap[t]

            if i*2+2<n:
                right_value,_ = self.heap[i*2+2]
                if t_value > right_value: 
                    t = i*2+2

            if t != i:
                self.heap[t],self.heap[i] = self.heap[i],self.heap[t]
                i = t  
            else:
                break

    def Build_min_heap(self):
        for i in range(int((self.K-2)/2),-1,-1):
            self.siftdown(i)

    def top(self):
        return self.heap[0]

    def Allnodes(self):
        return self.heap

    def replace(self,value):
        self.heap[0] = value
        self.Build_min_heap()


