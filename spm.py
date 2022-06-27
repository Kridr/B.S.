import sentencepiece as spm
t_prm = '--input=sent.txt --model_prefix=sent --vocab_size=30000'
spm.SentencePieceTrainer.train(t_prm)
