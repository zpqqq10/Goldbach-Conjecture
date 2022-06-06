from xmlrpc.client import MAXINT
import utils

def spell_correct(word):
    doc_list = utils.load_doclist_withp(word)
    # the dictionary does not contain this word
    if(len(doc_list) == 0):
        # get dictionary
        dictionary = utils.get_JSON('Dictionary')

        # get possible word
        possible_word = []
        i = 0
        min_distance = MAXINT
        while(i < len(dictionary)):
            if(abs(len(dictionary[i]) - len(word)) > min_distance):
                i = i + 1
                continue
            cur_distance = levenshtein(word, dictionary[i])
            if(cur_distance < min_distance):
                min_distance = cur_distance
                possible_word.clear()
                possible_word.append(dictionary[i])
            elif(cur_distance == min_distance):
                possible_word.append(dictionary[i])
            i = i + 1
        
        # print(possible_word)
        # select word with the highest frequency
        word_num = len(possible_word)
        if(word_num == 0):
            return 'there is no possible word to correct'
        if(word_num == 1):
            return possible_word[0]
        i = 0
        result = ''
        max_frequency = 0
        while(i < word_num):
            cur_frequency = word_frequency(possible_word[i])
            # print(cur_frequency)
            if(cur_frequency > max_frequency):
                max_frequency = cur_frequency
                result = possible_word[i]
            i = i + 1
        return result


# compute levenshtein distance between word1 and word2
def levenshtein(word1, word2):
    n1 = len(word1)
    n2 = len(word2)
    m = [[0 for i in range(n2 + 1)] for j in range(n1 + 1)]
    i = 0
    j = 0
    while(i <= n1):
        m[i][0] = i
        i = i + 1
    while(j <= n2):
        m[0][j] = j
        j = j + 1
    i = 1
    while(i <= n1):
        j = 1
        while(j <= n2):
            if(word1[i - 1] == word2[j - 1]):
                m[i][j] = min(m[i-1][j] + 1, m[i][j-1] + 1, m[i-1][j-1])
            else:
                m[i][j] = min(m[i-1][j] + 1, m[i][j-1] + 1, m[i-1][j-1] + 1)
            j = j + 1
        i = i + 1
    return m[n1][n2]

# compute word frequency
def word_frequency(word):
    doc_list = utils.load_doclist_withp(word)
    # print(doc_list)
    result = 0
    for value in doc_list.values():
        result = result + len(value)
    return result

