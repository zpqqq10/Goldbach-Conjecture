import utils
import TopK
from nltk.stem import WordNetLemmatizer
from BooleanQuery import build_or

def handler(query):
    wordlist = utils.word_split(query)
    if len(wordlist) == 1:
        # only one word
        origin = wordlist[0]
        lemmatizer = WordNetLemmatizer()
        extendedlist = utils.load_wordlist(lemmatizer.lemmatize(origin))
        doclist = []    # to print
        if extendedlist or len(extendedlist) > 1:
            # many result
            for w in extendedlist:
                doclist = build_or(doclist, utils.load_doclist(w))
            doclist = TopK.TopK_sort(utils.load_doclist(origin))
        else:
            doclist = TopK.TopK_sort(utils.load_doclist(origin))
        # print(len(doclist))
        # return doclist
        utils.print_result(wordlist, doclist, 'Term Query')
    else: 
        # many words, calculate consine distance
        res = termquery(wordlist)
        utils.print_result(wordlist, res, 'Term Query')
        
# sort all the documents by consine distance
# return those with bigger than 45 degrees
def termquery(wordlist):
    wordvec = {}
    # earn query vector
    for origin in wordlist: 
        if origin in wordvec:
            wordvec[origin] += 1
        else:
            wordvec[origin] = 1
    vsm = utils.get_JSON('VSM')
    _doclist = {}
    for doc in vsm:
        # print(doc)
        val = utils.cos_dist(wordvec, vsm[doc])
        if val > 45: 
            _doclist[doc] = val
    doclist = sorted(_doclist.items(), key=lambda i:i[1], reverse=True)
    return doclist


if __name__ == '__main__':

    # print(len(utils.load_doclist('government')))
    # print(len(utils.load_doclist('governments')))
    print(handler('government').sort() == list(set(utils.load_doclist('government') + utils.load_doclist('governments'))).sort())