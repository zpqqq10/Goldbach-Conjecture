import utils


def handler(query):
    result = bool_query(query)
    query = query.replace('NOT','')
    query = query.replace('AND','')
    query = query.replace('OR','')
    query = query.replace('(','')
    query = query.replace(')','')
    query = query.strip(' ')
    while(query.find('  ') >= 0):
        query = query.replace('  ',' ')
    word_list = []
    word_list = query.split(' ')
    # print(word_list)
    # print(result)
    utils.print_result(word_list, result, 'Boolean Query')


def bool_query(query):
    query = query.strip(' ')
    while(query.find('  ') >= 0):
        query = query.replace('  ',' ')
    query_len = len(query)
    all_doc = utils.get_all_docID()

    isAnd = False
    isOr = False
    isNot = False
    isHeadNot = False
    isAndNot = False
    isOrNot = False
    isWord = False

    i = 0
    cur_word = ''

    result_cur = []
    result_add = []
    while(i < query_len):
        if(query[i] == 'A'):  # AND
            if(i + 2 < query_len and query[i + 1] == 'N' and query[i + 2] == 'D'):
                if(i == 0):
                    print('Bad Query! Meet AND at first!')
                    return []
                elif(i + 2 == query_len - 1):
                    print('Bad Query! Meet AND at the tail!')
                elif(query[i - 1] == ' ' and query[i + 3] == ' '):
                    # like -> ' AND '
                    if(isOr):
                        print('Bad Query! Meet AND after OR!')
                        return []
                    elif(isNot):
                        print('Bad Query! Meet AND after NOT!')
                        return []
                    elif(isAnd):
                        print('Bad Query! Meet AND after AND!')
                        return []
                    elif(isAndNot):
                        print('Bad Query! Meet AND after AND_NOT!')
                        return []
                    elif(isOrNot):
                        print('Bad Query! Meet AND after OR_NOT!')
                        return []
                    else:
                        isAnd = True
                        isWord = False
                        i = i + 4
                else:
                    cur_word = cur_word + query[i]
                    i = i + 1
            else:
                cur_word = cur_word + query[i]
                i = i + 1
        elif(query[i] == 'O'):  # OR
            if(i + 1 < query_len and query[i + 1] == 'R'):
                if(i == 0):
                    print('Bad Query! Meet OR at first!')
                    return []
                elif(i + 1 == query_len - 1):
                    print('Bad Query! Meet OR at the tail!')
                elif(query[i - 1] == ' ' and query[i + 2] == ' '):
                    # like -> ' OR '
                    if(isOr):
                        print('Bad Query! Meet OR after OR!')
                        return []
                    elif(isNot):
                        print('Bad Query! Meet OR after NOT!')
                        return []
                    elif(isAnd):
                        print('Bad Query! Meet OR after AND!')
                        return []
                    elif(isAndNot):
                        print('Bad Query! Meet OR after AND_NOT!')
                        return []
                    elif(isOrNot):
                        print('Bad Query! Meet OR after OR_NOT!')
                        return []
                    else:
                        isOr = True
                        isWord = False
                        i = i + 3
                else:
                    cur_word = cur_word + query[i]
                    i = i + 1
            else:
                cur_word = cur_word + query[i]
                i = i + 1
        elif(query[i] == 'N'):
            if(i + 2 < query_len and query[i + 1] == 'O' and query[i + 2] == 'T'):
                if(i + 2 == query_len - 1):
                    print('Bad Query! Meet NOT at the tail!')
                elif(i == 0):
                    if(query[i + 3] == ' '):
                        # 'NOT '
                        isNot = True
                        isHeadNot = True
                        isWord = False
                        i = i + 4
                    else:
                        cur_word = cur_word + query[i]
                        i = i + 1
                elif(query[i - 1] == ' ' and query[i + 3] == ' '):
                    # like -> ' NOT '
                    if(isOr):
                        # like -> ' OR NOT '
                        isOr = False
                        isOrNot = True
                        isWord = False
                        i = i + 4
                    elif(isNot):
                        print('Bad Query! Meet NOT after NOT!')
                        return []
                    elif(isAnd):
                        # like -> ' AND NOT '
                        isAnd = False
                        isAndNot = True
                        isWord = False
                        i = i + 4
                    elif(isAndNot):
                        print('Bad Query! Meet NOT after AND_NOT!')
                        return []
                    elif(isOrNot):
                        print('Bad Query! Meet NOT after OR_NOT!')
                        return []
                    else:
                        isNot = True
                        isWord = False
                        i = i + 4
                else:
                    cur_word = cur_word + query[i]
                    i = i + 1
            else:
                cur_word = cur_word + query[i]
                i = i + 1
        elif(query[i] == ' '):
            if(cur_word != ''):
                cur_word = cur_word.lower()
                if(isAnd):
                    result_add = utils.load_doclist(cur_word)
                    result_cur = build_and(result_cur, result_add)
                    isAnd = False
                    cur_word = ''
                    isWord = True
                elif(isOr):
                    result_add = utils.load_doclist(cur_word)
                    result_cur = build_or(result_cur, result_add)
                    isOr = False
                    cur_word = ''
                    isWord = True
                elif(isNot):
                    result_add = utils.load_doclist(cur_word)
                    result_add = build_not(result_add, all_doc)
                    if(isHeadNot):
                        result_cur = result_add
                        isHeadNot = False
                    else:
                        result_cur = build_and(result_cur, result_add)
                    isNot = False
                    cur_word = ''
                    isWord = True
                elif(isAndNot):
                    result_add = utils.load_doclist(cur_word)
                    result_add = build_not(result_add, all_doc)
                    result_cur = build_and(result_cur, result_add)
                    isAndNot = False
                    cur_word = ''
                    isWord = True
                elif(isOrNot):
                    result_add = utils.load_doclist(cur_word)
                    result_add = build_not(result_add, all_doc)
                    result_cur = build_or(result_cur, result_add)
                    isOrNot = False
                    cur_word = ''
                    isWord = True
                else:
                    if(isWord):
                        print('Bad Query! There should be no consecutive words!')
                        return []
                    else:
                        result_cur = utils.load_doclist(cur_word)
                        cur_word = ''
                        isWord = True
            i = i + 1
        elif(query[i] == ')'):
            print('Bad Query! Meet ) before (!')
            return []
        elif(query[i] == '('):
            count_left = 1
            count_right = 0
            bracket_finish = False
            i = i + 1
            bracket_word = ''
            while(i < query_len):
                if(query[i] == '('):
                    bracket_word = bracket_word + query[i]
                    count_left = count_left + 1
                    i = i + 1
                elif(query[i] == ')'):
                    count_right = count_right + 1
                    if(count_left == count_right):
                        bracket_finish = True
                        i = i + 1
                        break
                    elif(count_left < count_right):
                        print('Bad Query! Meet ) before )!')
                        return []
                    else:
                        bracket_word = bracket_word + query[i]
                    i = i + 1
                else:
                    bracket_word = bracket_word + query[i]
                    i = i + 1
            if(bracket_finish == False):
                print('Bad Query! Meet ( more than )!')
                return []
            else:
                if(isAnd):
                    result_add = bool_query(bracket_word)
                    result_cur = build_and(result_cur, result_add)
                    isAnd = False
                    isWord = True
                elif(isOr):
                    result_add = bool_query(bracket_word)
                    result_cur = build_or(result_cur, result_add)
                    isOr = False
                    isWord = True
                elif(isNot):
                    if(isHeadNot):
                        result_add = bool_query(bracket_word)
                        result_add = build_not(result_add, all_doc)
                        result_cur = result_add
                        isHeadNot = False
                    else:
                        result_add = bool_query(bracket_word)
                        result_add = build_not(result_add, all_doc)
                        result_cur = build_and(result_cur, result_add)
                    isNot = False
                    isWord = True
                elif(isAndNot):
                    result_add = bool_query(bracket_word)
                    result_add = build_not(result_add, all_doc)
                    result_cur = build_and(result_cur, result_add)
                    isAndNot = False
                    isWord = True
                elif(isOrNot):
                    result_add = bool_query(bracket_word)
                    result_add = build_not(result_add, all_doc)
                    result_cur = build_or(result_cur, result_add)
                    isOrNot = False
                    isWord = True
                else:
                    if(isWord):
                        print('Bad Query! There should be no consecutive words!')
                        return []
                    else:
                        result_cur = bool_query(bracket_word)
                        cur_word = ''
                        isWord = True
        else:
            cur_word = cur_word + query[i]
            i = i + 1
    if(cur_word != ''):
        cur_word = cur_word.lower()
        if(isAnd):
            result_add = utils.load_doclist(cur_word)
            result_cur = build_and(result_cur, result_add)
            isAnd = False
            cur_word = ''
            isWord = True
        elif(isOr):
            result_add = utils.load_doclist(cur_word)
            result_cur = build_or(result_cur, result_add)
            isOr = False
            cur_word = ''
            isWord = True
        elif(isNot):
            result_add = utils.load_doclist(cur_word)
            result_add = build_not(result_add, all_doc)
            if(isHeadNot):
                result_cur = result_add
                isHeadNot = False
            else:
                result_cur = build_and(result_cur, result_add)
            isNot = False
            cur_word = ''
            isWord = True
        elif(isAndNot):
            result_add = utils.load_doclist(cur_word)
            result_add = build_not(result_add, all_doc)
            result_cur = build_and(result_cur, result_add)
            isAndNot = False
            cur_word = ''
            isWord = True
        elif(isOrNot):
            result_add = utils.load_doclist(cur_word)
            result_add = build_not(result_add, all_doc)
            result_cur = build_or(result_cur, result_add)
            isOrNot = False
            cur_word = ''
            isWord = True
        else:
            if(isWord):
                print('Bad Query! There should be no consecutive words!')
                return []
            else:
                result_cur = utils.load_doclist(cur_word)
                cur_word = ''
                isWord = True
    return result_cur
                


