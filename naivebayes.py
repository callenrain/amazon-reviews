from kindle import *
import string

def main():
	"""""fire",naiveBayes("kindlereviews.txt","firereviews.txt")
	"nook",naiveBayes("kindlereviews.txt","nookreviews.txt")
	"mbook",naiveBayes("kindlereviews.txt","macbookreviews.txt")
	"taylor",naiveBayes("kindlereviews.txt","taylorreviews.txt")
	"levi",naiveBayes("kindlereviews.txt","levireviews.txt")
	"lincoln",naiveBayes("kindlereviews.txt","lincolnreviews.txt")"""
	naiveBayes("last80kindlereviews.txt","first20kindlereviews.txt")
def naiveBayes(review,test):
	neg_feature_count = 0.0
	pos_feature_count = 0.0
	total_pos = 0.0
	total_neg = 0.0
	test_dict = getData(test)
	review_dict = getData(review)
	feature_list = getFeatures(review_dict)
	feature_counts = defaultdict(lambda: 0)
	for i in range(len(feature_list)):
		#for j in range(int(.2*(len(review_dict.items()))),len(review_dict.items())):
		for j in range(len(review_dict.items())):
			if review_dict[j]['score'] == 1:
				total_pos += 1.0
			else: 
				total_neg += 1.0
			review_dict[j]['score']
			if feature_list[i] in review_dict[j]['text']:
				if review_dict[j]['score'] == 0:
					feature_counts[(feature_list[i],0)] += 1.0
					neg_feature_count += 1.0
				else:
					feature_counts[(feature_list[i],1)] += 1.0
					pos_feature_count += 1.0
	counts = (neg_feature_count,pos_feature_count,total_pos,total_neg)
	tagged_test_data = computeAndTag(counts,test_dict,feature_counts)
	scoreData(tagged_test_data,test_dict)	

def computeAndTag(counts,review_dict,feature_counts):
	neg_feature_count = counts[0]
	pos_feature_count = counts[1]
	total_pos = counts[2]
	total_neg = counts[3]
	tags = defaultdict(lambda: 0)
	for i in range(int(.2*(len(review_dict.items())))):
		review_list = review_dict[i]['text'].split()
		pos_prob = (total_pos)/(total_neg+total_pos)
		neg_prob = (total_neg)/(total_neg+total_pos)
		for j in range(len(review_list)):
			word = review_list[j].lower()
			if word[len(word)-1] == ',' or word[len(word)-1] == '.':
				word = word[:len(word)-1]
			if review_list[j][0].isalpha():
				pos_prob *= (feature_counts[(word,1)]+.001)/(pos_feature_count+.001)
				neg_prob *= (feature_counts[(word,0)]+.001)/(neg_feature_count+.001)
		if pos_prob < neg_prob:
			tags[i] = 0
		else:
			tags[i] = 1
	return tags

def scoreData(tagged_test_data,review_dict):
	total_instances = 0.0 
	instances_correct = 0.0
	for i in range(int(.2*(len(review_dict.items())))):
		if review_dict[i]['score'] == tagged_test_data[i]:
			instances_correct += 1.0
		total_instances += 1.0
	print instances_correct/total_instances
	
main()