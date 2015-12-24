#!/usr/local/python2.7/bin/python2.7
#coding: utf-8
import sys,json

conj = set(["S","C"])

hapax = set()

wordFreq = {}


def logDice (bigrams, host2json, relation2json, lemma2json):
    if ' of' not in relation2json:
        logDice = 14 + (2*bigrams[host2json][relation2json][1][lemma2json][0])/(bigrams[host2json][relation2json][0] + bigrams[lemma2json][relation2json+' of'][0])
        log = logDice, bigrams[host2json][relation2json][1][lemma2json][0], bigrams[host2json][relation2json][0], bigrams[lemma2json][relation2json+' of'][0]
        return log[0]
    else:
        relationCUT = relation2json[0:-3]
        logDice = 14 + (2*bigrams[host2json][relation2json][1][lemma2json][0])/(bigrams[host2json][relation2json][0] + bigrams[lemma2json][relationCUT][0])
        log = logDice, bigrams[host2json][relation2json][1][lemma2json][0], bigrams[host2json][relation2json][0], bigrams[lemma2json][relationCUT][0]
        return log[0]


for line in open('ruscorpora_treetagger_vocabulary.csv','r', encoding='utf-8'):#changed
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
bigramsHost = {}
sentence = {}

for line in open('Filename.conll','r', encoding='utf-8'):
    res = line.split('\t')
    if len(res) == 1:
        for word in sentence:
            if sentence[word]['relation'] != 'ROOT' and sentence[word]['relation'] != 'PUNC' and sentence[word]['lemma'] != "--" and sentence[word]['lemma'] != '—' and len(sentence[word]['lemma']) > 0 and not sentence[word]['pos'] in conj:
                relation2json = sentence[word]['relation']

                if relation2json not in relationFreq:
                    relationFreq[relation2json] = 1
                else:
                    relationFreq[relation2json] += 1
                    
                lemma2json = sentence[word]['lemma'].strip()
                if lemma2json == "%" or lemma2json == '--' or lemma2json == '...' or '\\' in lemma2json or '//' in lemma2json:
                    continue
                if lemma2json in hapax:
                    continue
                host2json = sentence[sentence[word]['host']]['lemma']
                if sentence[sentence[word]['host']]['pos'].strip() in conj:
                    continue
#                if len(host2json.strip().decode('utf-8')) < 3:
                if len(host2json.strip()) < 3:
                    #print(sentence[sentence[word]['host']]['lemma'])
                    continue
                if host2json.strip() == "%" or host2json.strip() == '--' or host2json.strip() == '...' or '\\' in host2json.strip() or '//' in host2json.strip():
                    continue
                if host2json.strip() in hapax:
                    continue
                host2json = host2json.strip()

                #add hosts
                '''
                if not lemma2json in bigramsHost:
                    bigramsHost[lemma2json] = {}
                if not relation2json+' of' in bigramsHost[lemma2json]:
                    bigramsHost[lemma2json][relation2json+' of'] = [0,{}]
                bigramsHost[lemma2json][relation2json+' of'][0] += 1
                if not host2json in bigramsHost[lemma2json][relation2json+' of'][1]:
                    bigramsHost[lemma2json][relation2json+' of'][1][host2json] = 0
                bigramsHost[lemma2json][relation2json+' of'][1][host2json] += 1
                if relation2json+' of' not in relationFreq:
                    relationFreq[relation2json+' of'] = 1
                else:
                    relationFreq[relation2json+' of'] += 1
                '''

                if not lemma2json in bigrams:
                    bigrams[lemma2json] = {}
                if not relation2json+' of' in bigrams[lemma2json]:
                    bigrams[lemma2json][relation2json+' of'] = [0,{}]
                bigrams[lemma2json][relation2json+' of'][0] += 1
                if not host2json in bigrams[lemma2json][relation2json+' of'][1]:
                    bigrams[lemma2json][relation2json+' of'][1][host2json] = [0, 0]
                bigrams[lemma2json][relation2json+' of'][1][host2json][0] += 1
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
                    bigrams[host2json][relation2json][1][lemma2json] = [0, 0]
                bigrams[host2json][relation2json][1][lemma2json][0] += 1

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
    
#print(json.dumps(bigrams,ensure_ascii=False))
#print(relationFreq)
#print(bigramsHost)
'''
for word in bigramsHost:
    if "предик of" in bigramsHost[word]:
        print(word, bigramsHost[word]["предик of"])
'''
'''
word = 'компания'
print(word)
if word in bigramsHost:
    print(bigramsHost[word])
if word in bigrams:
    print(bigrams[word])

#print(relationFreq)
'''
'''
for lemma2json in bigrams:
    for relation2json in bigrams:
        for host2json in bigrams
    bigrams[host2json][relation2json][1][lemma2json][0]
'''

word = 'choose a word'
print(word)
for relation in bigrams[word]:
    for lemma in bigrams[word][relation][1]:
        print(relation, lemma, 'AM = ', logDice(bigrams, word, relation, lemma))
        #print(word, relation, lemma)


