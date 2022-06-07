from torch import topk
import re
import BooleanQuery
import utils
import TopK

#通配查询
#使用通配符*代替字符
def handler(query):
    word_list = utils.word_split(query)
    result =wildcard_query(query, word_list)
    # porecess result
    result = TopK.TopK_sort(result)
    utils.print_result(word_list, result, 'Wildcard Query')
    
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
        if(self.left is None and self.middle is None and self.right is None):
            return True
        else:
            return False

    #key2有值
    def is_full(self):
        if(self.key2 is not None):
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
        
    #若node有key值则不变，若无key值则继承子节点key值
    def check_key(self, node, key):
        if node is None:
            return None
        elif node.if_have_key(key):
            return node
        else:
            child = node.get_child(key)
            return self.check_key(child, key)
    
    #遍历    
    def all_check_key(self, key):
        if self.root is None:
            return None
        else:
            return self.check_key(self.root, key)

               
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
        if node.isFull():
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
            
    def find(self, key1, key2):
        result = []
        if self.root is not None:
            result = (self.root.find_key(key1, key2))
        return result

def build_tree(wordlist):
    #print("start to build B-tree.\n")
    #初始化建树
    btree = Tree()
    rev_btree = Tree()
    #对于词bike:b-tree针对bik*型搜索，将wordlist倒转后建立的reverse b-tree针对*ike型搜索
    #对于普适的情况如bi*e，从两树中分别查找然后求交集
    for word in wordlist: 
        btree.all_get_key(word)
        rev_btree.all_get_key(word[::-1])
    #print(btree.root.key1)
    #print(rev_btree.root.key1)
    #print("success for building B-tree！")
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

#通配查询
#目前只支持一个*的查询
def wildcard_query(query, btree, rev_btree, wordlist):
    if query == '*':
        return wordlist
    count = query.count('*')

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
            result1 = wildcard_query(words[0]+'*', btree, rev_btree, wordlist)
            result2 = wildcard_query('*'+words[1],btree, rev_btree, wordlist)
            result = []
            if result1 is None or result2 is None:
                return None
            for word in result1:
                if word in result2:
                    result.append(word)
            return result
        
    else:
    #多个*的情况待补充
        return result


