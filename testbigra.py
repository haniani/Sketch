#coding: utf-8

import sys,json
import os, io
import math, re, csv


conj = set(["S","C"])
hapax = set()
wordFreq = {}

i=0

def logDice (bigrams, host, relation, lemma, tag):

    if tag == None and ' of' not in relation:
        logDice = 14 + math.log(float(2*bigrams[host][relation][1][lemma][0])/float(bigrams[host][relation][0] + bigrams[lemma][relation+' of'][0]), 2)
        log = logDice, bigrams[host][relation][1][lemma][0], bigrams[host][relation][0], bigrams[lemma][relation+' of'][0]
        return log[0]
    elif tag == None and ' of' in relation:
        relationCUT = relation[0:-3]
        logDice = 14 + math.log(float(2*bigrams[host][relation][1][lemma][0])/float(bigrams[host][relation][0] + bigrams[lemma][relationCUT][0]), 2)
        log = logDice, bigrams[host][relation][1][lemma][0], bigrams[host][relation][0], bigrams[lemma][relationCUT][0]
        return log[0]
    elif tag != None and ' of' not in relation:
        freqTag = 0
        for host_i in bigrams[lemma][relation+' of'][1]:
            if tag in bigrams[lemma][relation+' of'][1][host_i]:
                freqTag += bigrams[lemma][relation+' of'][1][host_i][2][tag][1]
        logDice = 14 + math.log(float(2*bigrams[host][relation][1][lemma][2][tag][1])/float(bigrams[host][relation][0] + freqTag), 2)
        log = logDice, bigrams[host][relation][1][lemma][2][tag][1], bigrams[host][relation][0], freqTag
        return log[0]
    else:
        return 0


for line in open('ruscorpora_treetagger_vocabulary.csv','r'):
    i += 1
    res = line.strip().split('\t')
    if len(res) != 2:
        continue
    (freq,word) = res
    freq = int(freq.strip())
    if freq == 1:
        hapax.add(word.strip())
    else:
        wordFreq[word]= freq

relationFreq = {}
bigrams = {}
generateBigram = list()

