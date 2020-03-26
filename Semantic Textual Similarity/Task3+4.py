
# coding: utf-8

# In[1]:


import spacy
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import wordnet
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import numpy as np
import csv


# In[2]:


#Jaccard Similarity Measure of two sets of words
def jaccard_similarity(sent1, sent2):
    if(len(sent1) == 0 and len(sent2)==0):
        return 0
    intersection1 = set(sent1).intersection(set(sent2))
    union1 = set(sent1).union(set(sent2))
    return (len(intersection1)/len(union1))


# In[3]:


#Cosine Similarity Measure for two vectors
def cosine_similarity(vector1, vector2):
    dot_product = sum(p*q for p,q in zip(vector1, vector2))
    magnitude = math.sqrt(sum([val**2 for val in vector1])) * math.sqrt(sum([val**2 for val in vector2]))
    if not magnitude:
        print(0)
    return (dot_product/magnitude)


# In[ ]:


#returns a set of words that are closely associated with each of the wordsof the sentence
def enrich(sentence):
    enriched = []
    for token in sentence:   
        enriched.append(token.text)
        for syn in wordnet.synsets(token.text):
            for h in syn.hypernyms():
                for lemma in h.lemmas():
                    enriched.append(lemma.name())
            for h in syn.hyponyms():
                for lemma in h.lemmas():
                    enriched.append(lemma.name())
            for s in syn.lemmas():
                enriched.append(s.name())
    return enriched    


# In[32]:


#Corpus Reader to read the training data from train-set.txt 
    nlp = spacy.load('en_core_web_sm')
    data = []
    with open ("C:\\Users\\Sukruti\\Desktop\\data(1)\\data\\train-set.txt",'r',encoding='utf8') as file:
        lines = file.readlines()
        for line in lines:
            newLine = []
            lineArray = line.split("\t")
            newLine.append(lineArray[1])
            newLine.append(lineArray[2])
            newLine.append(lineArray[3])
            data.append(newLine)
 
    #Separates the label data from the main data
    
    Y = [] 
    for i in range(1, len(data)):
        Y.append(int(data[i][2]))

    Xt = np.zeros((len(data)-1,2))

    #Translating the sentences into a feature vector having Jaccard and Cosine Similarity as its features
    for i in range(0, len(data)-1):
        stop_words = set(stopwords.words('english')) 
        sent1 = data[i+1][0]
        sent2 = data[i+1][1]
        sents11 = nlp(sent1)
        sents12 = nlp(sent2)
        
        sentence1 = enrich(sents11)
        sentence2 = enrich(sents12)

        tfidfVec = TfidfVectorizer(norm='l2',min_df=0, use_idf=True, smooth_idf=False, sublinear_tf=True)
        VecRep = tfidfVec.fit_transform([' '.join(set(sentence1)), ' '.join(set(sentence2))])
        array = VecRep.toarray() 
        
        Xt[i][0] = float(jaccard_similarity(sentence1, sentence2))
        Xt[i][1] = float(cosine_similarity(array[0], array[1]))


# In[33]:


from sklearn.ensemble import BaggingClassifier
from sklearn.svm import SVC

bagModel = BaggingClassifier(base_estimator=SVC(),n_estimators=10, random_state=0).fit(Xt, Y)


# In[36]:


nlp = spacy.load('en_core_web_sm')
data = []
with open ("C:\\Users\\Sukruti\\Desktop\\data(1)\\data\\dev-set.txt",'r',encoding='utf8') as file:
    lines = file.readlines()
    for line in lines:
        newLine = []
        lineArray = line.split("\t")
        newLine.append(lineArray[0])
        newLine.append(lineArray[1])
        newLine.append(lineArray[2])
        newLine.append(lineArray[3])
        data.append(newLine)
 
#Separates the label data from the main data

