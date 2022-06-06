import os
from utils import *
import math
from tqdm import tqdm

# 保留多少位小数
RESERVEDBITS = 6
# 文档的数量
DOCS = 10788

# TODO: _ - .
def build_Iindex():
    # build inverted index
    index = {}      # inverted index list
    compressed_index = {}   # compressed
    doc_sizes = {}   # size of each documents
    # process each document
    docs = os.listdir('Reuters')
    # sort the filename
    docs.sort(key=lambda x: int(x[:-5]))
    
    print('Building inverted index...')
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
    
    # index compressed
    print('Compressing inverted index...')
    for word in tqdm(index.keys()):
        last = 0
        compressed_index[word] = []
        for docID in index[word].keys(): 
            delta = docID - last
            compressed_index[word].append(delta)
            compressed_index[word].append(index[word][docID])
            last = docID
    write_to_json(compressed_index, os.path.join('jsons', 'CompressedInvertedIndex.json'))
    print(GREEN+'Inverted index is successfully compressed and saved!'+WHITE_)
    
    print(GREEN+str(DOCS)+WHITE_+' documents and '+GREEN+str(len(index.keys()))+WHITE_+' indexes in total!')
    return index, doc_sizes


def build_VSM(index, doc_sizes):
    # build VSM
    # index: inverted index posting list (positional)
    # doc_sizes: size of each document
    print('Building VSM...')
    dictionary = [word for word in index.keys()]
    VSM = {}
    for docID in tqdm(doc_sizes.keys()):
        vector = {}
        # delta = 0
        for word in dictionary:
            if docID in index[word]:   # the docID is in the docIDlist of this index
                tf = float(len(index[word][docID]) / doc_sizes[docID])   # wordCount / documentLength
                tf = round(tf, RESERVEDBITS)
                idf = math.log2(DOCS / len(index[word]))                 # log2( DOCS / docCount )
                idf = round(idf, RESERVEDBITS)
                tf_idf = round(float(tf*idf), RESERVEDBITS)
                vector[word] = (tf, idf, tf_idf)
        VSM[docID] = vector
    write_to_json(dictionary, os.path.join('jsons', 'Dictionary.json'))
    print(GREEN+'Dictionary is successfully built and saved!'+WHITE_)
    write_to_json(VSM, os.path.join('jsons', 'VSM.json'))
    print(GREEN+'VSM is successfully built and saved!'+WHITE_)
    return VSM

# sum up the stat of a document, prepare for TopK
def sumup_VSM(VSM):
    sums = {}
    print('Summing up VSM...')
    for docID in tqdm(VSM.keys()):
        sum = [0, 0, 0]
        for word in VSM[docID].keys():
            vec = VSM[docID][word]
            sum[0] += vec[0]    # tf sum of a document
            sum[1] += vec[1]    # idf sum of a document
            sum[2] += vec[2]    # tf*idf sum of a document
        sum[0] = round(sum[0], RESERVEDBITS)
        sum[1] = round(sum[1], RESERVEDBITS)
        sum[2] = round(sum[2], RESERVEDBITS)
        sums[docID] = sum
    write_to_json(sums, os.path.join('jsons', 'VSMSum.json'))
    print(GREEN+'VSM is successfully summed up and saved!'+WHITE_)

    return sums


if __name__ == '__main__':
    index, doc_sizes = build_Iindex()
    build_VSM(index, doc_sizes)
