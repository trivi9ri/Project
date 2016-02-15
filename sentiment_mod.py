#code: pythonprogramming.net/twitter-sentiment-analysis-nltk-tutorial/
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
from statistics import mode
from nltk.tokenize import word_tokenize


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
		for c in self._classifiers:
			v = c.classify(features)
			votes.append(v)

		choice_votes = votes.count(mode(votes))
		conf = choice_votes/len(votes)
		return conf


documents_f = open("/home/pi/Desktop/pickled_algos/documents.pickle","rb")
documents = pickle.load(documents_f)
documents_f.close()

word_features5k_f = open("/home/pi/Desktop/pickled_algos/word_features5k.pickle","rb")
word_features = pickle.load(word_features5k_f)
word_features5k_f.close()

def find_features(document):
	words = word_tokenize(document)
	features = {}
	for w in word_features:
		features[w] = (w in words)
	return features

open_file = open("/home/pi/Desktop/pickled_algos/originalnaivebayes5k.pickle","rb")
classifier = pickle.load(open_file)
open_file.close()


voted_classifier = VoteClassifier(classifier, classifier,classifier, classifier, classifier)

def sentiment(text):
	feats = find_features(text)
	return voted_classifier.classify(feats), voted_classifier.confidence(feats)

