#!/usr/bin/python
import random
import nltk
import re
import itertools
from collections import defaultdict
from nltk import bigrams
import aspell
import sys

def main():
	#commandline arguments: not_words, number, sentences_len, bigrams, POS, spelling, num_features,file
	args = sys.argv
	not_wrds = args[1]
	number = args[2]
	sen_len = args[3]
	f_bigrams = args[4]
	pos = args[5]
	spelling = args[6]
	num_features = int(args[7])
	file_path = args[8]
	options = [not_wrds,number,sen_len,f_bigrams,pos,spelling,num_features]
	bayes(options,file_path)
	
def bayes(options,file_path):
	#print "Negation: "+not_wrds,"\nNumeric: "+number,"\nSentence Length: "+sen_len,"\nBigram: "+f_bigrams,"\nPOS: "+pos,"\nSpelling: "+spelling
	reviews = getData(file_path)
	train_set, test_set = reviews[len(reviews)/5:],reviews[:len(reviews)/5]
	feature_dicts = getFeatureDicts(reviews, options)
	train_dict, test_dict = feature_dicts[len(reviews)/5:],feature_dicts[:len(reviews)/5]
	
	naive_classifier = nltk.NaiveBayesClassifier.train(train_dict)
	print nltk.classify.accuracy(naive_classifier, test_dict)
	#naive_classifier.show_most_informative_features(50)
	#errors(test_set,naive_classifier)

def getFeatureDicts(reviews,options):
	feature_sets = []
	train_set = reviews[len(reviews)/5:]
	not_wrds,number,sen_len,f_bigrams,pos,spelling,num_features = options[0],options[1],options[2],options[3],options[4],options[5],options[6]
	all_words = nltk.FreqDist(w.lower() for [r,s] in train_set for w in r).keys()[:num_features]
	
	if pos == "True":
		new_words = []
		tagged = nltk.pos_tag(all_words)
		for (word,tag) in tagged:
			if tag == 'RB' or tag == 'JJ':
				new_words.append(word)
		pos_features = new_words
		feature_sets = [(posFeatures(text,pos_features,True), score) for (text,score) in reviews]
		return feature_sets
		
	if spelling == "True":
		feature_sets = [(bag_of_words_features(text,all_words,True), score) for (text,score) in reviews]
	elif spelling == "False":
		feature_sets = [(bag_of_words_features(text,all_words,False), score) for (text,score) in reviews]
	
	if not_wrds == 'True':
		feature_sets = not_words_features(feature_sets, reviews)
	
	if number == 'True':	
		feature_sets = has_number_feature(feature_sets, reviews)
		
	if sen_len == 'True':
		feature_sets = short_sentences(feature_sets, reviews)
	
	if f_bigrams == 'True':
		all_bigrams = nltk.FreqDist((bi,gram) for [text,score] in train_set for (bi,gram) in bigrams(text) if (bi != '.') and (gram != '.'))
		bigram_features_list = all_bigrams.keys()[:100]
		feature_sets = bigram_features(feature_sets, reviews, bigram_features_list)

	return feature_sets
	
def posFeatures(document,word_features,spell):
	features = {}
	document_words = set(document) 
	for word in word_features:
		features['adj/adv(%s)' % word] = (word in document)
	return features	
	
def errors(test_set,classifier):
	print len(test_set)
	error_list = []
	for (vector,score) in test_set:
		guess = classifier.classify(vector)
		if guess != score:
			error_list.append((score, guess, ' '.join(vector.keys())))
	#for (score, guess, article) in sorted(error_list):
		#print 'correct=%-8s guess=%-8s \n%-30s\n' % (score, guess, article)
	print len(error_list),"ERRORS"
	
def bag_of_words_features(document,word_features,spell):
	features = {}
	s = aspell.Speller('lang', 'en')
	if spell:
		for i in range(len(document)):
			if s.check(document[i]) == 0:
				if len(s.suggest(document[i])) > 0 and len(s.suggest(document[i])) < 15 and s.suggest(document[i])[0] in word_features:		
					document[i] = s.suggest(document[i])[0]
	document_words = set(document) 
	for word in word_features:
		features['contains(%s)' % word] = (word in document)
	return features

def bigram_features(feature_sets, review, bigram_list):
	for ((review_text,tag),(feature_set,tag)) in itertools.izip(review,feature_sets):
		for (bi,gram) in bigram_list:
			feature_set['bigram(%(word1)s %(word2)s)' % {"word1" : bi, "word2" : gram}] = ((bi,gram) in bigrams(review_text))
	return feature_sets

def not_words_features(feature_sets, review):
	not_distance = 3
	for ((review_text,tag),(feature_set,tag)) in itertools.izip(review,feature_sets):
		for i in range(len(review_text)-not_distance):
			if review_text[i] == 'not' or review_text[i] == 'doesn\'t' or review_text[i] == 'won\'t' or review_text[i] == 'no':
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
			if size > 20:
				feature_set['long_sentences'] = True
			elif size < 10:
				feature_set['short_sentences'] = True
		else:
			feature_set['no_periods'] = True
	return feature_sets

def getData(review_file):
	pos,full = 0,0
	infile = file(review_file,'r')
	lines = infile.readlines()
	review_list = []
	for i in range(len(lines)):
		split_lines = lines[i].split('"')
		split_lines = [word for word in split_lines if word != ',']
		if len(split_lines) == 10 and len(split_lines[8].split()) < 100 and split_lines[4] != '3.0' and split_lines[4] != '4.0':
			if split_lines[4] == '5.0' and float(pos)/float(full+1) < .5:
				pos += 1
				full += 1
				score = 1
				word_list = [w.lower() for w in re.findall(r'\w+\-\w+|\w+\'\w+|\.|\w+', split_lines[8])]
				review_list.append((word_list,score))
			elif split_lines[4] == '1.0' or split_lines[4] == '2.0':
				score = 0
				full += 1
				word_list = [w.lower() for w in re.findall(r'\w+\-\w+|\w+\'\w+|\.|\w+', split_lines[8])]
				review_list.append((word_list,score))
	#print "Random Baseline",float(pos)/float(full), pos, full
	return review_list
	
if __name__=='__main__':
	'''reviews = getData("/Users/callenrain/Documents/Programming/CS65Final/data/kindlereviews.txt")
	all_words = nltk.FreqDist(w.lower() for [r,s] in reviews for w in r)
	word_features = all_words.keys()[:2000]
	featuresets = [(bag_of_words_features(n,word_features), g) for (n,g) in reviews]
	print featuresets'''
	main()