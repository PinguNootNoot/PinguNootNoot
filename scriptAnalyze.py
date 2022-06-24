import numpy as np
import copy
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk import classify
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize as token
from nltk.stem import WordNetLemmatizer as Lemmatizer
from nltk.corpus import movie_reviews, stopwords, wordnet as wn, sentiwordnet as swn
from sklearn import preprocessing as pp
from pickle import NONE

# Syntax and Semantic analysis & Sentiment meanings of words
# Data vectorization (chart representation)
# Word relation with characters (also influence)
# Text conclusion & generation

#nltk.download('wordnet')
#nltk.download('sentiwordnet')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('vader_lexicon')
#nltk.download('movie_reviews')

#*************************data analysis**************************
movie_name = "The Devil Wears Prada"
name_list = ["ANDY", "EMILY", "MIRANDA", "NIGEL", "NATE", "CHRISTIAN", "LILY", "DOUG", "RICHARD"]

vader = SentimentIntensityAnalyzer()
stop_list = set(stopwords.words('english'))
lemma = Lemmatizer()

def tagDefine(word):
    tag = pos_tag(token(word))

    if tag[0][1].startswith('NN'):
        return wn.NOUN
    elif tag[0][1].startswith('JJ'):
        return wn.ADJ
    elif tag[0][1].startswith('VB'):
        return wn.VERB
    elif tag[0][1].startswith('RB'):
        return wn.ADV

    return NONE

def AnalysisVader(targetDF):
    averageScoreList = list()
    plotSequenceList = list()

    i = 0
    for paragraph in targetDF['Preprocessed Script']:
        charList = []
        tokenized_paragraph = copy.deepcopy(token(paragraph))
        for word in tokenized_paragraph:
            if word in name_list and word not in charList:
                charList.append(word)

        sentiment_set = vader.polarity_scores(paragraph)
        targetDF.at[i,'Score Set'] = sentiment_set
        targetDF.at[i,'Overall Score'] = sentiment_set['compound']
        targetDF.at[i,'Main Characters'] = charList
        averageScoreList.append(sentiment_set['compound'])
        plotSequenceList.append(i+1)

        if targetDF.at[i,'Overall Score'] >= 0.1:
            targetDF.at[i,'Sentiment Label'] = "Positive"
        elif targetDF.at[i,'Overall Score'] <= -0.1:
            targetDF.at[i,'Sentiment Label'] = "Negative"
        else:
            targetDF.at[i,'Sentiment Label'] = "Neutral"

        i += 1

    plt.figure(figsize=(12,6))
    frame, fig = plt.subplots(facecolor='xkcd:tan')
    fig.set_facecolor('cornsilk')
    fig.set_title(movie_name)
    fig.set_xlabel('Script Index', color='xkcd:chocolate', style='oblique')
    fig.set_ylabel('Sentiment Distribution', color='xkcd:chocolate', style='oblique')
    fig.tick_params(labelcolor='xkcd:plum')
    plt.plot(plotSequenceList[0:500], averageScoreList[0:500], 'royalblue')
    plt.show()

    return targetDF

def AnalysisNLTK(targetDF):
    averageScoreList = list()
    plotSequenceList = list()
    sampleDF = copy.deepcopy(targetDF)
    i = 0
    for paragraph in sampleDF['Preprocessed Script']:
        paragraph = token(paragraph)
        for word in paragraph:
            if word not in stop_list:
                word = word.lower()
                wordTag = tagDefine(word)
                if wordTag == NONE:
                    continue
                word = lemma.lemmatize(word, wordTag)
                scoreSet = list(swn.senti_synsets(word, wordTag))[0]


        i += 1

    #return NONE

def accuracyTesting():

    return NONE
#****************************************************************

#******************************main******************************
scriptDF = pd.read_csv("script.txt")
scriptDF.columns = ['Preprocessed Script']
scriptDF['Main Characters'] = scriptDF['Events Set'] = scriptDF['Score Set'] = scriptDF['Overall Score'] = scriptDF['Sentiment Label'] = ""

VaDF = AnalysisVader(scriptDF)
#NtDF = AnalysisNLTK(scriptDF)
#print(VaDF.head(7))
