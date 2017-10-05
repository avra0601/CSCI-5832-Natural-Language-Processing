# This program is written in python 2.7
from collections import Counter
import operator


def get_transmission_counts(wordtags):
    bigram = {}
    bigram = Counter([' '.join(w) for w in zip(wordtags, wordtags[1:])])
    return bigram  # transmit counts


# Creates a dictionary of dictionary that has a word and tag counts...
# Something like The:{DT:39517 NN:32)
def get_emmision_counts(wordandtags):
    counter = 0
    words = {}
    # wordandtags[counter][0] - word  #wordandtags[counter][1] - tag
    while(counter < len(wordandtags)):
        if(wordandtags[counter][0] in words):  # First check if the word is in the dictionary
            # Checks if the word and the tag is already there if yes add 1 or
            # assign 1
            if(words[wordandtags[counter][0]].get(wordandtags[counter][1], 0)):
                words[wordandtags[counter][0]][wordandtags[counter][1]] += 1
            else:
                words[wordandtags[counter][0]][wordandtags[counter][1]] = 1
        else:
            # Create a dimension for the tag for the first time
            words[wordandtags[counter][0]] = {}
            words[wordandtags[counter][0]][wordandtags[counter][1]] = 1  # Assign value 1
        counter = counter + 1
    return words  # return the dictionary of dictionaries  .... This will be the emit counts


# Function to build the trellis and backtrace
def viterbi(sample, trans_counts, emmission_counts, list_of_tags, tag_count):
    # Append start and end state (n+2) states
    text = "<s> " + ' '.join(sample) + " </s>"
    text = text.split()
    time_state = []
    counter = 0
    while(counter < len(text)):
        # Appending time states (t0 to the last word)
        time_state.append("t" + str(counter))
        counter = counter + 1
    trellis = {}
    counter = 0
    # The datastructure for trellis dictonaries (states)  of dictionaries
    # (time steps) of list (calculated prob and back pointer)
    trellis['<s>'] = {}
    while(counter < len(list_of_tags)):  # Code to generate the trellis
        trellis[list_of_tags[counter]] = {}
        j = 1
        trellis[list_of_tags[counter]][time_state[0]] = [0, ' ']
        while(j < len(text)):
            # Initially we assign 0.00 and we set back pointer to null in a
            # trellis
            trellis[list_of_tags[counter]][time_state[j]] = [0.00, ' ']
            j = j + 1
        counter = counter + 1
    end_state = len(text) - 1  # Finding the last state
    trellis['<s>']['t0'] = [1.00, 'S']  # Initialize start state as 1
    counter = 1
    while(counter < len(text)):  # The taken will be O(ls^2) where l is the time step and s is the state .( We use two loops )
        for prevnode in trellis:
            for currnode in trellis:
                tot_count = 0.00  # the denominator
                count = 0.00  # the numerator

                # it contains the count of current tag
                tot_count = tag_count[currnode]
                # for the word how much that it is tagged as curr node
                count = emmision_counts[text[counter]].get(currnode, 0)
                # Calculate emmission probability
                word_currentprob = float(count) / tot_count

                tot_count = tag_count.get(prevnode, 0)
                count = bigram.get((prevnode + ' ' + currnode), 0)
                transition_prob = count / float(tot_count)
                # temp stores the value for that time step
                temp = transition_prob * \
                    trellis[prevnode][time_state[counter - 1]][0] * word_currentprob
                # If temp value is greater then we assign the cell with the new
                # value and we store the back pointer as prev(Where it came
                # from)
                if(temp > trellis[currnode][time_state[counter]][0]):
                    trellis[currnode][time_state[counter]][0] = temp
                    trellis[currnode][time_state[counter]][1] = prevnode
        counter = counter + 1
# For the final state the emmision is 1 only for </s> and if it is the last state, so  only in that cell value gets stored. Right from here we start backtracing
    # The below code is for back tracing
    result_tags = []  # result_tags is the result. We are going to back trace and store in this list
    test = {}
    for currnode in trellis:  # Every value will be 0 except for </s> and end state. So I pick the highest value. For finding it counter have written the code below
        # Just convert final state as dictionary so that it is easy to find the
        # maximum probability and the state it came from
        test[trellis[currnode][time_state[end_state]][1]
             ] = trellis[currnode][time_state[end_state]][0]
    max_val = max(test.iteritems(), key=operator.itemgetter(1))[
        0]  # Find the end state max probability
    counter = len(text) - 2  # state before the last state ie state before </s>
    result_tags.append(max_val)  # Appends the max transcounts
    while(counter >= 2):
        result_tags.append(trellis[max_val][time_state[counter]][1])
        # find where the maximum value came from
        max_val = trellis[max_val][time_state[counter]][1]
        counter = counter - 1
    result_tags.reverse()  # reverse the list
    return result_tags  # result_tags contains our result


# Below code appends <s> and </s> states in the empty line
lines = []
with open('wsj00-18.tag', "r") as training_file:
    lines.append("<s>\t<s>")
    for line in training_file:
        if(line == "\n"):
            lines.append("</s>\t</s>")
            lines.append("<s>\t<s>")
        else:
            lines.append(line.rstrip())
lines.append("</s>\t</s>")

# Finally we append </s>\t</s> because each time counter m appending end and
# start states
wordandtags = [(l.split("\t")[0], l.split("\t")[1])
               for l in lines]  # Reads a tuple of words and it corresponding tag
# Just reads the tags. It will be easy to bigram counts with it
wordtags = [l.split("\t")[1] for l in lines]
bigram = {}  # Counts for bigram tags (say NN DT)
tag_count = {}  # Counts for storing tag_count counts
bigram = get_transmission_counts(wordtags)  # Passing word tags as an argument
# Store all tag_count counts for tags
tag_count = Counter([''.join(w) for w in zip(wordtags)])
# Calculates emmission counts. We will have word count for a given tag
# I am just passing wordandtags as an argument. It is a tuple that
# contains a word and its tag
emitcounts = get_emmision_counts(wordandtags)
list_of_tags = tag_count.keys()  # returns the list of tags (47 tags)
transcounts = bigram  # just copying those values into these variables.
print viterbi(['This', 'is', 'a', 'sentence', '.'], transcounts, emitcounts, list_of_tags, tag_count)
print viterbi(['This', 'might', 'produce', 'a', 'result', 'if', 'the', 'system', 'works', 'well', '.'], transcounts, emitcounts, list_of_tags, tag_count)
print viterbi(['Can', 'a', 'can', 'can', 'a', 'can', '?'], transcounts, emitcounts, list_of_tags, tag_count)
print viterbi(['Can', 'a', 'can', 'move', 'a', 'can', '?'], transcounts, emitcounts, list_of_tags, tag_count)
print viterbi(['Can', 'you', 'say', 'how', 'a', 'can', 'can', 'run', '?'], transcounts, emitcounts, list_of_tags, tag_count)
