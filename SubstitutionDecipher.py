% A code to first find information on some base text including letter and bigram-letter frequencies from a base text, and use it to decode some random cipher.
% I have used the ebooks of 'Pride and Prejeudice' and 'The Count of Monte Cristo' from Projet Gutenberg


import numpy as np
import string
from itertools import islice
import random
import math
from matplotlib import pyplot as plt
import seaborn as sns

def slice(n,str):
    return list(islice(str,n))

def textsimp(file):
    with open(file, encoding="utf8") as samp:
        text = samp.read()
    plain = []
    for t in text.lower():
        if t in (' ','\n','\r', '\t' ):
            if plain and plain[-1] != ' ':
                plain.append(' ')            
        if t in string.ascii_lowercase:
            plain.append(t)
    return "".join(plain)


def letterfreq(text):
    a=1
    freq = [0 for i in range(27)]
    for i in string.ascii_lowercase:
        for j in text:
            if i == j:
                freq[a] = freq[a] + 1
        a=a+1
    space = len(text) - sum(freq)
    freq[0] = freq[0] + space
    return freq

def letterprob(text):
    freq = letterfreq(text)
    n = sum(freq)
    return [i/n for i in freq]
    
    
pride = textsimp('PridePrejudice.txt')
cristo = textsimp('Cristo.txt')


def bigramprob(text):
    freq = [[0 for i in range(27)] for j in range(27)]
    characters = "".join((" ",string.ascii_lowercase))
    for i in range(len(text)-1):
        if text[i+1] == " ":
            for j in range(1,27):
                if text[i] == characters[j]:
                    freq[j][0] = freq[j][0] + 1           
        for a in range(1,27):
            if text[i+1] == characters[a]:
                for k in range(0,27):
                    if text[i] == characters[k]:
                        freq[k][a] = freq[k][a] + 1
    totals = [sum(i) for i in freq]
    prob = [[freq[a][b]/totals[a] for b in range(27)] for a in range(27)]
    return prob




def make_key():
    characters = list(string.ascii_lowercase)
    random.shuffle(characters)
    key = dict(zip(string.ascii_lowercase,characters))
    return key




def decrypt(code,key):
    trans = str.maketrans(key)
    return code.translate(trans)



def score(text,sampletters,sampbigram, letterweight = 2, bigramweight = 1):
    letterweight = letterweight/(letterweight+bigramweight)
    bigramweight = bigramweight/(letterweight+bigramweight)
    characters = "".join((" ",string.ascii_lowercase))
    aa = []
    bb = []
    current_score = 0
    for a,b in zip(text[:-1],text[1:]):
        for i in range(0,27):
            if a == characters[i]:
                aa.append(i)
        for i in range(0,27):
            if b == characters[i]:
                bb.append(i)
        current_score = current_score + math.log(letterweight*sampletters[(aa[-1])]
                                  +bigramweight*sampbigram[(aa[-1])][(bb[-1])])
    return current_score

encryption = make_key()
cristo_appended = cristo[1:10000]
cristo_encrypted = decrypt(cristo_appended,encryption)

prideprobs = letterprob(pride)
pridebigram = bigramprob(pride)


axis_labels = [' ','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o',
               'p','q','r','s','t','u','v','w','x','y','z']

ax = sns.heatmap(pridebigram, linewidth=0.5,xticklabels=axis_labels,
                yticklabels=axis_labels)
plt.show()

'''

iterations =5001

decrypt_key = make_key()
best_decryption = decrypt(cristo_encrypted,decrypt_key)
best_score = score(best_decryption,prideprobs,pridebigram)

for i in range(iterations):
    a,b = random.choices(string.ascii_lowercase,k=2)
    decrypt_key[a],decrypt_key[b] = decrypt_key[b], decrypt_key[a]
    current_decryption = decrypt(cristo_encrypted,decrypt_key)
    current_score = score(current_decryption,prideprobs,pridebigram)
    if current_score > best_score:
        best_score = current_score
    else:
        decrypt_key[a],decrypt_key[b] = decrypt_key[b], decrypt_key[a]
    if i%500 == 0:
        print('{n}: {d}'.format(n=i, d = current_decryption[6000:6150]))
        
        
'''
        
        

                        
                        
