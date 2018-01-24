import pronouncing
import markovify
import re
import random
import numpy as np
import os
from keras.models import Sequential
from keras.layers import LSTM

depth = 4  # depth of the network. changing will require a retrain
maxsyllables = 16  # maximum syllables per line. Change this freely without retraining the network
train_mode = False
artist = "jay_z"  # used when saving the trained model
rap_file = "neural_rap.txt"  # where the rap is written to


def create_network(depth):
    # Sequential() creates a linear stack of layers
    model = Sequential()
    # Adds a LSTM layer as the first layer in the network with
    # 4 units (nodes), and a 2x2 tensor (which is the same shape as the
    # training data)
    model.add(LSTM(4, input_shape=(2, 2), return_sequences=True))
    # adds 'depth' number of layers to the network with 8 nodes each
    for i in range(depth):
        model.add(LSTM(8, return_sequences=True))
    # adds a final layer with 2 nodes for the output
    model.add(LSTM(2, return_sequences=True))
    # prints a summary representation of the model
    model.summary()
    # configures the learning process for the network / model
    # the optimizer function rmsprop: optimizes the gradient descent
    # the loss function: mse: will use the "mean_squared_error when trying to improve
    model.compile(optimizer='rmsprop',
                  loss='mse')

    if artist + ".rap" in os.listdir(".") and train_mode == False:
        # loads the weights from the hdf5 file saved earlier
        model.load_weights(str(artist + ".rap"))
        print "loading saved network: " + str(artist) + ".rap"
    return model


def markov(text_file):
    read = open(text_file, "r").read()
    # markovify goes line by line of the lyrics.txt file and
    # creates a model of the text which allows us to use
    # make_sentence() later on to create a bar for lyrics
    # creates a probability distribution for all the words
    # so it can generate words based on the current word we're on
    text_model = markovify.NewlineText(read)
    return text_model


# used when generating bars and making sure the length is not longer
# than the max syllables, and will continue to generate bars until
# the amount of syllables is less than the max syllables
def syllables(line):
    count = 0
    for word in line.split(" "):
        vowels = 'aeiouy'
        word = word.lower().strip(".:;?!")
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith('e'):
            count -= 1
        if word.endswith('le'):
            count += 1
        if count == 0:
            count += 1
    return count / maxsyllables


# writes a rhyme list to a rhymes file that allows for use when
# building the dataset, and composing the rap
def rhymeindex(lyrics):
    if str(artist) + ".rhymes" in os.listdir(".") and train_mode == False:
        print "loading saved rhymes from " + str(artist) + ".rhymes"
        return open(str(artist) + ".rhymes", "r").read().split("\n")
    else:
        rhyme_master_list = []
        print "Alright, building the list of all the rhymes"
        for i in lyrics:
            # grabs the last word in each bar
            word = re.sub(r"\W+", '', i.split(" ")[-1]).lower()
            # pronouncing.rhymes gives us a word that rhymes with the word being passed in
            rhymeslist = pronouncing.rhymes(word)
            # need to convert the unicode rhyme words to UTF8
            rhymeslist = [x.encode('UTF8') for x in rhymeslist]
            # rhymeslistends contains the last two characters for each word
            # that could potentially rhyme with our word
            rhymeslistends = []
            for i in rhymeslist:
                rhymeslistends.append(i[-2:])
            try:
                # rhymescheme gets all the unique two letter endings and then
                # finds the one that occurs the most
                rhymescheme = max(set(rhymeslistends), key=rhymeslistends.count)
            except Exception:
                rhymescheme = word[-2:]
            rhyme_master_list.append(rhymescheme)
        # rhyme_master_list is a list of the two letters endings that appear
        # the most in the rhyme list for the word
        rhyme_master_list = list(set(rhyme_master_list))

        reverselist = [x[::-1] for x in rhyme_master_list]
        reverselist = sorted(reverselist)
        # rhymelist is a list of the two letter endings (reversed)
        # the reason the letters are reversed and sorted is so
        # if the network messes up a little bit and doesn't return quite
        # the right values, it can often lead to picking the rhyme ending next to the
        # expected one in the list. But now the endings will be sorted and close together
        # so if the network messes up, that's alright and as long as it's just close to the
        # correct rhymes
        rhymelist = [x[::-1] for x in reverselist]

        f = open(str(artist) + ".rhymes", "w")
        f.write("\n".join(rhymelist))
        f.close()
        print rhymelist
        return rhymelist


