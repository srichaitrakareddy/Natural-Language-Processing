# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 21:13:58 2019

@author: Sri Chaitra Kareddy
"""

import nltk
import spacy
nlp = spacy.load("en_core_web_sm")
from nltk.stem import WordNetLemmatizer 
from nltk.grammar import DependencyGrammar
from nltk.parse import DependencyGraph
from nltk.corpus import wordnet as wn
from nltk.parse import CoreNLPParser



def my_chunks(sentence):
    print("====================")
    print("PARSING:")
    print("====================")
    sents = nlp(sentence)
    for token in sents:
        print(token.text,token.lemma_,token.pos_,token.tag_,token.dep_)
        return sents
	

def my_tokenizer(arg1):
	tokenize_words=word_tokenize(arg1)
	print("====================")
	print("TOKENS:")
	print("====================")
	print(tokenize_words)


def my_pos(arg1):
	tokenize_words=word_tokenize(arg1)
	pos_tag_items=nltk.pos_tag(tokenize_words)
	print("====================")
	print("POS TAGGED SENTENCE:")
	print("====================")
	print(pos_tag_items)

def my_lemma(arg1):
	lemmatizer = WordNetLemmatizer() 
	tokenize_words=word_tokenize(arg1)
	print("====================")
	print("LEMMATIZATION OUTPUT:")
	print("====================")
	output = ' '.join([lemmatizer.lemmatize(w) for w in tokenize_words])
	print(output)



def get_extract(synset,arg1):
    if(arg1=='partholonym'):
    	s=synset.part_holonyms()
    elif(arg1=='subholonym'):
    	s=synset.substance_holonyms()
    elif(arg1=='partmeronym'):
    	s=synset.part_meronyms()
    elif(arg1=='submeronym'):
    	s=synset.substance_meronyms()
    elif(arg1=='Hyper'):
    	s=synset.hypernyms()
    else:
    	s=synset.hyponyms()
    ans = set()
    for each in s:
        ans |= set(get_extract(each,arg1))
    return ans | set(s)



def my_wordnet_extractions(arg1):
    tokenize_words=word_tokenize(arg1)
    for each in tokenize_words:
        print("====================")
        print("SYNSET INFORRMATION:")
        print("====================")
        list_synsets=wn.synsets(each)
        if(len(list_synsets)==0):
            print("No more synsets available")
        print("====================")
        print("EACH SYNSET MEANING:")
        print("====================")
        for synset in list_synsets:
            print("\tLemma: {}".format(synset.name()))
            print("\tDefinition: {}".format(synset.definition()))
            print("\tExample: {}".format(synset.examples()))
        print("====================")
        print("Words in a particular Synset:")
        print("====================")
        for synset in list_synsets:
            print(synset.lemma_names())
        print("====================")
        print("Hyponym(specific):")
        print("====================")
        for each in list_synsets:
            hypo = get_extract(each,'hypo')
            if(len(hypo)==0):
                print("No more Hyponyms available")
        print("====================")
        print("Hypernym(general):")
        print("====================")
        for each in list_synsets:
            hyper = get_extract(each,'Hyper')
            if(len(hyper)==0):
                print("No more Hypernyms available")
        print("====================")
        print("Meronyms:(Denotes the part of a Whole)")
        print("====================")
        print("Part_Representation of a Meronym")
        print("====================")
        for each in list_synsets:
            partmero = get_extract(each,'partmeronym')
            if(len(partmero)==0):
                print("No more part representation of a Meronym")
        print("====================")
        print("Whole_Representation/Substance of a Meronym")
        print("====================")
        for each in list_synsets:
            submero = get_extract(each,'submeronym')
            if(len(submero)==0):
                print("No more submeronyms available")
        print("====================")
        print("Holonyms:(Denotes a membership to something)")
        print("====================")
        print("Part_Representation of a Holonyms")
        print("====================")
        for each in list_synsets:
            partho = get_extract(each,'partholonym')
            if(len(partho)==0):
                print("No more Partholyms available")
        print("Whole_Representation of a Holonyms")
        print("====================")
        for each in list_synsets:
            subho = get_extract(each,'subholonym')
            if(len(subho)==0):
                print("No more Subholonyms available")
        print("====================")
 



if __name__ == '__main__':
	print("Enter your input sentence:")
	sentence=input()
	my_tokenizer(sentence)
	my_pos(sentence)
	my_lemma(sentence)
	my_wordnet_extractions(sentence)
	my_chunks(sentence)
