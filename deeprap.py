# imports
import re
import pickle
import random
import pronouncing
import pybrain
from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer

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

# self explanatory - finds the most common item in a list
def most_common(lst):
    return max(set(lst), key=lst.count)

# implements a system that i made - figures out all of the rhymes of the lines
def rhymeindex(lyrics):
    rhyme_master_list = []
    print "Alright, building the list of all the rhymes - here are the words that have to be taken into account;"
    for i in lyrics:
        word = re.sub(r"\W+", '', i.split(" ")[-1]).lower()
        print word
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
    rhyme_master_list = remove_duplicate_items(rhyme_master_list)
    return rhyme_master_list

# removes duplicate items in a list
def remove_duplicate_items(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

# determines what a sentence rhymes with
def determine_rhyme(sentence):
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

#builds the list of all possible rhymes in the lyrics it can draw from
def rhyme_list_generator(lyrics, rapdict, all_possible_rhymes):
    for i in lyrics:
        if i != "":
            try:
                rapdict.append([str(i), int(syllablesentencecount(str(i))), all_possible_rhymes.index(determine_rhyme(i))])
            except Exception:
                print "Hm, for some reason we couldn't do anything with this line - remove symbols from it and try again: " + str(i)

# turns the dataset-like numbers into the corresponding lyrics
def formatbar(bar, rapdict, all_possible_rhymes, lyricsused, song):
    for i in rapdict:
        if abs(i[1] - int(bar[0] * 20)) < 2 and i[2] == int((bar[1]) * len(all_possible_rhymes)):
            if str(i[0]) not in lyricsused and str(i[0]) not in lyrics_used_in_song(song):
                lyricsused.append(str(i[0]))

# creates a list 'rap' with all of the dataset-like numbers in it - and uses function 'formatbar' to turn these into
# actual lyrics.
def writearap(start, net, rapdict, all_possible_rhymes, lyricsused, song):
    rap = []
    rap.append(start)
    while len(rap) < 100:
        rap.append(net.activate(rap[-1]))

    for i in range(0, 100):
        formatbar([rap[i][0], rap[i][1]], rapdict, all_possible_rhymes, lyricsused, song)
        formatbar([rap[i][2], rap[i][3]], rapdict, all_possible_rhymes, lyricsused, song)
    if len(lyricsused) > 2:
        return lyricsused
    else:
        return []

# gets all of the lyrics that have been used in neural_rap.txt
def lyrics_used_in_song(song):
    used = []
    for line in song:
        if line != "":
            used.append(line)
    return used

# the main function -- i'll clean this up and divide it into smaller functions soon.
def main():
    # the existing lyrics you've filled the text document with
    lyrics = open('lyrics.txt').read().split("\n")

    # the (now empty) song the neural network is going to write
    song = []

    # all of the possible rhymes based on the contents of the stuff you fed it
    all_possible_rhymes = rhymeindex(lyrics)

    # debug stuff...
    print "\n\nAlright, here are all of the possible rhymes from the lyrics it can draw from."
    print all_possible_rhymes

    # rapdict is just the list containing smaller lists as follows;
    # [the text of the line, the number of syllables in the line, the number of the rhyme scheme of the line]
    rapdict = []
    rhyme_list_generator(lyrics, rapdict, all_possible_rhymes)
    print rapdict

    # makes a dataset
    ds = SupervisedDataSet(4,4)
    # the dataset is in the form of the amount of syllables and rhyme scheme of TWO lines that are next to each other in the song.


    for i in rapdict[:-3]:
        if i != "" and rapdict[rapdict.index(i) + 1] != "" and rapdict[rapdict.index(i) + 2] != "" and rapdict[rapdict.index(i) + 3] != "":
            # twobars is just a list containing the aspects of two lines in a row
            twobars = [i[1], i[2], rapdict[rapdict.index(i) + 1][1], rapdict[rapdict.index(i) + 1][2], rapdict[rapdict.index(i) + 2][1], rapdict[rapdict.index(i) + 2][2], rapdict[rapdict.index(i) + 3][1], rapdict[rapdict.index(i) + 3][2]]

            # twobars gets formatted into floating point values between 0 and 1 so it can be entered into the dataset
            ds.addSample((twobars[0] / float(20), int(twobars[1]) / float(len(all_possible_rhymes)), twobars[2] / float(20), int(twobars[3]) / float(len(all_possible_rhymes))), (twobars[4] / float(20), int(twobars[5]) / float(len(all_possible_rhymes)), twobars[6] / float(20), int(twobars[7]) / float(len(all_possible_rhymes))))

    # printing the dataset
    print "\n\nAlright, here is the dataset."
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

    trainingcount = 1000

    # The part that actually writes a rap.
    final_song = open("neural_rap.txt", "r+")

    # The number 3 at the end of this line can be tweaked- it's just so things don't get too repetitive/drawn out.
    # for example; if i had 30 lines to draw from, I wouldn't want to try and rearrange them into a song with 30 lines.
    # it would be much better if i only tried to take 10 rhyming lines and make a song with those.
    while len(song) < len(lyrics) / 3:
        # uncomment this next line if you're training the network.
        #t.trainOnDataset(ds, 100)
        verse = writearap([(random.choice(range(1,20))) / 20.0 , (random.choice(range(1, len(all_possible_rhymes)))) / float(len(all_possible_rhymes)), (random.choice(range(1, 20))) / 20.0, (random.choice(range(1, len(all_possible_rhymes)))) / float(len(all_possible_rhymes))], net, rapdict, all_possible_rhymes, lyricsused, song)
        if len(verse) > 2:
            for line in lyricsused:
                final_song.write(str(line) + "\n")

                # actually write the line to the song
                song.append(line)
            final_song.write("\n")
            print "Just wrote a verse to the file... - " + str(lyricsused)
            lyricsused = []
        #uncomment these if you wish to train the network, you'll also have to uncomment above lines that actually train the network (around line 145)
        """
        fileObject = open('trained_net_' + str(trainingcount), 'w')
        pickle.dump(net, fileObject)
        fileObject.close()
        trainingcount += 1000
        """

main()
print "\nDone! Check neural_rap.txt for the finished rap."