Ydev = [] 
header = []
header.append(data[0][0])
header.append(data[0][1])
header.append(data[0][2])
header.append(data[0][3])
devids = []
for i in range(1, len(data)):
    Ydev.append(int(data[i][3]))

Xdev = np.zeros((len(data)-1,2))

#Translating the sentences into a feature vector having Jaccard and Cosine Similarity as its features
for i in range(0, len(data)-1):
    devids.append(data[i+1][0])
    sent1 = data[i+1][0]
    sent2 = data[i+1][1]
    sents11 = nlp(sent1)
    sents12 = nlp(sent2)
    
    sentence1 = enrich(sents11)
    sentence2 = enrich(sents12)

    tfidfVec = TfidfVectorizer(norm='l2',min_df=0, use_idf=True, smooth_idf=False, sublinear_tf=True)
    VecRep = tfidfVec.fit_transform([' '.join(set(sentence1)), ' '.join(set(sentence2))])
    array = VecRep.toarray() 
    
    Xdev[i][0] = float(jaccard_similarity(sentence1, sentence2))
    Xdev[i][1] = float(cosine_similarity(array[0], array[1]))


# In[37]:


#predict labels for dev
pred_labels = bagModel.predict(Xdev)


# In[38]:


pred_file = []
newHeader = []
newHeader.append(header[0])
newHeader.append(header[3][:-1])
pred_file.append(newHeader)
for i in range(len(pred_labels)):
    newLine=[]
    newLine.append(devids[i])
    newLine.append(pred_labels[i])
    pred_file.append(newLine)


# In[39]:


import csv
with open('C:\\Users\\Sukruti\\Desktop\\dev-set-predicted-answers.txt', mode='w', newline='\n') as writeFile:
    writeFile = csv.writer(writeFile, delimiter='\t')
    for i in range(len(pred_file)):
        writeFile.writerow(pred_file[i])


# In[75]:


nlp = spacy.load('en_core_web_sm')
data = []
with open ("C:\\Users\\Sukruti\\Desktop\\data(1)\\data\\test-set.txt",'r',encoding='utf8') as file:
    lines = file.readlines()
    for line in lines:
        newLine = []
        lineArray = line.split("\t")
        newLine.append(lineArray[0])
        newLine.append(lineArray[1])
        newLine.append(lineArray[2])
        data.append(newLine)

testids = []

Xtest = np.zeros((len(data)-1,2))

#Translating the sentences into a feature vector having Jaccard and Cosine Similarity as its features
for i in range(0, len(data)-1):
    testids.append(data[i+1][0])
    sent1 = data[i+1][0]
    sent2 = data[i+1][1]
    sents11 = nlp(sent1)
    sents12 = nlp(sent2)
    
    sentence1 = enrich(sents11)
    sentence2 = enrich(sents12)

    tfidfVec = TfidfVectorizer(norm='l2',min_df=0, use_idf=True, smooth_idf=False, sublinear_tf=True)
    VecRep = tfidfVec.fit_transform([' '.join(set(sentence1)), ' '.join(set(sentence2))])
    array = VecRep.toarray() 
    
    Xtest[i][0] = float(jaccard_similarity(sentence1, sentence2))
    Xtest[i][1] = float(cosine_similarity(array[0], array[1]))


# In[76]:


test_pred_labels = bagModel.predict(Xtest)


# In[77]:


test_pred_file = []
newHeader = []
newHeader.append(header[0])
newHeader.append(header[3][:-1])
test_pred_file.append(newHeader)
for i in range(len(test_pred_labels)):
    newLine=[]
    newLine.append(testids[i])
    newLine.append(test_pred_labels[i])
    test_pred_file.append(newLine)


# In[78]:


import csv
with open('C:\\Users\\Sukruti\\Desktop\\test-set-predicted-answers.txt', mode='w', newline='\n') as writeFile:
    writeFile = csv.writer(writeFile, delimiter='\t')
    for i in range(len(test_pred_file)):
        writeFile.writerow(test_pred_file[i])

