#!/usr/bin/python2
#coding: utf-8
import sys,json,codecs

def logDice (trigrams, host, relation, lemma, tag):
    if tag == None and ' of' not in relation:
        logDice = 14 + (2*trigrams[host][relation][1][lemma][0])/(trigrams[host][relation][0] + trigrams[lemma][relation+' of'][0])
        log = logDice, trigrams[host][relation][1][lemma][0], trigrams[host][relation][0], trigrams[lemma][relation+' of'][0]
        return log[0]
    elif tag == None and ' of' in relation:
        relationCUT = relation[0:-3]
        logDice = 14 + (2*reigrams[host][relation][1][lemma][0])/(trigrams[host][relation][0] + trigrams[lemma][relationCUT][0])
        log = logDice, trigrams[host][relation][1][lemma][0], trigrams[host][relation][0], trigrams[lemma][relationCUT][0]
        return log[0]
    elif tag != None and ' of' not in relation:
        freqTag = 0
        for host_i in trigrams[lemma][relation+' of'][1]:
            if tag in trigrams[lemma][relation+' of'][1][host_i]:
                freqTag += trigrams[lemma][relation+' of'][1][host_i][2][tag][1]
        logDice = 14 + (2*trigrams[host][relation][1][lemma][2][tag][1])/(trigrams[host][relation][0] + freqTag)
        log = logDice, trigrams[host][relation][1][lemma][2][tag][1], trigrams[host][relation][0], freqTag
        return log[0]
    else:
        return 0

cases = {"n":"Nom","g":"Gen","d":"Dat","a":"Acc","v":"Voc","l":"Loc","i":"Ins"}

hapax = set()
relationFreq = {}

for line in open('ruscorpora_treetagger_vocabulary.csv','r'):
    res = line.strip().split('\t')
    if len(res) != 2:
        continue
    (freq,word) = res
    freq = int(freq.strip())
    if freq == 1:
        hapax.add(word.strip())

valid = set()

for line in codecs.open('predlogi.txt','r','utf-8').readlines():
    res = line.strip()
    valid.add(res)

trigrams = {}

for line in sys.stdin:
    if (float(len(trigrams))/10000).is_integer():
        print >> sys.stderr, "Words in trigrams matrix:", len(trigrams)

    trigram = json.loads(line.strip())
    if not trigram["1"]["lemma"].isalnum() or not trigram["2"]["lemma"].isalnum() or not trigram["3"]["lemma"].isalnum() or trigram["3"]["tag"][1] == "-":
        continue
    a = trigram["1"]["lemma"]
    if a.strip() == "%" or a.strip() == '--' or a.strip() == '...' or '\\' in a.strip() or a.strip() == "-" or len(a.strip()) < 3:
        continue
    if a.strip() in hapax:
        continue


    if u"предл" in trigram["2"]["relation"]:
        connector = trigram["2"]["lemma"]+"_"+cases[trigram["3"]["tag"][1]]
        if not connector in valid:
            continue
        c = trigram["3"]["lemma"]
        token = trigram["3"]["token"]
        tag = trigram["3"]["tag"][0]
        if c.strip() == "%" or c.strip() == '--' or c.strip() == '...' or '\\' in c.strip() or c.strip() == '-':
            continue
        if c.strip() in hapax:
            continue
        if not a in trigrams:
            trigrams[a] = {}
        if not connector in trigrams[a]:
            trigrams[a][connector] = [0, {}]
        trigrams[a][connector][0] += 1 
        if not c in trigrams[a][connector][1]:
            trigrams[a][connector][1][c] = [0, 0, {}]
        trigrams[a][connector][1][c][0] += 1
        if not tag in trigrams[a][connector][1][c][2]:
            trigrams[a][connector][1][c][2][tag] = [token, 0, 0]
        trigrams[a][connector][1][c][2][tag][1] += 1

        if connector not in relationFreq:
            relationFreq[connector] = 1
        else:
            relationFreq[connector] += 1

        if not c in trigrams:
            trigrams[c] = {}
        if not connector+' of' in trigrams[c]:
            trigrams[c][connector+' of'] = [0, {}]
        trigrams[c][connector+' of'][0] += 1 
        if not a in trigrams[c][connector+' of'][1]:
            trigrams[c][connector+' of'][1][a] = [0, 0, {}]
        trigrams[c][connector+' of'][1][a][0] += 1
        if not tag in trigrams[c][connector+' of'][1][a][2]:
            trigrams[c][connector+' of'][1][a][2][tag] = [token, 0, 0]
        trigrams[c][connector+' of'][1][a][2][tag][1] += 1

        if connector+' of' not in relationFreq:
            relationFreq[connector+' of'] = 1
        else:
            relationFreq[connector+' of'] += 1

    elif u"союзн" in trigram["2"]["relation"]:

        token = trigram["3"]["token"]
        tag = trigram["3"]["tag"][0]

        if not a in trigrams:
            trigrams[a] = {}
        connector = trigram["2"]["lemma"]
        c = trigram["3"]["lemma"]
        if c.strip() == "%" or c.strip() == '--' or c.strip() == '...' or '\\' in c.strip() or c.strip() == '-':
            continue
        if c.strip() in hapax:
            continue

        if not connector in trigrams[a]:
            trigrams[a][connector] = [0, {}]
        trigrams[a][connector][0] += 1 
        if not c in trigrams[a][connector][1]:
            trigrams[a][connector][1][c] = [0, 0, {}]
        trigrams[a][connector][1][c][0] += 1

        if not tag in trigrams[a][connector][1][c][2]:
            trigrams[a][connector][1][c][2][tag] = [token, 0, 0]
        trigrams[a][connector][1][c][2][tag][1] += 1

        if connector not in relationFreq:
            relationFreq[connector] = 1
        else:
            relationFreq[connector] += 1

        if not c in trigrams:
            trigrams[c] = {}

        if not connector+' of' in trigrams[c]:
            trigrams[c][connector+' of'] = [0, {}]
        trigrams[c][connector+' of'][0] += 1 
        if not a in trigrams[c][connector+' of'][1]:
            trigrams[c][connector+' of'][1][a] = [0, 0, {}]
        trigrams[c][connector+' of'][1][a][0] += 1

        if not tag in trigrams[c][connector+' of'][1][a][2]:
            trigrams[c][connector+' of'][1][a][2][tag] = [token, 0, 0]
        trigrams[c][connector+' of'][1][a][2][tag][1] += 1

        if connector+' of' not in relationFreq:
            relationFreq[connector+' of'] = 1
        else:
            relationFreq[connector+' of'] += 1 

print >> sys.stderr, "Trigrams:", len(trigrams)

for word in trigrams:
    for relation in trigrams[word]:
        for lemma in trigrams[word][relation][1]:
            try:
                logLem = logDice(trigrams, word, relation, lemma, None)
            except:
                logLem = 0
            trigrams[word][relation][1][lemma][1] = logLem
            for tag in trigrams[word][relation][1][lemma][2]:
                try:
                    logTok = logDice(trigrams, word, relation, lemma, tag)
                except:
                    logTok = 0
                trigrams[word][relation][1][lemma][2][tag][2] = logTok

print >> sys.stderr, "Trigrams:", len(trigrams)

for word in trigrams:
    print word.encode('utf-8')+'\t'+json.dumps(trigrams[word],ensure_ascii = False).encode('utf-8')

#print json.dumps(trigrams,ensure_ascii = False).encode('utf-8')

w = open('relationFreq_tri.tsv', 'w')
for rel in relationFreq:
    s = rel+'\t'+str(relationFreq[rel])+'\n'
    w.write(s.encode('utf-8'))
w.close()
