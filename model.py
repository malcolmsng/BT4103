# all import functions
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import nltk
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('tagsets')
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords, wordnet
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer
import nlpaug.augmenter.word as naw
import contractions
from wordcloud import WordCloud
from collections import Counter

import os

from sklearn.metrics import *
from sklearn import preprocessing
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.ensemble import RandomForestClassifier 
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
import time
#from xgboost import XGBClassifier
#from xgboost import plot_importance
import scikitplot as skplt

def read_data(x='pseudo_data.xlsx'):
    if x == 'pseudo_data.xlsx':
        pseudo_data = pd.read_excel("./data/" + x, sheet_name="Defect Data")
    else:
        pseudo_data = pd.read_excel("./data/" + x)
    pseudo_df = pd.DataFrame(pseudo_data)
    return pseudo_df

# part-of-speech (pos) tagging for lemmatisation
def get_pos(tag):
    if tag[0] == 'N':
        return wordnet.NOUN
    elif tag[0] == 'V':
        return wordnet.VERB
    elif tag[0] == 'R':
        return wordnet.ADV
    elif tag[0] == 'J':
        return wordnet.ADJ
    return wordnet.NOUN

def processText(sentence):
    #tokenize
    tokenizer = RegexpTokenizer('\w+|\$[\d\.]+')
    tokens = tokenizer.tokenize(sentence.lower())

    # fix contractions
    fixed_tokens = [contractions.fix(word) for word in tokens]

    #remove stopwords
    useful_words = [word for word in fixed_tokens if word not in stopwords.words('english')]

    #pos tagging
    pos_tuple = pos_tag(useful_words)
    
    #lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(tup[0], get_pos(tup[1])) for ind, tup in enumerate(pos_tuple)]

    clean_text = ""
    for lem_word in lemmatized_tokens:
        clean_text += str(lem_word) + " "
        
    return clean_text

if __name__ == '__main__':

    # import training dataset
    df = read_data()
    df['Combined Text'] = df[df.columns[0:]].apply(lambda x: ' '.join(x.dropna().astype(str)),axis=1)
    df['Processed Text'] = df['Combined Text'].apply(lambda x: processText(x))

    # import test dataset
    test_df = read_data('temp_train.xlsx')
    test_df = test_df.tail(-1)      # remove header row
    test_df['Combined Text'] = test_df[test_df.columns[0:]].apply(lambda x: ' '.join(x.dropna().astype(str)),axis=1)
    test_df['Processed Text'] = test_df['Combined Text'].apply(lambda x: processText(x))

    #Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(df["Processed Text"], df["Primary Root Cause Classification #3"], test_size=0.2, shuffle=True)

    #Tf-Idf vectorization
    tfidf_vectorizer = TfidfVectorizer(use_idf = True)
    X_train_tfidf = tfidf_vectorizer.fit_transform(X_train) 
    X_test_tfidf = tfidf_vectorizer.transform(X_test)

    # train SVC model
    print("Training SVC model")
    #Parameter Tuning using Grid Search & Stratified K Fold Cross Validation for SVC
    parameters = {'kernel':('linear', 'poly', 'rbf'), 'C':[0.1, 1, 10, 100], 'gamma':[0.001, 0.01, 0.1, 1], 'degree': [1, 2, 3, 4]}
    grid_svc = GridSearchCV(SVC(), parameters, refit=True, cv=10, verbose=3) #cv: number of folds in a StratifiedKFold cross validation
    grid_svc.fit(X_train_tfidf, y_train)
    #print(grid_svc.best_estimator_)

    #Implement best SVC model
    print("Predicting root cases using SVC model")
    param_dict = grid_svc.best_params_
    svc = SVC(kernel=param_dict['kernel'], C=param_dict['C'], gamma=param_dict['gamma'], degree=param_dict['degree'], decision_function_shape='ovr') 
    svc.fit(X_train_tfidf, y_train)
    svc_y_pred = svc.predict(X_test_tfidf)

    svc_cr = classification_report(y_test, svc_y_pred, output_dict= True)

    # train Naive Bayes model model
    print("Training Naive Bayes model")
    #Parameter Tuning using Grid Search & Stratified K Fold Cross Validation for Naive Bayes
    parameters = {'alpha':[0.01, 0.1, 0.5, 1, 2, 5]} #smoothing parameter
    grid_mnb = GridSearchCV(MultinomialNB(), parameters, refit=True, cv=10, verbose=3) #cv: number of folds in a StratifiedKFold cross validation
    grid_mnb.fit(X_train_tfidf, y_train)

    #Implement best model
    print("Predicting root cases using Naive Bayes model")
    param_dict = grid_mnb.best_params_
    mnb = MultinomialNB(alpha=param_dict['alpha'])
    mnb.fit(X_train_tfidf, y_train)
    mnb_y_pred = mnb.predict(X_test_tfidf)

    mnb_cr = classification_report(y_test, mnb_y_pred, output_dict= True)

    # train Multinomial Logistic Regression model model
    print("Training Multinomial Logistic Regression model")
    #Parameter Tuning using Grid Search & Stratified K Fold Cross Validation for Multinomial Logistic Regression
    parameters = {'multi_class': ['multinomial'], 'solver': ['lbfgs'], 'C': [0.0, 0.0001, 0.001, 0.01, 0.1, 1.0], 'penalty': ['l2']} #smoothing parameter
    grid_mlr = GridSearchCV(LogisticRegression(), parameters, refit=True, cv=10, verbose=3) #cv: number of folds in a StratifiedKFold cross validation
    grid_mlr.fit(X_train_tfidf, y_train)

    #Implement best model
    param_dict = grid_mlr.best_params_
    mlr = LogisticRegression(multi_class='multinomial', solver='lbfgs', C=param_dict['C'], penalty=param_dict['penalty'])
    mlr.fit(X_train_tfidf, y_train)
    mlr_y_pred = mlr.predict(X_test_tfidf)

    mlr_cr = classification_report(y_test, mlr_y_pred, output_dict= True)


    all_values = [list(svc_cr['weighted avg'].values()), list(mnb_cr['weighted avg'].values()), list(mlr_cr['weighted avg'].values())]
    temp = pd.DataFrame(all_values, index = ["SVC", "Multinomial Naive Bayes", "Multiomial Logistic Regression"], columns = list(mlr_cr['weighted avg'].keys()))
    print(temp)
    print('donez')

