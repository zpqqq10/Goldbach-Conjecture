import utils

def TopK_sort(doclist):
    _doclist = {}
    for docID in doclist:
        _doclist[docID] = utils.load_docsum(docID)[2]
    return sorted(_doclist.items(),key=lambda i:i[1], reverse=True)