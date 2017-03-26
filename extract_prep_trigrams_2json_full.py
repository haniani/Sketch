#!/usr/bin/python2
#coding: utf-8
import sys,json

prepsandconjs = set(["S","C"])
noms = set(["N","A","P"])

dictpartsspeech = open("dictpartsspeech.txt", 'w')
dictpartsspeech.write("{")

sentence = {}

for line in sys.stdin:
    trigrams = {}
    res = line.split('\t')
    if len(res) == 1:
        for word in sentence:
            if sentence[word]['relation'] != 'ROOT' and sentence[word]['relation'] != 'PUNC' and sentence[word]['lemma'] != "--" and sentence[word]['lemma'] != '—' and sentence[word]['lemma'] != '//' and len(sentence[word]['lemma']) > 0:
                if sentence[word]['host'] == "0":
                    continue
                if sentence[sentence[word]['host']]['host'] == "0":
                    continue
                host2json = sentence[sentence[word]['host']]['lemma']
                host2json_token = sentence[sentence[word]['host']]['token']
                host2json_pos = sentence[sentence[word]['host']]['pos']
                hyperhost2json = sentence[sentence[sentence[word]['host']]['host']]['lemma']
                hyperhost2json_token = sentence[sentence[sentence[word]['host']]['host']]['token']
                hyperhost2json_pos = sentence[sentence[sentence[word]['host']]['host']]['pos']
                hyperhost2json_relation = sentence[sentence[sentence[word]['host']]['host']]['relation']
                relation2json = sentence[word]['relation']
                lemma2json = sentence[word]['lemma']
                token2json = sentence[word]['token']
                pos2json = sentence[word]['pos']
                tag2json = sentence[word]['tag']
                hyperrelation2json = sentence[sentence[word]['host']]['relation']

                if host2json_pos in prepsandconjs and pos2json in noms:
                    if hyperhost2json_pos in prepsandconjs:
                        #print >> sys.stderr, hyperhost2json
                        continue
                    if hyperhost2json_relation == 'PUNC' or hyperhost2json == "--" or hyperhost2json == '—' or hyperhost2json == '//' or len(hyperhost2json) < 1:
                        #print >> sys.stderr, hyperhost2json
                        continue
                    if "союзн" in relation2json or "предл" in relation2json:
                        if pos2json == "N":
                            case2json = sentence[word]['tag'][4]
                        else:
                            case2json = sentence[word]['tag'][5]
                    trigrams[1] = {"lemma":hyperhost2json,"token":hyperhost2json_token,"relation":hyperrelation2json}
                    trigrams[2] = {"lemma":host2json,"token":host2json_token,"relation":relation2json}
                    trigrams[3] = {"lemma":lemma2json,"token":token2json,"tag":[tag2json, case2json]}
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
    sentence[number]['tag'] = tag.strip()
    sentence[number]['token'] = token.strip()
    sentence[number]['host'] = host.strip()
    sentence[number]['relation'] = relation.strip()
    sentence[number]['pos'] = pos1
    sentence[number]['out'] = token+' '+lemma+' '+pos1

    lemma_tri = str(sentence[number]['lemma'])

    dictpartsspeech.write(str(sentence[number]['lemma']) + ":" + pos1 + "\n")


dictpartsspeech.write("}")
