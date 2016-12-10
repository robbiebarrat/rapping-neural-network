import pronouncing
import pyttsx
engine = pyttsx.init()
import re
import pybrain
from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
import pickle
import random

#fill lyrics.txt with the rap lyrics you want it to use. leave out anything that isn't a line, and keep it newline delimited.
lyrics = open('lyrics.txt').read().split("\n")

# counts syllables in word
def syllablecount(word):
    count = 0
    vowels = 'aeiouy'
    word = word.lower().strip(".:;?!")
    if word[0] in vowels:
        count +=1
    for index in range(1,len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            count +=1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count+=1
    if count == 0:
        count +=1
    return count
# counts syllables in sentence
def syllablesentencecount(sentence):
    count = 0
    for word in sentence.split(" "):
        count += syllablecount(word)
    return count

# self explanatory
def most_common(lst):
    return max(set(lst), key=lst.count)

# implements a system that i made - indexes all of the rhymes of the lines
def rhymeindex():
    rhyme_master_list = []
    for i in lyrics:
        word = re.sub(r"\W+", '', i.split(" ")[-1]).lower()
        print word + 'cscs'
        #print syllablesentencecount(word)
        rhymeslist = pronouncing.rhymes(word)
        rhymeslist = [x.encode('UTF8') for x in rhymeslist]
        rhymeslistends = []
        for i in rhymeslist:
            rhymeslistends.append(i[-2:])
        try:
            rhymescheme = most_common(rhymeslistends)
        except Exception:
            rhymescheme = word[-2:]
        rhyme_master_list.append(rhymescheme)
    rhyme_master_list = f7(rhyme_master_list)
    return rhyme_master_list

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

# determines what a sentence rhymes with
def rhymeschemeofsentence(sentence):
    word = re.sub(r"\W+", '', sentence.split(" ")[-1]).lower()
    rhymeslist = pronouncing.rhymes(word)
    rhymeslist = [x.encode('UTF8') for x in rhymeslist]
    rhymeslistends = []
    for i in rhymeslist:
        rhymeslistends.append(i[-2:])
    try:
        rhymescheme = most_common(rhymeslistends)
    except Exception:
        rhymescheme = word[-2:]
    return rhymescheme

rhyme_master_list = rhymeindex()

# debug stuff...
print rhyme_master_list


rapdict = []
def dictionarybuilder():
    for i in lyrics:
        if i != "":
            try:
                rapdict.append([str(i), int(syllablesentencecount(str(i))), rhyme_master_list.index(rhymeschemeofsentence(i))])
            except Exception:
                print "Hm, for some reason we couldn't do anything with this line - remove symbols from it and try again: " + str(i)
dictionarybuilder()
print rapdict

# makes a dataset
ds = SupervisedDataSet(4,4)
# the dataset is in the form of the amount of syllables and rhyme scheme of TWO lines that are next to each other in the song.


for i in rapdict[:-3]:
    if i != "" and rapdict[rapdict.index(i) + 1] != "" and rapdict[rapdict.index(i) + 2] != "" and rapdict[rapdict.index(i) + 3] != "":
        twobars = [i[1], i[2], rapdict[rapdict.index(i) + 1][1], rapdict[rapdict.index(i) + 1][2], rapdict[rapdict.index(i) + 2][1], rapdict[rapdict.index(i) + 2][2], rapdict[rapdict.index(i) + 3][1], rapdict[rapdict.index(i) + 3][2]]
        print twobars
        ds.addSample((twobars[0] / float(20), int(twobars[1]) / float(len(rhyme_master_list)), twobars[2] / float(20), int(twobars[3]) / float(len(rhyme_master_list))), (twobars[4] / float(20), int(twobars[5]) / float(len(rhyme_master_list)), twobars[6] / float(20), int(twobars[7]) / float(len(rhyme_master_list))))

print ds

# Only uncomment this if you are training it on lyrics yourself.
# this part gets a neural network, trains it on lyrics and syllables and then saves it.
"""
net = buildNetwork(4,6,6,6,4,recurrent=True)
t = BackpropTrainer(net,learningrate=0.05,momentum=0.5,verbose=True)
t.trainOnDataset(ds,100)
t.testOnData(verbose=True)

fileObject = open('trained_net', 'w')
pickle.dump(net, fileObject)
fileObject.close()
"""

# This loads a neural network that has already been trained on an actual rap song - so it knows how the rhymes and syllables should fit together
fileObject = open('trained_net_420000','r')
net = pickle.load(fileObject)
t = BackpropTrainer(net,learningrate=0.01,momentum=0.5,verbose=True)

# uncomment this line too if you're training.
#t.trainOnDataset(ds, 200)

#just to make sure it doesn't keep using the same lyric over and over
lyricsused = []
# takes a list of 2 values, syllables and rhyming scheme
def formatbar(bar):
    for i in rapdict:
        if abs(i[1] - int(bar[0] * 20)) < 2 and i[2] == int((bar[1]) * len(rhyme_master_list)):
            if str(i[0]) not in lyricsused:
                hs = open("neural_rap.txt", "a")
                hs.write(str(i[0]) + " \n")
                hs.close()

                lyricsused.append(str(i[0]))

#
def writearap(start):
    rap = []
    rap.append(start)
    while len(rap) < 100:
        rap.append(net.activate(rap[-1]))

    for i in range(0, 100):
        formatbar([rap[i][0], rap[i][1]])
        formatbar([rap[i][2], rap[i][3]])
    lyricsused = []
trainingcount = 1000

# The part that actually writes a rap.
# COPY AND PASTE THE GOOD LINES IT COMES UP WITH INTO A FILE CALLED neural_rap.txt TO USE THE SPEECH PROGRAM (speechtest)
while True:
    #t.trainOnDataset(ds, 100)
    writearap([(random.choice(range(1,20))) / 20.0 , (random.choice(range(1,len(rhyme_master_list)))) / float(len(rhyme_master_list)), (random.choice(range(1,20))) / 20.0, (random.choice(range(1,len(rhyme_master_list)))) / float(len(rhyme_master_list))])
    print "\n\n\n\n\n ----- \n\n\n\n\n"
    fileObject = open('trained_net_' + str(trainingcount), 'w')
    pickle.dump(net, fileObject)
    fileObject.close()
    trainingcount += 1000