def bigramSketch(file):
    sentence = {}
    with open(file, 'r') as chotatam:
        for line in chotatam:
            res = line.split('\t')
            if len(res) == 1:
                for word in sentence:
                    if sentence[word]['relation'] != 'ROOT' and sentence[word]['relation'] != 'PUNC' and sentence[word]['lemma'] != "--" and sentence[word]['lemma'] != '—' and len(sentence[word]['lemma']) > 0 and not sentence[word]['pos'] in conj:
                        relation2json = sentence[word]['relation']

                        if relation2json not in relationFreq:
                            relationFreq[relation2json] = 1
                        else:
                            relationFreq[relation2json] += 1

                        token2json = sentence[word]['token'].strip()
                        if token2json == "%" or token2json == '--' or token2json == '...' or '\\' in token2json or '//' in token2json:
                            continue

                        tag2json = sentence[word]['tag'].strip()
                        if tag2json == "%" or tag2json == '--' or tag2json == '...' or '\\' in tag2json or '//' in tag2json:
                            continue


                        lemma2json = sentence[word]['lemma'].strip()
                        if lemma2json == "%" or lemma2json == '--' or lemma2json == '...' or '\\' in lemma2json or '//' in lemma2json:
                            continue
                        if lemma2json in hapax:
                            continue
                        host2json = sentence[sentence[word]['host']]['lemma']
                        if sentence[sentence[word]['host']]['pos'].strip() in conj:
                            continue
                        if len(host2json.strip().decode('utf-8', "replace")) < 3:
                            #print >> sys.stderr, sentence[sentence[word]['host']]['lemma']
                            continue
                        if host2json.strip() == "%" or host2json.strip() == '--' or host2json.strip() == '...' or '\\' in host2json.strip() or '//' in host2json.strip():
                            continue
                        if host2json.strip() in hapax:
                            continue
                        host2json = host2json.strip()



                        if not lemma2json in bigrams:
                            bigrams[lemma2json] = {}
                        if not relation2json+' of' in bigrams[lemma2json]:
                            bigrams[lemma2json][relation2json+' of'] = [0,{}]
                        bigrams[lemma2json][relation2json+' of'][0] += 1
                        if not host2json in bigrams[lemma2json][relation2json+' of'][1]:
                            bigrams[lemma2json][relation2json+' of'][1][host2json] = [0, 0, {}]
                        if not tag2json in bigrams[lemma2json][relation2json+' of'][1][host2json][2]:
                            bigrams[lemma2json][relation2json+' of'][1][host2json][2][tag2json] = [token2json, 0, 0]

                        bigrams[lemma2json][relation2json+' of'][1][host2json][0] += 1
                        bigrams[lemma2json][relation2json+' of'][1][host2json][2][tag2json][1] += 1

                        if relation2json+' of' not in relationFreq:
                            relationFreq[relation2json+' of'] = 1
                        else:
                            relationFreq[relation2json+' of'] += 1


                        if not host2json in bigrams:
                            bigrams[host2json] = {}
                        if not relation2json in bigrams[host2json]:
                            bigrams[host2json][relation2json] = [0,{}]
                        bigrams[host2json][relation2json][0] += 1
                        if not lemma2json in bigrams[host2json][relation2json][1]:
                            bigrams[host2json][relation2json][1][lemma2json] = [0, 0, {}]
                        if not tag2json in bigrams[host2json][relation2json][1][lemma2json][2]:
                            bigrams[host2json][relation2json][1][lemma2json][2][tag2json] = [token2json, 0, 0]
                        bigrams[host2json][relation2json][1][lemma2json][0] += 1
                        bigrams[host2json][relation2json][1][lemma2json][2][tag2json][1] += 1

                        if relation2json not in relationFreq:
                            relationFreq[relation2json] = 1
                        else:
                            relationFreq[relation2json] += 1



                #print sentence[sentence[word]['host']]['out']+'\t'+sentence[word]['out']+'\t'+sentence[word]['relation']
                sentence = {}
                continue


            (number,token,lemma,pos1,pos2,tag,host,relation,strange1,strange2) = res
            lemma = lemma.replace('«','').strip()
            lemma = lemma.replace('»','').strip()
            lemma = lemma.replace('...','').strip()
            lemma = lemma.replace('*','').strip()

            sentence[number] = {}
            sentence[number]['lemma'] = lemma.strip()
            sentence[number]['token'] = token.strip()
            sentence[number]['host'] = host.strip()
            sentence[number]['relation'] = relation.strip()
            sentence[number]['pos'] = pos1
            sentence[number]['out'] = token+' '+lemma+' '+pos1
            sentence[number]['tag'] = tag.strip()


for root, dirs, files in os.walk(r'/home/rmuhanova/FilesForSketch/corpus'):
    generateBigram += [os.path.join(root, name) for name in files if name[-5:] == 'conll']


for each in generateBigram:
    bigramSketch(each)


for word in bigrams:                                                                #слово
    for relation in bigrams[word]:                                                  #отношение
        for lemma in bigrams[word][relation][1]:                                    #лемма
            try:
                logLem = logDice(bigrams, word, relation, lemma, None)
            except:
                logLem = 0
            bigrams[word][relation][1][lemma][1] = logLem                           #лемма логдайс
            for tag in bigrams[word][relation][1][lemma][2]:                        #тэг
                try:
                    logTok = logDice(bigrams, word, relation, lemma, tag)
                except:
                    logTok = 0
                bigrams[word][relation][1][lemma][2][tag][2] = logTok               #токен логдайс
'''
with open('bigrams.json', 'a') as b:                 #общий корпус биграммов
        for key, value in bigrams.items():
            g = json.dumps(value, ensure_ascii=False)
            p = str(key) + str(g) + "\n"
            print(p)
            b.write(p)
'''

j = 0
dictofallwords = open("dictofallwords.txt", 'w')                    #отдельными файлами + оглавление

for key, value in bigrams.items():
    g = json.dumps(value, ensure_ascii=False)
    nameforword = key.decode("utf-8")
    b = open(nameforword +'.json', "w")
    p = str(key) + str(g) + "\n"
    b.write(p)
    j += 1
    dictofallwords.write(str(key) + ":" + str(j) + "\n")


w = open('relationFreq.tsv', 'w')
#d = open('relationFreqdict.tsv', 'w')
for rel in relationFreq:
    s = rel+'\t'+str(relationFreq[rel])+'\n'
    #c =  rel+':'+str(relationFreq[rel]) +'\n'
    w.write(s)
    #d.write(c)
w.close()
#d.close()
b.close()
dictofallwords.close()
