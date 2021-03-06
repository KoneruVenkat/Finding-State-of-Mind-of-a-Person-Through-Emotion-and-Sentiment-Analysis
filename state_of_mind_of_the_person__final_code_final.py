# -*- coding: utf-8 -*-
"""Copy_of_state_of_mind_of_the_person__final_code_FINAL.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uz5ZQR5U8KcWXgx3hVpteDVpP-ZBI0wQ
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import warnings

data=pd.read_csv("finalSentimentdata2.csv")

data

print(data.shape)

data.isnull().any()

from sklearn.feature_extraction.text import CountVectorizer


cv = CountVectorizer(stop_words = 'english')
words = cv.fit_transform(data.text)

sum_words = words.sum(axis=0)

words_freq = [(word, sum_words[0, i]) for word, i in cv.vocabulary_.items()]
words_freq = sorted(words_freq, key = lambda x: x[1], reverse = True)

frequency = pd.DataFrame(words_freq, columns=['word', 'freq'])

frequency.head(30).plot(x='word', y='freq', kind='bar', figsize=(15, 7), color = 'blue')
plt.title("Most Frequently Occuring Words - Top 30")

from wordcloud import WordCloud

wordcloud = WordCloud(background_color = 'white', width = 1000, height = 1000).generate_from_frequencies(dict(words_freq))

plt.figure(figsize=(10,8))
plt.imshow(wordcloud)
plt.title("WordCloud - Vocabulary from Reviews", fontsize = 22)

import re
import nltk

nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(max_features = 2500)
x = cv.fit_transform(data).toarray()
y = data.iloc[:, 1]

print(x.shape)
print(y.shape)

# adding a column to represent the length of the tweet

data['len'] = data['text'].str.len()


data.head(10)

# tokenizing the words present in the training set
tokenized_text = data['text'].apply(lambda x: x.split()) 

# importing gensim
import gensim

# creating a word to vector model
model_w2v = gensim.models.Word2Vec(
            tokenized_text,
            size=200, # desired no. of features/independent variables 
            window=5, # context window size
            min_count=2,
            sg = 1, # 1 for skip-gram model
            hs = 0,
            negative = 10, # for negative sampling
            workers= 2, # no.of cores
            seed = 34)

model_w2v.train(tokenized_text, total_examples= len(data['text']), epochs=20)

model_w2v.wv.most_similar(positive = "happy")

model_w2v.wv.most_similar(positive = "sad")

from tqdm import tqdm
tqdm.pandas(desc="progress-bar")
from gensim.models.doc2vec import LabeledSentence

def add_label(txt):
    output = []
    for i, s in zip(txt.index, txt):
        output.append(LabeledSentence(s, ["textt_" + str(i)]))
    return output

# label all the tweets
labeled_texts = add_label(tokenized_text)

labeled_texts[:6]

# removing unwanted patterns from the data

import re
import nltk

nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

train_corpus = []

for i in range(0, 3090):
  review = re.sub('[^a-zA-Z]', ' ', data['text'][i])
  review = review.lower()
  review = review.split()
  
  ps = PorterStemmer()
  
  # stemming
  review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
  
  # joining them back with space
  review = ' '.join(review)
  train_corpus.append(review)

# creating bag of words

from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(max_features = 2500)
x = cv.fit_transform(train_corpus).toarray()
y = data.iloc[:, 1]

print(x.shape)
print(y.shape)

# splitting the training data into train and valid sets

from sklearn.model_selection import train_test_split

x_train, x_valid, y_train, y_valid = train_test_split(x, y, test_size = 0.20, random_state = 42)

print(x_train.shape)
print(x_valid.shape)
print(y_train.shape)
print(y_valid.shape)

# standardization

from sklearn.preprocessing import StandardScaler

sc = StandardScaler()

x_train = sc.fit_transform(x_train)
x_valid = sc.transform(x_valid)

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score

model = RandomForestClassifier()
model.fit(x_train, y_train)

y_pred = model.predict(x_valid)

print("Training Accuracy :", model.score(x_train, y_train))
print("Validation Accuracy :", model.score(x_valid, y_valid))

# confusion matrix
cm = confusion_matrix(y_valid, y_pred)
print(cm)

f1_score(y_valid,y_pred, average='macro')

from statistics import mean, stdev
from sklearn import preprocessing
from sklearn.model_selection import StratifiedKFold
from sklearn import linear_model
from sklearn import datasets

kf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

cnt = 1
# split()  method generate indices to split data into training and test set.
for train_index, test_index in kf.split(x, y):
    print(f'Fold:{cnt}, Train set: {len(train_index)}, Test set:{len(test_index)}')
    cnt+=1

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.model_selection import cross_val_score


score = cross_val_score(RandomForestClassifier(random_state= 42), x, y, cv= kf, scoring="accuracy")
print(f'Scores for each fold are: {score}')
print(f'Average score: {"{:.2f}".format(score.mean())}')

n_estimators = [50, 100, 150, 200, 250, 300, 350]

for val in n_estimators:
    score = cross_val_score(RandomForestClassifier(n_estimators= val, random_state= 42), x, y, cv= kf, scoring="accuracy")
    print(f'Average score({val}): {"{:.3f}".format(score.mean())}')

from sklearn.metrics import accuracy_score
accuracy_score(y_valid,y_pred)*100

from xgboost import XGBClassifier

model = XGBClassifier()
model.fit(x_train, y_train)

y_pred = model.predict(x_valid)

print("Training Accuracy :", model.score(x_train, y_train))
print("Validation Accuracy :", model.score(x_valid, y_valid))



# confusion matrix
cm = confusion_matrix(y_valid, y_pred)
print(cm)

from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(x_train, y_train)

y_pred = model.predict(x_valid)

print("Training Accuracy :", model.score(x_train, y_train))
print("Validation Accuracy :", model.score(x_valid, y_valid))



# confusion matrix
cm = confusion_matrix(y_valid, y_pred)
print(cm)

# create model
model = LogisticRegression()
# evaluate model
scores = cross_val_score(model, x, y, scoring='accuracy', cv=kf, n_jobs=-1)
# report performance
print('Accuracy: %.3f ' % (mean(scores)))

from sklearn.svm import SVC

model = SVC()
model.fit(x_train, y_train)

y_pred = model.predict(x_valid)

print("Training Accuracy :", model.score(x_train, y_train))
print("Validation Accuracy :", model.score(x_valid, y_valid))


# confusion matrix
cm = confusion_matrix(y_valid, y_pred)
print(cm)

from sklearn.tree import DecisionTreeClassifier
score = cross_val_score(DecisionTreeClassifier(random_state= 42), x, y, cv= kf, scoring="accuracy")
print(f'Scores for each fold are: {score}')
print(f'Average score: {"{:.2f}".format(score.mean())}')

from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier()
model.fit(x_train, y_train)

y_pred = model.predict(x_valid)

print("Training Accuracy :", model.score(x_train, y_train))
print("Validation Accuracy :", model.score(x_valid, y_valid))


# confusion matrix
cm = confusion_matrix(y_valid, y_pred)
print(cm)

score = cross_val_score(DecisionTreeClassifier(random_state= 42), x, y, cv= kf, scoring="accuracy")
print(f'Scores for each fold are: {score}')
print(f'Average score: {"{:.2f}".format(score.mean())}')

max_depth = [1,2,3,4,5,6,7,8,9,10]

for val in max_depth:
    score = cross_val_score(DecisionTreeClassifier(max_depth= val, random_state= 42), x, y, cv= kf, scoring="accuracy")
    print(f'Average score({val}): {"{:.3f}".format(score.mean())}')

from sklearn.ensemble import GradientBoostingRegressor

alg= GradientBoostingRegressor(n_estimators= 550, learning_rate= 0.1, max_depth= 3)
alg.fit(x_train,y_train)

"""APPLYING PCA 

