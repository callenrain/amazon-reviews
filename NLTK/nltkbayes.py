import nltk
import re
import itertools
from collections import defaultdict
from nltk import bigrams

def main():
	featuresets = {}
	file_path = "kindlereviews.txt"
	review = getData(file_path)
	all_words = nltk.FreqDist(w.lower() for [r,s] in review for w in r)
	#all_bigrams = nltk.FreqDist((bi,gram) for [text,score] in review for (bi,gram) in bigrams(text) if (bi != '.') and (gram != '.'))
	#bigram_features_list = all_bigrams.keys()[:500]
	word_features = all_words.keys()[:100]
	featuresets = [(bag_of_words_features(n,word_features), g) for (n,g) in review]
	#featuresets = not_words_features(featuresets, review)
	#featuresets = has_number_feature(featuresets, review)
	#featuresets = short_sentences(featuresets, review)
	#featuresets = bigram_features(featuresets, review, bigram_features_list)
	
	train_set, test_set = featuresets[len(review)/5:],featuresets[:len(review)/5]
	
	#naive_classifier = nltk.NaiveBayesClassifier.train(train_set)
	#decision_classifier = nltk.DecisionTreeClassifier.train(train_set)
	maxent_classifier = nltk.MaxentClassifier.train(train_set,max_iter=10)
	
	#print nltk.classify.accuracy(naive_classifier, test_set)
	#print nltk.classify.accuracy(decision_classifier, test_set)
	print nltk.classify.accuracy(maxent_classifier, test_set)
	
	#naive_classifier.show_most_informative_features(50)
	#print decision_classifier.pseudocode()
	#show_errors(word_features,test_set,review,naive_classifier)
	
def show_errors(word_features,test_set,review,classifier):
	errors = []
	for ((article,tag),(text,score)) in itertools.izip(test_set,review):
		guess = classifier.classify(bag_of_words_features(article,word_features))
		if guess != tag:
			errors.append((tag, guess, ' '.join(text)))
	for (tag, guess, article) in sorted(errors):
		print 'correct=%-8s guess=%-8s \n%-30s\n' % (tag, guess, article)
	
def bag_of_words_features(document,word_features):
    document_words = set(document) 
    features = {}
    for word in word_features:
		if word in document_words:
			features['contains(%s)' % word] = 1
		else:
			features['contains(%s)' % word] = 0
    return features

def bigram_features(feature_sets, review, bigram_list):
	for ((review_text,tag),(feature_set,tag)) in itertools.izip(review,feature_sets):
		for (bi,gram) in bigram_list:
			feature_set['bigram(%(word1)s %(word2)s)' % {"word1" : bi, "word2" : gram}] = ((bi,gram) in bigrams(review_text))
	return feature_sets

def not_words_features(feature_sets, review):
	not_distance = 3
	for ((review_text,tag),(feature_set,tag)) in itertools.izip(review,feature_sets):
		for i in range(len(review_text)):
			if i < len(review_text)-not_distance:
				if review_text[i] == 'not' or review_text[i] == 'doesn\'t' or review_text[i] == 'won\'t':
					for j in range(1,not_distance+1):
						feature_set['contains(NOT %s)' % review_text[i+j]] = True
						feature_set['contains(%s)' % review_text[i+j]] = False
	return feature_sets
	
def has_number_feature(feature_sets, review):
	for ((review_text,tag),(feature_set,tag)) in itertools.izip(review,feature_sets):
		for w in review_text:
			if re.search(r'\d',w):
				feature_set['numeric'] = True
	return feature_sets
	
def short_sentences(feature_sets, review):
	d = defaultdict(int)
	for ((review_text,tag),(feature_set,tag)) in itertools.izip(review,feature_sets):
		period = 0
		for w in review_text:
			if w == '.':
				period += 1
		if period > 0:
			size = int(str(len(review_text)/period))
			if size > 15:
				feature_set['long_sentences'] = True
			elif size < 10:
				feature_set['short_sentences'] = True
		else:
			feature_set['no_periods'] = True
	return feature_sets

def getData(review_file):
	pos, neg, neut = 0 , 0, 0
	infile = file(review_file,'r')
	lines = infile.readlines()
	review_list = []
	for i in range(len(lines)):
		split_lines = lines[i].split('"')
		split_lines = [word for word in split_lines if word != ',']
		if len(split_lines) == 10 and len(split_lines[8].split()) < 100 and split_lines[4] != '3.0' and split_lines[4] != '4.0':
			if split_lines[4] == '5.0':
				score = 1
			elif split_lines[4] == '1.0' or split_lines[4] == '2.0':
				score = 0
			word_list = [w.lower() for w in re.findall(r'\w+\-\w+|\w+\'\w+|\.|\w+', split_lines[8])]
			review_list.append([word_list,score])
	return review_list
	
if __name__=='__main__':
	'''reviews = getData("/Users/callenrain/Documents/Programming/CS65Final/data/kindlereviews.txt")
	all_words = nltk.FreqDist(w.lower() for [r,s] in reviews for w in r)
	word_features = all_words.keys()[:2000]
	featuresets = [(bag_of_words_features(n,word_features), g) for (n,g) in reviews]
	print featuresets'''
	main()