class trie(object):
    def __init__(self, path, depth):
        self.path = path
        self.depth = depth
        self.tot = 0
        self.ends = 0
        self.children = {} 

    def add(self, line):
        self.tot += 1
        if not line: 
            self.ends += 1
        elif self.depth<11: 
            first,remain = line[0], line[1:]
            if first not in self.children:
                self.children[first] = trie(self.path+first, self.depth+1)
            self.children[first].add(remain)
    
    def travel(self, min_depth=3, max_depth=8, is_valid=False):
        if self.depth>max_depth:
            if is_valid:
                yield '%s\t%s' % (self.path, self.tot)
        elif self.depth<min_depth:
            for c in self.children:
                child = self.children[c]
                for line in child.travel(min_depth, max_depth, False):
                    yield line 
        elif self.tot > 100:
            new_valid = False
            valid_child = None
            for c in self.children:
                child = self.children[c]
                if child.tot * 3 >= self.tot:
                    new_valid = True 
                    valid_child = child
            if is_valid and not new_valid:
                yield '%s\t%s' % (self.path, self.tot)
            elif new_valid:
                for line in valid_child.travel(min_depth,max_depth,True): 
                    yield line
            else: 
                for c in self.children:
                    child = self.children[c]
                    for line in child.travel(min_depth, max_depth, False):
                        yield line 

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 5:
        print '<usage> in out from n'
        exit(1)
    root = trie('^', 0)
    n = 0
    start_n = int(sys.argv[3])
    end_n = int(sys.argv[3]) + int(sys.argv[4])
    for line in open(sys.argv[1]):
        arr = line.strip().split('\t',4)
        try: name = arr[1]
        except: continue 
        n+=1
        if n%100000 == 0: print n
        if n >= start_n and n<end_n:
            x = [v for v in name.lower().split('.') if v]
            if len(x)==3: 
                root.add('%s.%%.%s' % (x[0], x[2])) 
                root.add('%%.%s.%s' % (x[1], x[2])) 
            x = [v for v in name.lower().split('_') if v]
            if len(x)==3: 
                root.add('%s_%%_%s' % (x[0], x[2])) 
                root.add('%%_%s_%s' % (x[1], x[2])) 
            elif len(x)==2: 
                root.add('%s_%%' % (x[0])) 
                root.add('%%_%s' % (x[1])) 
            elif len(x)==1: 
                root.add(x[0])
            root.add(name.lower()[::-1]) 
        if n>=end_n: break
    with open(sys.argv[2], 'w') as fo:
        for line in root.travel(5, 12):
            fo.write(line + '\n') 

