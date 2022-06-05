import xml.etree.cElementTree as ET
import re
from collections import defaultdict, Counter
import matplotlib.pyplot as plt

xml_file = 'annot.opcorpora.xml'
corp_unkn = 'unkn.txt'
corp_amb = 'amb.txt'
corp_rep_sent = 'rep_sent.txt'

named_entities = set(['Name', 'Surn', 'Patr', 'Geox'])

tree = ET.ElementTree(file=xml_file)
root = tree.getroot()

unkn_list = []
amb_words = defaultdict(list)

repeated_sentences = defaultdict(int)
classes = defaultdict(int)
colors = ['aqua', 'aquamarine', 'yellow', 'orchid', 'black',
          'blue', 'brown', 'chartreuse', 'chocolate', 'coral',
          'crimson', 'cyan', 'darkblue', 'darkgreen', 'fuchsia',
          'gold', 'goldenrod', 'green', 'grey', 'indigo',
          'olive', 'khaki']

for text in root.iter('text'):
    for paragraphs in text.iter('paragraphs'):
        for paragraph in paragraphs.iter('paragraph'):
            for sentence in paragraph.iter('sentence'):
                repeated_sentences[sentence.find('source').text] += 1
                for tokens in sentence.iter('tokens'):
                    word_list = []
                    pos_ner_list = []
                    for token in tokens.iter('token'):
                        l = token.find('tfr').find('v').find('l')

                        if l.find('g').attrib['v'] == 'UNKN':
                            unkn_list.append(token.attrib['text'])
                            
                        if l.attrib['id'] != '0' or l.find('g').attrib['v'] == 'UNKN':
                            pos_ner = ''
                            for g in l.iter('g'):
                                pn = g.attrib['v']
                                if pn in named_entities:
                                    pos_ner = pn
                                    break
                            if not pos_ner:
                                pos_ner = l.find('g').attrib['v']

                            classes[pos_ner] += 1

                            amb_words[token.attrib['text'].lower()].append(pos_ner)

labels = []
sizes = []

for x, y in classes.items():
    labels.append(x)
    sizes.append(y)

# Plot
plt.pie(sizes, labels=labels, colors=colors, labeldistance=None)

plt.legend()
plt.axis('equal')
plt.show()

repeated_sentences = {k: v for k, v in repeated_sentences.items() if v > 1}
with open(corp_rep_sent, mode='w', encoding='utf-8') as crs:
    for k, v in repeated_sentences.items():
        crs.write(k)
        crs.write('\t')
        crs.write(str(v))
        crs.write('\n')


unkn_list = list(set(unkn_list))
unkn_list.sort()
with open(corp_unkn, mode='w', encoding='utf-8') as cu:
    for w in unkn_list:
        cu.write(w)
        cu.write('\n')

amb_words = dict((k, dict(Counter(v))) for k, v in amb_words.items() if len(set(v)) > 1)
with open(corp_amb, mode='w', encoding='utf-8') as aw:
    for w, p in amb_words.items():
        p_str = [k + '-' + str(v) for k, v in p.items()]
        aw.write(w)
        aw.write('\t')
        aw.write(','.join(p_str))
        aw.write('\n')
