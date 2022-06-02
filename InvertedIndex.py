import os
from utils import *
import math
from tqdm import tqdm

DOCS = 10788
# DOCS = 25
# IDRANGE = 21576
# IDRANGE = 45


def build_Iindex():
    # build inverted index
    print('Building inverted index...')
    index = {}      # inverted index list
    doc_sizes = {}   # size of each documents
    # process each document
    docs = os.listdir('Reuters')
    for file in tqdm(docs):  
        content = process_doc_content(os.path.join('Reuters', file))
        docID = get_doc_ID(file)
        # print(docID)
        position = 0    # 一个word在文档中的位置
        for word in content:
            if word in index:
                # the word has been added
                if docID in index[word]:
                    # the document has been added
                    index[word][docID].append(position)
                else:
                    index[word][docID] = [position]
            else:
                # a new word
                docIDlist = {}
                docIDlist[docID] = [position]
                index[word] = docIDlist
            position += 1
        doc_sizes[docID] = position
    write_to_json(index, os.path.join('jsons', 'InvertedIndex.json'))
    print(GREEN+'Inverted index is successfully built and saved!'+WHITE_)
    print(GREEN+str(DOCS)+WHITE_+' documents and '+GREEN+str(len(index.keys()))+WHITE_+' indexes in total!')
    return index, doc_sizes


def build_VSM(index, doc_sizes):
    # build VSM
    print('Building VSM...')
    dictionary = [word for word in index.keys()]
    VSM = {}
    for docID in tqdm(doc_sizes.keys()):
        vector = {}
        # delta = 0
        for word in dictionary:
            if docID in index[word]:   # the docID is in the docIDlist of this index
                # if delta > 0:
                #     tf_idf_list.append(str(delta))
                tf = float(len(index[word][docID]) / doc_sizes[docID])   # wordCount / documentLength
                idf = math.log2(DOCS / len(index[word]))                 # log2( DOCS / docCount )
                tf_idf = round(float(tf*idf), 4)
                vector[word] = tf_idf
                # delta = 0
            # else:
            #     delta += 1
            #     continue
        VSM[docID] = vector
    write_to_json(dictionary, os.path.join('jsons', 'Dictionary.json'))
    print(GREEN+'Dictionary is successfully built and saved!'+WHITE_)
    write_to_json(VSM, os.path.join('jsons', 'VSM.json'))
    print(GREEN+'VSM is successfully built and saved!'+WHITE_)
    return VSM

# 为 Top K 暴力查表做准备
# def VSM_sum(VSM):
#     sum_VSM = {}
#     for d in range(0, IDRANGE+1):  # 21576
#         if str(d) in VSM.keys():
#             sum = 0.0
#             for tfidf in VSM[str(d)]:
#                 if float(tfidf) < 1:
#                     sum += float(tfidf)
#             sum_VSM[d] = '%.3f' % sum

#     return sum_VSM


if __name__ == '__main__':
    index, doc_sizes = build_Iindex()
    build_VSM(index, doc_sizes)
