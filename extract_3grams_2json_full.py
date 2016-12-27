#!/usr/local/python2.7/bin/python2.7
#coding: utf-8
import sys,json
conj = set(["S","C"])

sentence = {}

for line in sys.stdin:
    trigrams = {}
    res = line.split('\t')
    if len(res) == 1:
        for word in sentence:
            if sentence[word]['relation'] != 'ROOT' and sentence[word]['relation'] != 'PUNC' and sentence[word]['lemma'] != "--" and sentence[word]['lemma'] != '—' and len(sentence[word]['lemma']) > 0:
                if sentence[word]['host'] == "0":
                    continue
                if sentence[sentence[word]['host']]['host'] == "0":
                    continue
                #print sentence[word]['host'],sentence[sentence[word]['host']]['host']
                host2json = sentence[sentence[word]['host']]['lemma']
                host2json_token = sentence[sentence[word]['host']]['token']
                hyperhost2json = sentence[sentence[sentence[word]['host']]['host']]['lemma']
                hyperhost2json_token = sentence[sentence[sentence[word]['host']]['host']]['token']
                hyperhost2json_pos = sentence[sentence[sentence[word]['host']]['host']]['pos']
                hyperhost2json_relation = sentence[sentence[sentence[word]['host']]['host']]['relation']
                if hyperhost2json_pos in conj and hyperhost2json_relation == "ROOT":
                    print >> sys.stderr, hyperhost2json_token
                    continue
                relation2json = sentence[word]['relation']
                lemma2json = sentence[word]['lemma']
                token2json = sentence[word]['token']
                tag2json = sentence[word]['tag']
                hyperrelation2json = sentence[sentence[word]['host']]['relation']
                #print hyperhost2json,hyperrelation2json,host2json,relation2json,lemma2json
                trigrams[1] = {"lemma":hyperhost2json,"token":hyperhost2json_token,"relation":hyperrelation2json}
                trigrams[2] = {"lemma":host2json,"token":host2json_token,"relation":relation2json}
                trigrams[3] = {"lemma":lemma2json,"token":token2json, "tag": [tag2json, '']}
                print json.dumps(trigrams,ensure_ascii=False)
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
    sentence[number]['tag'] = tag.strip()
    sentence[number]['out'] = token+' '+lemma+' '+pos1

