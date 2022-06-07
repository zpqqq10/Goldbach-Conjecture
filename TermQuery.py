import utils
import TopK

def handler(query):
    wordlist = query.split(' ')
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
        utils.print_result(wordlist, doclist, 'Term Query')