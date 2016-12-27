#!/usr/bin/python2.7
#coding: utf-8
import sys,json,gzip,codecs

bigrams_file = sys.argv[1]

trigrams_file = sys.argv[2]

bigrams = json.loads(codecs.open(bigrams_file,'r','utf-8').read())
print >> sys.stderr, bigrams_file,'loaded'
trigrams = json.loads(codecs.open(trigrams_file,'r','utf-8').read())
print >> sys.stderr, trigrams_file,'loaded'

#print json.dumps(bigrams[u"в"],ensure_ascii = False).encode('utf-8')
#exit()


for entry in trigrams:
    if entry in bigrams:
        bigrams[entry].update(trigrams[entry])
    else:
        bigrams[entry] = trigrams[entry]


print json.dumps(bigrams,ensure_ascii = False).encode('utf-8')