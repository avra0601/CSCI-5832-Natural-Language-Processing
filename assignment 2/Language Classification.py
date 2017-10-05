# -*- coding: cp1252 -*-

# This program is written in python 2.7.
import itertools
from itertools import *
import codecs
import math
import operator
import re
from collections import Counter


# This function returns the best class and the probabilities.
def classify(bigram, words, all_words, classes, text):
    sen = " " + text  # just padding space to the sentence
    # we store the list of probabilities in this dictionary for each language
    list_of_probabilities = {}
    probs = {}  # creates a probability dictionary
    # gets possible bigrams from the test sentence
    sen_bigrams = [''.join(w) for w in zip(sen, sen[1:])]
    for lang in classes:
        probs[lang] = {}
        counter = 0
        # For each bigram we find the probability. If the bigram is not found
        # in the particular language then we just apply smoothing
        while(counter < len(sen_bigrams)):
            # just checks if each letter in bigram are there in the alphabet
            # set (ie in the 32 words). If yes probabilities are assigned else
            # if we   see any other character not availble in the training set
            # assign 0 to that bigram
            if((sen_bigrams[counter][0] in all_words) and (sen_bigrams[counter][1] in all_words)):
                probs[lang][sen_bigrams[counter]] = math.log(float(bigram[lang].get(
                    sen_bigrams[counter], 0.00) + 1.00) / float(words[lang].get(sen_bigrams[counter][0], 0.00) + 32.00))
            else:
                probs[lang][sen_bigrams[counter]] = 0.00
            counter = counter + 1
        counter = 0
        sum = 0.00  # Initializes the sum variable to 0

        # Below while loop adds all the probablities calculated.
        while(counter < len(sen_bigrams)):
            # Adds all the bigram counts and sotre it in sum
            sum += probs[lang].get(sen_bigrams[counter], 0)
            counter = counter + 1
        # We store the total probability in a dictionary
        list_of_probabilities[lang] = sum
    best_class = max(
        list_of_probabilities.iteritems(),
        key=operator.itemgetter(1))[0]
    return (best_class, list_of_probabilities)

def main():
    classes = ['de', 'en', 'nl', 'sv']  # Stores all classes in a list
    texts = {}
    alphabet = set()  # List that will contain all possible unique words (ie. V = 32 in our case)

    for lang in classes:
        texts[lang] = [line.strip() for line in codecs.open(
            lang, 'r', encoding='utf-8')][0]  # Stores the training data
        # Stores all 32 words in the training set as a list (without duplicates)
        alphabet |= {unigram for unigram in texts[lang]}


    bigram = {}  # dictionary consists of all bigram counts
    words = {}  # dictionary that consists of word count
    # The below block of code stores bigram count and word count for each language
    for lang in classes:
        # Creating a seperate dictionary for each language that stores the bigram
        # counts for each language
        bigram[lang] = {}
        # Creating a seperate dictionary for each language that stores the words
        # counts for each language
        words[lang] = {}

        # gets the word count in a dictionary where keys are the words
        words[lang] = Counter([''.join(w) for w in zip(texts[lang])])
        # gets possible bigrams from the test sentence
        bigram[lang] = Counter([''.join(w)
                                for w in zip(texts[lang], texts[lang][1:])])

    print ('\n')

    # we load the bigram counts, word counts, possible words, classes and the
    # test string

    print classify(bigram, words, alphabet, classes, u'this is a very short text')
    print classify(bigram, words, alphabet, classes, u'dies ist ein sehr kurzer text')
    print classify(bigram, words, alphabet, classes, u'dit is een zeer korte tekst')
    print classify(bigram, words, alphabet, classes, u'detta �r en mycket kort text')


if __name__ == "__main__":
    main()