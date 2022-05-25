# !/usr/bin/env python

import os
from tqdm import tqdm
import wget
from utils import *
import rarfile
import InvertedIndex
# sudo apt install unrar

# 从 JSON 读取数据， JSON 文件默认放在 IRProject 下
# print('Getting Data from Files...')
# index = utils.get_from_file('index')
# wordlist = utils.get_from_file('wordlist')
# doc_size = utils.get_from_file('doc_size')
# VSM = utils.get_from_file('VSM')
# btree, btree_rev = GlobbingQuery.BuildTree(wordlist)

prompt = '''Please select the query mode:  
1.Boolean Query
2.Phrase Query
3.Wildcard Query
4.Fuzzy Query
0.quit
> '''
# main function, a loop


def main():
    while True:
        print("\n"+"*"*50)
        number = input(prompt)
        if int(number) == 0:
            break
        elif int(number) > 4 or int(number) < 0:
            print("ERROR: WRONG INPUT!")
            continue
        query = input("Input your query:\n> ")
        # boolean query
        if(int(number) == 1):
            # BooleanQuery.controller(query)
            print('boolean')
        # phrase query
        elif(int(number) == 2):
            # PhraseQuery.phrasequery(query)
            print('phrase')
        # wildcard query
        elif(int(number) == 3):
            # GlobbingQuery.controller(query, btree, btree_rev,wordlist)
            print('globbing')
        # Fuzzy Query
        elif(int(number) == 4):
            # SpellingCorrect.spelling_correct(query)
            print('correcting')

        # merge
        # if query.find('*')!=-1:
            #GlobbingQuery.controller(query, btree, btree_rev, wordlist)


if __name__ == "__main__":
    # check files
    if not os.path.exists('jsons'):
        # create a dir
        os.mkdir('jsons')
    if os.path.exists('jsons'):
        if os.path.isfile('jsons'):
            # create a dir
            raise Exception('Please make sure there is no file named jsons!')
        if not os.path.exists(os.path.join('jsons', 'InvertedIndex.json')) or \
           not os.path.exists(os.path.join('jsons', 'Dictionary.json')) or \
           not os.path.exists(os.path.join('jsons', 'VSM.json')):
            if not os.path.exists('Reuters'):
                if not os.path.exists('Reuters.rar'):
                    print('Downloading Reuters...')
                    wget.download('http://10.76.3.31/Reuters.rar', os.getcwd())
                    print('\n')
                print('Extracting Reuters...')
                z = rarfile.RarFile(os.path.join(os.getcwd(), 'Reuters.rar'))
                for f in tqdm(z.namelist()): 
                    z.extract(f)
                z.close()
                print(GREEN+'Extraction is successfully done!'+WHITE_)
            index, doc_sizes = InvertedIndex.build_Iindex()
            InvertedIndex.build_VSM(index, doc_sizes)

    main()
