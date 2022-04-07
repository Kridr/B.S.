import xml.etree.cElementTree as ET
import re

xml_file = 'annot.opcorpora.xml'
corp_cased = 'corp_cased.csv'

named_entities = set(['Name', 'Surn', 'Patr', 'Geox'])

tree = ET.ElementTree(file=xml_file)
root = tree.getroot()

with open(corp_cased, mode = 'w', encoding = 'utf-8') as cc:
    for text in root.iter('text'):
        for paragraphs in text.iter('paragraphs'):
            for paragraph in paragraphs.iter('paragraph'):
                for sentence in paragraph.iter('sentence'):
                    for tokens in sentence.iter('tokens'):
                        word_list = []
                        pos_ner_list = []
                        for token in tokens.iter('token'):
                            l = token.find('tfr').find('v').find('l')
                            if l.attrib['id'] != '0':
                                pos_ner = ''
                                for g in l.iter('g'):
                                    pn = g.attrib['v']
                                    if pn in named_entities:
                                        pos_ner = pn
                                        break
                                if not pos_ner:
                                    pos_ner = l.find('g').attrib['v']

                                word_list.append(token.attrib['text'])
                                pos_ner_list.append(pos_ner)

                        cc.write(' '.join(word_list))
                        cc.write(',')
                        cc.write(' '.join(pos_ner_list))
                        cc.write('\n')
