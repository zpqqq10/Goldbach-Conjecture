import BooleanQuery
import utils
import TopK

#通配查询
#使用通配符*代替字符
def handler(query):
    dictionary = utils.get_JSON('Dictionary')
    btree, rev_btree = build_tree(dictionary)
    #word_result：符合通配查询输入query的词表
    word_result = WildcardQuery(query, btree, rev_btree, dictionary)
    if len(word_result) == 0:
        print("There's no word that meet the query.")
    else:
        print("We list the words you may want to search as follows:")   
        print(word_result)
        print("And here are the doc ID of all search result:")
        #doc_result_list存放word_result中word查询得到的对应文档  
        doc_result_list = []
        for word in word_result:
            docID = utils.load_doclist(word)
            doc_result_list.append(docID)
            doc_result = doc_result_list[0]
        #调用布尔查询中的or操作得到全部结果
        for i in range(1,len(doc_result_list)):
            doc_result = BooleanQuery.build_or(doc_result,doc_result_list[i])
        # porecess result
        print(doc_result)
        doc_result = TopK.TopK_sort(doc_result)
        utils.print_result(word_result, doc_result, 'Wildcard Query')
    
#Node    
class Node(object):
    def __init__(self, key):
        self.key1 = key
        self.key2 = None
        self.left = None
        self.middle = None
        self.right = None
        
    #叶节点：没有子节点，均为None
    def is_leaf(self):
        if self.left is None and self.middle is None and self.right is None:
            return True
        else:
            return False

    #key2有值
    def is_full(self):
        if self.key2 is not None:
            return True
        else:
            return False

    #key1、key2至少一个为key
    def if_have_key(self, key):
        if (self.key1 == key) or (self.key2 is not None and self.key2 == key):
            return True
        else:
            return False

    def get_child(self, key):
        if key < self.key1:
            return self.left
        elif self.key2 is None:
            return self.middle
        elif key < self.key2:
            return self.middle
        else:
            return self.right

    def find_key(self, key1, key2):
        result = []
        if key2 <= self.key1:
            if self.left is not None:
                temp = self.left.find_key(key1, key2)
                for word in temp:
                    result.append(word)
        if key2 > self.key1 >= key1:
            if self.left is not None and self.key1 > key1:
                temp = self.left.find_key(key1, key2)
                for word in temp:
                    result.append(word)
            result.append(self.key1)
        if self.key2 is not None:
            if key2 <= self.key2:
                if self.middle is not None:
                    temp = (self.middle.find_key(key1, key2))
                    for word in temp:
                        result.append(word)
            if key2 > self.key2 >= key1:
                if self.middle is not None and self.key2 > key1:
                    temp = (self.middle.find_key(key1, key2))
                    for word in temp:
                        result.append(word)
                result.append(self.key2)
            if key1 > self.key2 or key2 > self.key2:
                if self.right is not None:
                    temp = (self.right.find_key(key1, key2))
                    for word in temp:
                        result.append(word)
        else:
            if key1 > self.key1 or key2 >= self.key1:
                if self.middle is not None:
                    temp = (self.middle.find_key(key1, key2))
                    for word in temp:
                        result.append(word)

        return result

