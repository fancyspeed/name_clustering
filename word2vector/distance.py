# coding: utf-8
import os
import math

def norm_l2(float_list):
    tot = math.sqrt(sum([v**2 for v in float_list]))
    if tot == 0:
        return [0] * len(float_list)
    return [v/tot for v in float_list]
    
def mean(vec_list, axis=0):
    if not vec_list: return 0
    tot = []
    for i in xrange(len(vec_list[0])):
        tot.append(sum([vec_list[j][i] for j in xrange(len(vec_list))]))
    list_len = float(len(vec_list))
    return [v/list_len for v in tot]

def cosine_dist(vec_1, vec_2):
    s = sum([v1*vec_2[i] for i, v1 in enumerate(vec_1)])
    t1 = math.sqrt(sum([v**2 for v in vec_1]))
    t2 = math.sqrt(sum([v**2 for v in vec_2]))
    if t1==0 or t2==0: return 0 
    return s/t1/t2
            
def load_word2vec(p_in, is_binary=False):
    word_vec = {}
    if not os.path.isfile(p_in):
        raise Exception("no such file: %" % p_in)
    for line in open(p_in):
        arr = line.strip().split(' ')
        if len(arr) < 2: continue
        word = arr[0].lower()
        vec = map(float, arr[1:])
        word_vec[word] = norm_l2(vec)
    return word_vec

def get_similar_words(word_list, word_vec, top_n=10):
    vec_list = []
    for word in word_list:
        if word not in word_vec:
            return word
        vec_list.append(word_vec[word])
    mean_vec = mean(vec_list)

    dist_dict = {}
    for word in word_vec:
        if word in word_list: continue
        dist_dict[word] = cosine_dist(word_vec[word], mean_vec) 
    return sorted(dist_dict.items(), key=lambda d:-d[1])[:top_n]
        

def main():
    import sys
    if len(sys.argv) != 2:
        print '<usage> %s p_model' % sys.argv[0]
        exit(1)
    word_vec = load_word2vec(sys.argv[1])
    while True:
        word_list = raw_input('Exit or any word->').lower().split(' ')
        if word_list and word_list[0] == 'exit': break
        top_words = get_similar_words(word_list, word_vec, 10)
        for word, score in top_words:
            print '\t\t%s\t\t%s' % (word, score)

if __name__ == '__main__':
    main()
