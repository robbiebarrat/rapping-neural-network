# Rapping-neural-network
I made this for my high school's programming club - which I'm the president/founder of.

It's a neural network that has been trained on rap songs, and can use any lyrics you feed it and write a new song (it now writes *word by word* as opposed to *line by line*) that rhymes and has a flow (to an extent).

Listen to / read the example at the bottom of this readme - it is the result of feeding the network ~6,000 Kanye West lines.



## Write song

Install (with python 2.x)

    pip install -U -r requirements.txt 

Fill "lyrics.txt" with rap lyrics of your choosing - the more the better - avoid putting things like "[bridge]" or "[intro]" in there - only put in actual lines from the song - and separate each line by a newline (the newline format is found on most websites that host lyrics, so you should have no trouble copying and pasting. The more songs the better - a few hundred lines should be fine, but you tend to get better results as the number of lines tends towards infinity.

    python deeprap.py

deeprap.py will show you some of its processes, and once it terminates, 'neural_rap.txt' will contain the song the neural network has composed. By default, the neural network no longer uses full lines from the lyrics you give it, but now it writes the song *word by word* with the help of a Markov chain. This means that it actually writes original lyrics.

### More info on deeprap.py, training the network on your own lyrics, and how the trained nets are stored ###
deeprap.py contains a variable on line 15 - "training". You can set training to 0 to have it just write a song from the lyrics you give it (this is the default value, and is probably what most people will use it for) - but if you actually want to train the network on your own set of lyrics change the value of "training" to 1, and it will train a network on the lines in "lyrics.txt". Keep in mind: the trained networks are saved as folders titled the number of epochs the network has been trained for. If you already have folders named "100", "200", etc. in the same directory as deeprap.py when you try to train a network, you should move these somewhere else to avoid confusion. The trained network folders contain 2 files, an xml file of the actual trained neural network, and a text file containing the list of rhymes the neural network was trained with. This is needed because since the neural network just works with numbers (each type of rhyme is interpreted as a float value) - this list is there so the network always interprets the same rhymes as their corresponding float values, regardless of the data you feed it.
    
## Generate sound

    python speechtest.py 
    
one of the mp3 files (specified in speechtest.py as a global variable) is the beat

# Let's hear something it made
Okay... Here's a song it wrote *word by word* - excuse the vulgarities, the neural network wrote it and not me.
http://pastebin.com/raw/MUDc9Unt
And here is the recording of "speechtest.py" using those lyrics, and "lofi_long.mp3".
https://soundcloud.com/rapping_neural_network/networks-with-attitude
