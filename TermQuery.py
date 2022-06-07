import utils
import TopK

def handler(query):
    wordlist = utils.word_split(query)
    if len(wordlist) == 1:
        # only one word
        doclist = TopK.TopK_sort(utils.load_doclist(wordlist[0]))
        utils.print_result(wordlist, doclist, 'Term Query')
    else: 
        # many words, calculate consine distance
        wordvec = {}
        # earn query vector
        for word in wordlist: 
            if word in wordvec:
                wordvec[word] += 1
            else:
                wordvec[word] = 1
        vsm = utils.get_JSON('VSM')
        _doclist = {}
        for doc in vsm:
            # print(doc)
            _doclist[doc] = utils.cos_dist(wordvec, vsm[doc])
        doclist = sorted(_doclist.items(), key=lambda i:i[1], reverse=True)
        res = []
        # pass those not similar
        for d in doclist:
            if d[1] > 40:
                res.append(d)
            else: 
                break
        utils.print_result(wordlist, res, 'Term Query')