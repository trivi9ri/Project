import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
try:
        import cPickle as pickle
except:
        import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
import statistics 
from nltk.tokenize import word_tokenize

#15
class VoteClassifier(ClassifierI):
	def __init__(self, *classifiers):
		self._classifiers = classifiers


	def classify(self, features):
		votes = []
		for c in self._classifiers:
			v = c.classify(features)
			votes.append(v)
		return mode(votes)


	def confidence(self, features):
		votes = []
		for c in self._classifieres:
			v = c.classify(features)
			votes.append(v)


		choice_votes = votes.count(mode(votes))
		conf = choice_votes/len(votes)
		return conf

short_pos = open("C:/Users/Administrator/Downloads/positive.txt","r").read()
short_neg = open("C:/Users/Administrator/Downloads//negative.txt","r").read()


all_words = []
documents = []


allowed_word_types = ["J"]

#50
for p in short_pos.split('\n'):
	documents.append((p,"pos"))
	words = word_tokenize(p)
	pos = nltk.pos_tag(words)
	for w in pos:
		if w[1][0] in allowed_word_types:
			all_words.append(w[0].lower())

		
#60
	print ("short_posi"+p)
       
for p in short_neg.split('\n'):
	documents.append((p,"neg"))
	words = word_tokenize(p)
	pos = nltk.pos_tag(words)
	for w in pos:
		if w[1][0] in allowed_word_types:
			all_words.append(w[0].lower())
#70
	print ("short_nega"+p)
	
        

save_documents = open("C:/Users/Administrator/pickled_algos/documents.pickle","wb")
pickle.dump(documents, save_documents)
save_documents.close()

all_words = nltk.FreqDist(all_words)
#80
word_features = list(all_words.keys())[:5000]

save_word_features = open("C:/Users/Administrator/pickled_algos/word_features5k.pickle","wb")
pickle.dump(word_features, save_word_features)
save_word_features.close()


def find_features(document):
	words = word_tokenize(document)
	features = {}
	for w in word_features:
		features[w] = (w in words)
	return features

featuresets = [(find_features(rev), category) for (rev, category) in documents]

save_featuresets = open("C:/Users/Administrator/pickled_algos/featuresets.pickle","wb")
pickle.dump(featuresets, save_featuresets)
save_featuresets.close()
#100
random.shuffle(featuresets)
print(len(featuresets))

testing_set = featuresets[10000:]
training_set = featuresets[:10000]

classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier,testing_set))*100)
classifier.show_most_informative_features(15)
#110

save_classifier = open("C:/Users/Administrator/pickled_algos/originalnaivebayes5k.pickle","wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()

