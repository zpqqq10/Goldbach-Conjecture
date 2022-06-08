import utils

TOPK = 10

def _TopK_sort(doclist):
    _doclist = {}
    print(doclist)
    for docID in doclist:
        _doclist[docID] = utils.load_docsum(docID)[2]
    return sorted(_doclist.items(), key=lambda i: i[1], reverse=True)


def TopK_sort(doclist, k=TOPK):
    vsm = utils.get_JSON('VSMSum')
    inputdata = []
    for docID in doclist:
        inputdata.append((docID, vsm[str(docID)][2]))

    if len(doclist) < TOPK:
        k = len(doclist)
    return TopK(inputdata, k)


def TopK(id_score, k):
    size = len(id_score)
    minheap = Heap(id_score, size)
    minheap.Build_max_heap()
    res = []
    for i in range(k):
        res.append(minheap.pop())
    res += minheap.Allnodes()
    return res


class Heap():
    # data: list of first K data
    def __init__(self, data=[], s=1) -> None:
        self.size = s
        # data (score,doc id)
        self.heap = data

    # let this heap a minheap with root n
    def shiftdown(self, i):
        n = self.size
        t = 0
        while i*2+1 < n:
            _, i_value = self.heap[i]
            _, left_value = self.heap[2*i+1]
            if i_value < left_value:
                t = i*2+1
            else:
                t = i
            _, t_value = self.heap[t]

            if i*2+2 < n:
                _, right_value = self.heap[i*2+2]
                if t_value < right_value:
                    t = i*2+2

            if t != i:
                self.heap[t], self.heap[i] = self.heap[i], self.heap[t]
                i = t
            else:
                break

    def Build_max_heap(self):
        for i in range(int((self.size-2)/2), -1, -1):
            self.shiftdown(i)

    def top(self):
        return self.heap[0]

    def Allnodes(self):
        return self.heap

    def pop(self):
        res = self.heap[0]
        self.heap.remove(res)
        self.size -= 1
        self.Build_max_heap()
        return res
