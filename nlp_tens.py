import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import numpy as np
import random
import pickle
from collections import Counter

lemmatizer = WordNetLemmatizer()
hm_lines = 10000000

def create_lexicon(pos,neg):
    lexicon = []
    for fi in [pos,neg]:
        with open(fi,'r') as f:
            contents = f.readlines()
            for l in contents[:hm_lines]:
                all_words = word_tokenize(l.lower())
                lexicon += list(all_words)

    lexicon = [lemmatizer.lemmatize(i) for  i in lexicon]
    w_counts = Counter(lexicon)

    l2 = []
    for w in w_counts:
        if 1000 > w_counts > 50:
            l2.append(w)
    print(len(l2))
    return l2

def sample_handling(sample,lexicon,classification):
    featureset = []

    with open(sample,'r') as f:
        contents = f.readlines()
        for l in contents[:hm_lines]:
            current_words = word_tokenize(l.lower())
            current_words = [lemmatizer.lemmatize(i)for i in current_words]
            feature = np.zeros(len(lexicon))
            for word in current_words:
                if word.lower() in lexicon:
                    index_value = lexicon.index(word.lower())
                    feature[index_value] +=1
            feature = list(feature)
            featureset.append([feature, classification])
    return featureset

def create_feature_set_and_labels(pos,neg,test_size = 0.1):
    lexicon = create_lexicon(pos,neg)
    feature = []
    feature += sample_handling('pos.txt',lexicon,[1,0])
    feature += sample_handling('neg.txt', lexicon,[0,1])
    random.shuffle(feature)
    feature = np.array(feature)
    testing_size = int(test_size*len(feature))

    train_x = list(feature[:,0][:-testing_size])
    train_y = list(feature[:,1][:-testing_size])

    test_x = list(feature[:,0][:-testing_size])
    test_y = list(feature[:,1][:-testing_size])

    return train_x, train_y, test_x, test_y

if __name__ == 'main':
    train_x, train_y, test_x, test_y =  create_feature_set_and_labels('pos.txt','neg.txt')
    with open('sentiment_set.pickle','wb') as f:
        pickle.dump([train_x, train_y, test_x, test_y], f)