def build_and(index1, index2):
    index1.sort()
    index2.sort()
    ret = []
    i1 = 0
    i2 = 0
    n1 = len(index1)
    n2 = len(index2)
    while(i1 < n1 and i2 < n2):
        if(index1[i1] == index2[i2]):
            ret.append(index1[i1])
            i1 = i1 + 1
            i2 = i2 + 1
        elif(index1[i1] < index2[i2]):
            i1 = i1 + 1
        else:
            i2 = i2 + 1
    return ret

def build_or(index1, index2):
    index1.sort()
    index2.sort()
    ret = []
    i1 = 0
    i2 = 0
    n1 = len(index1)
    n2 = len(index2)
    while(i1 < n1 and i2 < n2):
        if(index1[i1] == index2[i2]):
            ret.append(index1[i1])
            i1 = i1 + 1
            i2 = i2 + 1
        elif(index1[i1] < index2[i2]):
            ret.append(index1[i1])
            i1 = i1 + 1
        else :
            ret.append(index2[i2])
            i2 = i2 + 1
    while(i1 < n1):
        ret.append(index1[i1])
        i1 = i1 + 1
    while(i2 < n2):
        ret.append(index2[i2])
        i2 = i2 + 1
    return ret

def build_not(index, all_doc):
    index.sort()
    all_doc.sort()
    ret = []
    i1 = 0
    i2 = 0
    n1 = len(index)
    n2 = len(all_doc)
    while(i1 < n1 and i2 < n2):
        if(index[i1] > all_doc[i2]):
            ret.append(all_doc[i2])
            i2 = i2 + 1
        elif(index[i1] == all_doc[i2]):
            i1 = i1 + 1
            i2 = i2 + 1
    while(i2 < n2):
        ret.append(all_doc[i2])
        i2 = i2 + 1
    return ret