# converts the index of the most common rhyme ending
# into a float
def rhyme(line, rhyme_list):
    word = re.sub(r"\W+", '', line.split(" ")[-1]).lower()
    rhymeslist = pronouncing.rhymes(word)
    rhymeslist = [x.encode('UTF8') for x in rhymeslist]
    rhymeslistends = []
    for i in rhymeslist:
        rhymeslistends.append(i[-2:])
    try:
        rhymescheme = max(set(rhymeslistends), key=rhymeslistends.count)
    except Exception:
        rhymescheme = word[-2:]
    try:
        float_rhyme = rhyme_list.index(rhymescheme)
        float_rhyme = float_rhyme / float(len(rhyme_list))
        return float_rhyme
    except Exception:
        return None


# grabs each line of the lyrics file and puts them
# in their own index of a list, and then removes any empty lines
# from the lyrics file and returns the list as bars
def split_lyrics_file(text_file):
    text = open(text_file).read()
    text = text.split("\n")
    while "" in text:
        text.remove("")
    return text


# only ran when not training
def generate_lyrics(lyrics_file):
    bars = []
    last_words = []
    lyriclength = len(open(lyrics_file).read().split("\n"))
    count = 0
    markov_model = markov(lyrics_file)

    while len(bars) < lyriclength / 9 and count < lyriclength * 2:
        # By default, the make_sentence method tries, a maximum of 10 times per invocation,
        # to make a sentence that doesn't overlap too much with the original text.
        # If it is successful, the method returns the sentence as a string.
        # If not, it returns None. (https://github.com/jsvine/markovify)
        bar = markov_model.make_sentence()

        # make sure the bar isn't 'None' and that the amount of
        # syllables is under the max syllables
        if type(bar) != type(None) and syllables(bar) < 1:

            # function to get the last word of the bar
            def get_last_word(bar):
                last_word = bar.split(" ")[-1]
                # if the last word is punctuation, get the word before it
                if last_word[-1] in "!.?,":
                    last_word = last_word[:-1]
                return last_word

            last_word = get_last_word(bar)
            # only use the bar if it is unique and the last_word
            # has only been seen less than 3 times
            if bar not in bars and last_words.count(last_word) < 3:
                bars.append(bar)
                last_words.append(last_word)
                count += 1

    return bars


# used to construct the 2x2 inputs for the LSTMs
# the lyrics being passed in are lyrics (original lyrics if being trained,
# or ours if it's already trained)
def build_dataset(lyrics, rhyme_list):
    dataset = []
    line_list = []
    # line_list becomes a list of the line from the lyrics, the syllables for that line (either 0 or 1 since
    # syllables uses integer division by maxsyllables (16)), and then rhyme returns the most common word
    # endings of the words that could rhyme with the last word of line
    for line in lyrics:
        line_list = [line, syllables(line), rhyme(line, rhyme_list)]
        dataset.append(line_list)

    x_data = []
    y_data = []

    # using range(len(dataset)) - 3 because of the way the indices are accessed to
    # get the lines
    for i in range(len(dataset) - 3):
        line1 = dataset[i][1:]
        line2 = dataset[i + 1][1:]
        line3 = dataset[i + 2][1:]
        line4 = dataset[i + 3][1:]

        # populate the training data
        # grabs the syllables and rhyme index here
        x = [line1[0], line1[1], line2[0], line2[1]]
        x = np.array(x)
        # the data is shaped as a 2x2 array where each row is a
        # [syllable, rhyme_index] pair
        x = x.reshape(2, 2)
        x_data.append(x)

        # populate the target data
        y = [line3[0], line3[1], line4[0], line4[1]]
        y = np.array(y)
        y = y.reshape(2, 2)
        y_data.append(y)

    # returns the 2x2 arrays as datasets
    x_data = np.array(x_data)
    y_data = np.array(y_data)

    # print "x shape " + str(x_data.shape)
    # print "y shape " + str(y_data.shape)
    return x_data, y_data

# only used when not training
def compose_rap(lines, rhyme_list, lyrics_file, model):
    rap_vectors = []
    human_lyrics = split_lyrics_file(lyrics_file)

    # choose a random line to start in from given lyrics
    initial_index = random.choice(range(len(human_lyrics) - 1))
    # create an initial_lines list consisting of 2 lines
    initial_lines = human_lyrics[initial_index:initial_index + 8]

    starting_input = []
    for line in initial_lines:
        # appends a [syllable, rhyme_index] pair to starting_input
        starting_input.append([syllables(line), rhyme(line, rhyme_list)])

    # predict generates output predictions for the given samples
    # it's reshaped as a (1, 2, 2) so that the model can predict each
    # 2x2 matrix of [syllable, rhyme_index] pairs
    starting_vectors = model.predict(np.array([starting_input]).flatten().reshape(4, 2, 2))
    rap_vectors.append(starting_vectors)

    for i in range(49):
        rap_vectors.append(model.predict(np.array([rap_vectors[-1]]).flatten().reshape(4, 2, 2)))

    return rap_vectors


