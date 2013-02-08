import nltk
from collections import defaultdict
from math import log 
from operator import itemgetter
import string
import re
import itertools
from nltkbayes import *
import sys

def main():
	#commandline arguments: file, num_features, num_rules
	args = sys.argv
	file_path = args[1]
	num_features = int(args[2])
	num_rules = int(args[3])
	
	decList(file_path,num_features,num_rules)
		
def decList(file_path, num_features, num_rules):
	review_list = getData(file_path)
	train_list,test_list = review_list[len(review_list)/5:],review_list[:len(review_list)/5]
	features_list = nltk.FreqDist(w.lower() for [r,s] in train_list for w in r).keys()[:num_features]
	
	train_feature_sets = [(bag_of_words_features(text,features_list,False), score) for (text,score) in train_list]
	contains_features_list = ['contains(%s)' % word for word in features_list]
	
	scores = []
	for feature in contains_features_list:
		for k in range(2):
			f_present = 0.0
			f_other = 0.0
			for (vector,rating) in train_feature_sets:
				if vector[feature]:
					if rating == k:
						f_present += 1.0
					else:
						f_other += 1.0
			if k == 0:
				score = log((f_present + .01)/(f_other + .01))
			else:
				score = log((f_present + .01)/(f_other + .01))
			scores.append((feature,k,score))
	sorted_scores = sorted(scores, key=itemgetter(2), reverse=True)[:num_rules]
	#print ["%s %s /n" % (a,b) for (a,b,c) in sorted_scores[:20]]
	tagged_test_data = tagData(sorted_scores,test_list,features_list)
	scoreData(tagged_test_data,test_list)
	
def scoreData(tagged_test_data,test_list):
	total_instances = 0.0 
	instances_correct = 0.0
	for ((review,correct),guess) in itertools.izip(test_list,tagged_test_data):
		if correct == guess:
			instances_correct += 1.0
		total_instances += 1.0
	print instances_correct/total_instances

	
def tagData(scores,test_list,features_list):
	test_feature_sets = [(bag_of_words_features(text,features_list,False), score) for (text,score) in test_list]
	tags = []
	for (vector,rating) in test_feature_sets:
		found = False
		for (feature,k,score) in scores:
			if vector[feature]:
				tags.append(k)
				found = True
				break
		if found == False:
			tags.append(1)
	return tags	

	
if __name__=='__main__':
	#print getFeatures(['i', 'think', 'not', 'this', 'product', 'is', 'stupid'])
	main()


