# Rapping-neural-network
I made this for my high school's programming club - which I'm the president/founder of.

It's a neural network that has been trained on rap songs, and can rearrange any lyrics you feed it into a song that rhymes and has a flow (to an extent).

For example: I could feed it the lyrics of around 10 rap songs from various artists and it would in essence, combine lines from all of the songs you feed it to make a new song. There's also another file that helps it actually rap the song on a beat with text to speech.





## Write song

Install (with python 2.x)

    pip install -U -r requirements.txt 

Fill "lyrics.txt" with rap lyrics of your choosing - the more the better - avoid putting things like "[bridge]" or "[intro]" in there - only put in actual lines from the song - and separate each line by a newline (the newline format is found on most websites that host lyrics, so you should have no trouble copying and pasting. The more songs the better - a few hundred lines should be fine, but you tend to get better results as the number of lines tends towards infinity).

    python deeprap.py

deeprap.py will show you some of its processes, and once it terminates, 'neural_rap.txt' will contain the song the neural network has composed. You no longer have to add the good verses it generates by hand - It can select good verses and write them to the file itself.

### more info on deeprap.py, training the network on your own lyrics, and how the trained nets are stored ###
deeprap.py contains a variable on line 15 - "training". You can set training to 0 to have it just write a song from the lyrics you give it (this is the default value, and is probably what most people will use it for) - but if you actually want to train the network on your own set of lyrics change the value of "training" to 1, and it will train a network on the lines in "lyrics.txt". Keep in mind: the trained networks are saved as folders titled the number of epochs the network has been trained for. If you already have folders named "100", "200", etc. in the same directory as deeprap.py when you try to train a network, you should move these somewhere else to avoid confusion. The trained network folders contain 2 files, an xml file of the actual trained neural network, and a text file containing the list of rhymes the neural network was trained with. This is needed because since the neural network just works with numbers (each type of rhyme is interpreted as a float value) - this list is there so the network always interprets the same rhymes as their corresponding float values, regardless of the data you feed it.
    
## Generate sound

    python speechtest.py 
    
beat.mp3 is the beat

# Let's hear something it made
Okay... Here's some lyrics that it made - excuse the vulgarities, the neural network wrote it and not me.
http://pastebin.com/raw/u0Vf7T4L

And here is the recording of "speechtest.py" using those lyrics.
http://vocaroo.com/i/s1liCOwMUhuZ
