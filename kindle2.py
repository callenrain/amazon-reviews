from collections import defaultdict
from math import log 
from operator import itemgetter
import string

def main():
	review_dict = getData()
	feature_list = getFeatures(review_dict)
	scores = []
	for i in range(len(feature_list)):
		for k in range(-1,0,1):
			f_present = 0.0
			f_other = 0.0
			for j in range(int(.2*(len(review_dict.items()))),len(review_dict.items())):
				if feature_list[i] in review_dict[j]['text']:
					if review_dict[j]['score'] == k:
						f_present += 1.0
					else:
						f_other += 1.0
				score = log((f_present + .1)/(f_other + .1))
			scores.append((feature_list[i],k,str(score)[:4]))
	sorted_scores = sorted(scores, key=itemgetter(2), reverse=True)
	print sorted_scores[:20]
	tagged_test_data = tagData(sorted_scores,review_dict)
	scoreData(tagged_test_data,review_dict)
	
def scoreData(tagged_test_data,review_dict):
	total_instances = 0.0 
	instances_correct = 0.0
	for i in range(int(.2*(len(review_dict.items())))):
		if review_dict[i]['score'] == tagged_test_data[i]:
			instances_correct += 1.0
		total_instances += 1.0
	print instances_correct/total_instances

	
def tagData(scores,review_dict):
	tags = defaultdict(lambda: 0)
	for i in range(int(.2*(len(review_dict.items())))):
		found = False
		for j in range(2000):
			declist_feature = scores[j][0]
			declist_score = scores[j][1]
			if declist_feature in review_dict[i]['text']:
				tags[i]=declist_score
				found = True
				break
		if found == False:
			tags[i]=0
	return tags	

	
def getFeatures(review_dict):
	feature_list = []
	review_list = review_dict.items()
	for i in range(int(.2*(len(review_list))),len(review_list)):
		features = review_list[i][1]['text'].split()
		for j in range(len(features)):
			f = features[j].lower()
			remove = set(string.punctuation)
			f = ''.join(char for char in f if char not in remove)
			if f not in feature_list:
				feature_list.append(features[j])
	return feature_list

	
def getData():
	infile = file("kindlereviews.txt",'r')
	lines = infile.readlines()
	d = defaultdict(lambda: 0)
	identifier = 0
	for i in range(len(lines)):
		split_lines = lines[i].split('"')
		split_lines = [word for word in split_lines if word != ',']
		if len(split_lines) == 10 and len(split_lines[8].split()) < 100:
			small_dict = defaultdict(lambda: 0)
			small_dict["num"] = split_lines[1]
			if split_lines[4] == '5.0':
				score = 1
			elif split_lines[4] == '4.0' or split_lines[4] == '3.0':
				score = 0
			elif split_lines[4] == '2.0' or split_lines[4] == '1.0':
				score = -1
			small_dict["score"] = score
			small_dict["text"] = split_lines[8]
			d[identifier]=small_dict
			identifier += 1
	return d	

	
if __name__=='__main__':
	"""d = getData()
	f = getFeatures(d)
	pos = 0
	neg = 0
	for i in range(len(d.items())):
		if d.items()[i][1]['score'] == 1:
			pos += 1
		else:
			neg += 1
	print pos, neg"""
	main()