#B-tree
class Tree(object):
    def __init__(self):
        self.root = None
    
    #遍历    
    def all_check_key(self, key):
        if self.root is None:
            return None
        else:
            return self.check_key(self.root, key)

    #若node有key值则不变，若无key值则继承子节点key值
    def check_key(self, node, key):
        if node is None:
            return None
        elif node.if_have_key(key):
            return node
        else:
            child = node.get_child(key)
            return self.check_key(child, key)
            
            
    def all_get_key(self, key):
        if self.root is None:
            self.root = Node(key)
        else:
            pKey, pRef = self.get_key(self.root, key)
            if pKey is not None:
                newnode = Node(pKey)
                newnode.left = self.root
                newnode.middle = pRef
                self.root = newnode
            
    def get_key(self, node, key):
            if node.if_have_key(key):
                return None, None
            elif node.is_leaf():
                return self.add_to_node(node, key, None)
            else:
                child = node.get_child(key)
                pKey, pRef = self.get_key(child, key)
                if pKey is None:
                    return None, None
                else:
                    return self.add_to_node(node, pKey, pRef)
                        
    def find(self, key1, key2):
        result = []
        if self.root is not None:
            result = (self.root.find_key(key1, key2))
        return result
              
    def split_node(self, node, key, pRef):
        newnode = Node(None)
        if key < node.key1:
            pKey = node.key1
            node.key1 = key
            newnode.key1 = node.key2
            if pRef is not None:
                newnode.left = node.middle
                newnode.middle = node.right
                node.middle = pRef
        elif key < node.key2:
            pKey = key
            newnode.key1 = node.key2
            if pRef is not None:
                newnode.left = pRef
                newnode.middle = node.right
        else:
            pKey = node.key2
            newnode.key1 = key
            if pRef is not None:
                newnode.left = node.right
                newnode.middle = pRef
        node.key2 = None
        return pKey, newnode
    
    def add_to_node(self, node, key, pRef):
        if node.is_full():
            return self.split_node(node, key, pRef)
        else:
            if key < node.key1:
                node.key2 = node.key1
                node.key1 = key
                if pRef is not None:
                    node.right = node.middle
                    node.middle = pRef
            else:
                node.key2 = key
                if pRef is not None:
                    node.right = pRef
            return None, None
             

def build_tree(wordlist):
    print("start to build B-tree.\n")
    #初始化建树
    btree = Tree()
    rev_btree = Tree()
    #对于词bike:b-tree针对bik*型搜索，将wordlist倒转后建立的reverse b-tree针对*ike型搜索
    #对于普适的情况如bi*e，从两树中分别查找然后求交集
    for word in wordlist: 
        btree.all_get_key(word)
        rev_btree.all_get_key(word[::-1])
    print("success for building B-tree！")
    return btree, rev_btree

def next_word(word):
    if(word[len(word)-1]<'z'):
        number = ord(word[len(word)-1])
        newword = word[0:len(word)-1]
        word = newword + chr(number+1)
    else:
        newword = word[0:len(word)-1]
        word = next_word(newword)+word[len(word)-1]
    return word

#通配查询:从词典中查出所有符合query的词
def WildcardQuery(query, btree, rev_btree, wordlist):
    if query == '*':
        return wordlist
    count = query.count('*')

    #只有一个通配符*
    if count == 1:
        #bik*型情况:b-tree
        if query[len(query)-1] == '*':
            words_list = query.split('*')
            word = words_list[0]
            word2 = next_word(word)
            result = btree.find(word, word2)
            return result
        
        #*ike型情况:reverse b-tree
        elif query[0] == '*':
            word = query[1::]
            word2 = next_word(word[::-1])[::-1]
            result_rev = rev_btree.find(word[::-1], word2[::-1])
            result = []
            for word in result_rev:
                result.append(word[::-1])
            return result
        
         #bi*e型情况：b-tree and reverse b-tree
        else:
            words = query.split('*')
            result1 = WildcardQuery(words[0]+'*', btree, rev_btree, wordlist)
            result2 = WildcardQuery('*'+words[1],btree, rev_btree, wordlist)
            result = []
            if result1 is None or result2 is None:
                return None
            for word in result1:
                if word in result2:
                    result.append(word)
            return result
        
    #一个查询中出现多个*    
    else:
        #判断query首、尾字符的情况，来决定将query拆成几部分
        if query[0]!='*' and query[len(query)-1]!='*':
            query_part = query.split('*')
            new_query = query_part[0]+'*'+query_part[len(query_part)-1]
        elif query[0]!='*':
            query_part = query.split('*')
            new_query = query_part[0]+'*'
        elif query[len(query)-1]!='*':
            query_part = query.split('*')
            new_query = '*'+query_part[len(query_part)-1]
        else:
            query_part = query.split('*')
            new_query = '*'
        #print(new_query)
        result = WildcardQuery(new_query, btree, rev_btree, wordlist)
        j = 0
        
        while True:
            if j>=len(result):
                break
            word = result[j]
            for i in range(1, len(query_part)-1):
                if word.find(query_part[i]) == -1:
                    result.remove(word)
                    j -= 1
                    break
            j += 1
        return result