"""

from sklearn.preprocessing import StandardScaler

sc = StandardScaler()

x_train = sc.fit_transform(x_train)
x_valid = sc.transform(x_valid)

from sklearn.decomposition import PCA


pca = PCA(n_components = 3)
x_train = pca.fit_transform(x_train)
x_valid = pca.fit_transform(x_valid)

"""OneVsRestClassifier"""

from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix

clf = OneVsRestClassifier(SVC()).fit(x_train, y_train)
y_pred = clf.predict(x_train)

print("Training Accuracy :", clf.score(x_train, y_train))
print("Validation Accuracy :", clf.score(x_valid, y_valid))
#print("Validation Accuracy :", clf.score(x_valid, y_valid))

# confusion matrix
cm = confusion_matrix(y_train, y_pred)
print(cm)

print("Validation Accuracy :", clf.score(x_valid, y_valid))

y_pred1 = clf.predict(x_valid)
cm = confusion_matrix(y_valid, y_pred1)
print(cm)

from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from matplotlib import pyplot

x, y = make_classification(n_samples=1000, n_classes=2, random_state=1)

trainx, testx, trainy, testy = train_test_split(x, y, test_size=0.5, random_state=2)

ns_probs = [0 for _ in range(len(testy))]

model = DecisionTreeClassifier()
model.fit(trainx, trainy)

ypred = model.predict(testx)

print("Training Accuracy :", model.score(trainx, trainy))
print("Validation Accuracy :", model.score(testx, testy))


# confusion matrix
cm = confusion_matrix(testy, ypred)
print(cm)

model = RandomForestClassifier()
model.fit(trainx, trainy)

ypred = model.predict(testx)

print("Training Accuracy :", model.score(trainx, trainy))
print("Validation Accuracy :", model.score(testx, testy))


# confusion matrix
cm = confusion_matrix(testy, ypred)
print(cm)

lr_probs = model.predict_proba(testx)

lr_probs = lr_probs[:, 1]

ns_auc = roc_auc_score(testy, ns_probs)
lr_auc = roc_auc_score(testy, lr_probs)

print('No Skill: ROC AUC=%.3f' % (ns_auc))
print('Logistic: ROC AUC=%.3f' % (lr_auc))

ns_fpr, ns_tpr, _ = roc_curve(testy, ns_probs)
lr_fpr, lr_tpr, _ = roc_curve(testy, lr_probs)

pyplot.plot(ns_fpr, ns_tpr, linestyle='--', label='No Skill')
pyplot.plot(lr_fpr, lr_tpr, marker='.', label='Logistic')

pyplot.plot(ns_fpr, ns_tpr, linestyle='--', label='No Skill')
pyplot.plot(lr_fpr, lr_tpr, marker='.', label='Logistic')
# axis labels
pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')
# show the legend
pyplot.legend()
# show the plot
pyplot.show()

np.histogram(data)
pyplot.show()