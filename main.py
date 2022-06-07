# !/usr/bin/env python

import os
from tqdm import tqdm
import wget
from utils import *
import rarfile
import InvertedIndex
import BooleanQuery
import SpellCorrection
# sudo apt install unrar


prompt = '''Please select the query mode:  
    {}1{}.Boolean Query
    {}2{}.Phrase Query
    {}3{}.Wildcard Query
    {}4{}.Spell Correction
    {}0{}.quit
> '''.format(BLUE, WHITE_, BLUE, WHITE_, BLUE, WHITE_, BLUE, WHITE_, BLUE, WHITE_)
# main function, a loop


def main():
    while True:
        print('\n'+'*'*50)
        number = input(prompt)
        try:
            if int(number) == 0:
                break
            elif int(number) > 4 or int(number) < 0:
                print('ERROR: WRONG INPUT!')
                continue
            query = input('Input your query:\n> ')
            # boolean query
            if(int(number) == 1):
                BooleanQuery.handler(query)
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
                print('Correcting ... ')
                # print(SpellCorrection.spell_correct(query))
                SpellCorrection.handler(query)
            # merge
            # if query.find('*')!=-1:
                #GlobbingQuery.controller(query, btree, btree_rev, wordlist)
        except Exception as e:
            print(RED+repr(e)+WHITE_)

if __name__ == '__main__':
    # check files
    if not os.path.exists('jsons'):
        # create a dir
        os.mkdir('jsons')
    if os.path.exists('jsons'):
        if os.path.isfile('jsons'):
            # create a dir
            raise Exception('Please make sure there is no file named jsons!')
        if not os.path.exists(os.path.join('jsons', 'InvertedIndex.json')) or \
           not os.path.exists(os.path.join('jsons', 'CompressedInvertedIndex.json')) or \
           not os.path.exists(os.path.join('jsons', 'Dictionary.json')) or \
           not os.path.exists(os.path.join('jsons', 'VSMSum.json')) or \
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
            VSM = InvertedIndex.build_VSM(index, doc_sizes)
            InvertedIndex.sumup_VSM(VSM)

    main()
