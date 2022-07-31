# BS
This repo represents my graduate work (MPEI, Bachelor of Science)

I researched POS-tagging and NER problem at the same time for russian language.\
Hence, tokens in my task can relate to either part of speech tag or named entity tag.

## Data
I prepared dataset from open data. Credit http://opencorpora.org \
In order to get essential data I prepared CSV-file from XML-file extracting fields that I need.\
During researching of Opencorpora data I found out that it is not ideal:
1. lots of tokens with unknown tag
2. Repeated sentences
3. Wrong tags for some tokens
So I think it is better to try out new datasets. For example, SynTagRus 

## Approaches
I used two different methods for this problem:
1. WordVec + Embedding layer
2. BERT (with two different pretrained models: multilingual and russian)

Also, I used two different representation of sentences: classification-like and direct (sequence2sequence).\
Classification approach: We take some word with its context. I used neighbour tokens for my context.\
Example: «Сущность диалектического противоречия»:
1. [0, Сущность, диалектического] → NOUN;
2. [Сущность, диалектического, противоречия] → ADJF; 
3. [диалектического, противоречия, 0] → NOUN.

I've created 3 models:
1. WordVec + Embedding + Classification-like
2. BERT + Classification-like
3. BERT + Sequence2Sequence

## Reduction of vocabulary size
For the first model I researched 4 ways to reduce vocabulary size:
1. Lemmatization
2. Stemming
3. SentencePiece
4. BertTokenizer (DeepPavlov)

Also, there was another option: no reduction at all.\
The best option according to metrics and overall size was `lemmatization`.

## Evaluating of models
Because of considerable disbalance of classes I used precision, recall and F1 scores (weighted average) for evaluating of created models.

The best model according to metrics was BERT with russian pretrained model and classification-like representation of sentence:
| precision | recall | f1  |
| :-------: | :----: | :-: |
| 0.95 | 0.94 | 0.95 |

But that model have trained for a lot of time (4-5 hours on Collab), so we also need to choose the best model for real-world applications.\
And such model is Word2Vec + Embedding + Classification-like representation of sentences.
| precision | recall | f1  |
| :-------: | :----: | :-: |
| 0.93 | 0.93 | 0.94 |

## Comparison with existing solution
A contester of my model is Textovod service (https://textovod.com/members_proposal).\
I chose 15 random sentences, then obtained tags using my best model for real-world application and using textovod. \
Look at the results in the table:

| Attempt | Textovod  | Word2Vec model |
| :-----: | :-------: | :------------: |
| Wrong tags | 6 | 2 | 
| Time | ~16s | 0.25s |

You can see that my model work better than textovod service. And my model is also free to use!

