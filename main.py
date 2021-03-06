# !/usr/bin/env python

import os
from tqdm import tqdm
import wget
from utils import *
import rarfile
import InvertedIndex
import BooleanQuery
import SpellCorrection
import TermQuery
import PhraseQuery
import WildcardQuery
import SynonmyQuery
# sudo apt install unrar


prompt = '''Please select the query mode:  
    {}1{}.Boolean Query
    {}2{}.Phrase Query
    {}3{}.Wildcard Query
    {}4{}.Term Query
    {}5{}.Synonmy Query
    {}6{}.Spell Correction
    {}0{}.quit
> '''.format(BLUE, WHITE_, BLUE, WHITE_, BLUE, WHITE_, BLUE, WHITE_, BLUE, WHITE_, BLUE, WHITE_, BLUE, WHITE_)
# main function, a loop



def main():
    while True:
        print('\n'+'*'*50)
        number = input(prompt)
        try:
            if int(number) == 0:
                break
            elif int(number) > 6 or int(number) < 0:
                print('ERROR: WRONG INPUT!')
                continue
            query = input('Input your query:\n> ')
            # boolean query
            if(int(number) == 1):
                BooleanQuery.handler(query)
            # phrase query
            elif(int(number) == 2):
                PhraseQuery.handler(query)
            # wildcard query
            elif(int(number) == 3):
                WildcardQuery.handler(query)
            # term query
            elif(int(number) == 4):
                TermQuery.handler(query)
            # synonmy query 
            elif(int(number) == 5):
                SynonmyQuery.handler(query)
            # Correction
            elif(int(number) == 6):
                print('Correcting ... ')
                SpellCorrection.handler(query)
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
           not os.path.exists(os.path.join('jsons', 'VSM.json')) or \
           not os.path.exists(os.path.join('jsons', 'Stem2Word.json')):
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
            vsm, dictionary = InvertedIndex.build_VSM(index, doc_sizes)
            InvertedIndex.sumup_VSM(vsm)
            InvertedIndex.stemming(dictionary)

    main()
