python naivebayes.py False False False False False False 500 'allbooks.txt' #negation
python naivebayes.py True False False False False False 500 'allbooks.txt' #negation
python naivebayes.py False True False False False False 500 'allbooks.txt' #numeric
python naivebayes.py False False True False False False 500 'allbooks.txt' #sentence length
python naivebayes.py False False False True False False 500 'allbooks.txt' #bigrams
python naivebayes.py False False False False True False 500 'allbooks.txt' #pos
python naivebayes.py False False False False False True 500 'allbooks.txt' #spelling

python naivebayes.py False False False False False False 500 'allmedia.txt' #negation
python naivebayes.py True False False False False False 500 'allmedia.txt' #negation
python naivebayes.py False True False False False False 500 'allmedia.txt' #numeric
python naivebayes.py False False True False False False 500 'allmedia.txt' #sentence length
python naivebayes.py False False False True False False 500 'allmedia.txt' #bigrams
python naivebayes.py False False False False True False 500 'allmedia.txt' #pos
python naivebayes.py False False False False False True 500 'allmedia.txt' #spelling

python naivebayes.py False False False False False False 500 'kindlereviews.txt' #negation
python naivebayes.py True False False False False False 500 'kindlereviews.txt' #negation
python naivebayes.py False True False False False False 500 'kindlereviews.txt' #numeric
python naivebayes.py False False True False False False 500 'kindlereviews.txt' #sentence length
python naivebayes.py False False False True False False 500 'kindlereviews.txt' #bigrams
python naivebayes.py False False False False True False 500 'kindlereviews.txt' #pos
python naivebayes.py False False False False False True 500 'kindlereviews.txt' #spelling

python naivebayes.py False True False True False False 500 'allbooks.txt' #negation+sen_len
python naivebayes.py False True False True False False 500 'allmedia.txt' #negation+sen_len
python naivebayes.py False True False True False False 500 'kindlereviews.txt' #negation+sen_len