def vectors_into_song(vectors, generated_lyrics, rhyme_list):
    print "\n\n"
    print "About to write rap (this could take a moment)..."
    print "\n\n"

    # compare the last words to see if they are the same, if they are
    # increment a penalty variable which grants penalty points for being
    # uncreative
    def last_word_compare(rap, line2):
        penalty = 0
        for line1 in rap:
            word1 = line1.split(" ")[-1]
            word2 = line2.split(" ")[-1]

            # remove any punctuation from the words
            while word1[-1] in "?!,. ":
                word1 = word1[:-1]

            while word2[-1] in "?!,. ":
                word2 = word2[:-1]

            if word1 == word2:
                penalty += 0.2

        return penalty

    # vector_half is a single [syllable, rhyme_index] pair
    # returns a score rating for a given line
    def calculate_score(vector_half, syllables, rhyme, penalty):
        desired_syllables = vector_half[0]
        desired_rhyme = vector_half[1]
        # desired_syllables is the number of syllables we want
        desired_syllables = desired_syllables * maxsyllables
        # desired rhyme is the index of the rhyme we want
        desired_rhyme = desired_rhyme * len(rhyme_list)

        # generate a score by subtracting from 1 the sum of the difference between
        # predicted syllables and generated syllables and the difference between
        # the predicted rhyme and generated rhyme and then subtract the penalty
        score = 1.0 - (abs((float(desired_syllables) - float(syllables))) + abs(
            (float(desired_rhyme) - float(rhyme)))) - penalty

        return score

    # generated a list of all the lines from generated_lyrics with their
    # line, syllables, and rhyme float value
    dataset = []
    for line in generated_lyrics:
        line_list = [line, syllables(line), rhyme(line, rhyme_list)]
        dataset.append(line_list)

    rap = []

    vector_halves = []
    for vector in vectors:
        # vectors are the 2x2 rap_vectors (predicted bars) generated by compose_rap()
        # separate every vector into a half (essentially one bar) where each
        # has a pair of [syllables, rhyme_index]
        vector_halves.append(list(vector[0][0]))
        vector_halves.append(list(vector[0][1]))

    for vector in vector_halves:
        # Each vector (predicted bars) is scored against every generated bar ('item' below)
        # to find the generated bar that best matches (highest score) the vector predicted
        # by the model. This bar is then added to the final rap and also removed from the
        # generated lyrics (dataset) so that we don't get duplicate lines in the final rap.
        scorelist = []
        for item in dataset:
            # item is one of the generated bars from the Markov model
            line = item[0]

            if len(rap) != 0:
                penalty = last_word_compare(rap, line)
            else:
                penalty = 0
            # calculate the score of the current line
            total_score = calculate_score(vector, item[1], item[2], penalty)
            score_entry = [line, total_score]
            # add the score of the current line to a scorelist
            scorelist.append(score_entry)

        fixed_score_list = []
        for score in scorelist:
            fixed_score_list.append(float(score[1]))
        # get the line with the max valued score from the fixed_score_list
        max_score = max(fixed_score_list)
        for item in scorelist:
            if item[1] == max_score:
                # append item[0] (the line) to the rap
                rap.append(item[0])
                print str(item[0])

                # remove the line we added to the rap so
                # it doesn't get chosen again
                for i in dataset:
                    if item[0] == i[0]:
                        dataset.remove(i)
                        break
                break
    return rap


def train(x_data, y_data, model):
    # fit is used to train the model for 5 'epochs' (iterations) where
    # the x_data is the training data, and the y_data is the target data
    # x is the training and y is the target data
    # batch_size is a subset of the training data (2 in this case)
    # verbose simply shows a progress bar
    model.fit(np.array(x_data), np.array(y_data),
              batch_size=2,
              epochs=5,
              verbose=1)
    # save_weights saves the best weights from training to a hdf5 file
    model.save_weights(artist + ".rap")


def main(depth, train_mode):
    model = create_network(depth)
    # change the lyrics file to the file with the lyrics you want to be trained on
    text_file = "jayz_lyrics.txt"

    if train_mode == True:
        bars = split_lyrics_file(text_file)

    if train_mode == False:
        bars = generate_lyrics(text_file)

    rhyme_list = rhymeindex(bars)
    if train_mode == True:
        x_data, y_data = build_dataset(bars, rhyme_list)
        train(x_data, y_data, model)

    if train_mode == False:
        vectors = compose_rap(bars, rhyme_list, text_file, model)
        rap = vectors_into_song(vectors, bars, rhyme_list)
        f = open(rap_file, "w")
        for bar in rap:
            f.write(bar)
            f.write("\n")


main(depth, train_mode)
