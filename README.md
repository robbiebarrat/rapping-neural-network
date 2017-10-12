# Rapping-neural-network
This is a generative art project I made for my high school's programming club - which ~I'm the president/founder of~ I was the president/founder of until I graduated the other month.

It's a neural network that has been trained on Kanye West's discography, and can use any lyrics you feed it and write a new song *word by word* that rhymes and has a flow (to an extent).

Quartz did a really nice profile on me and the program here; https://qz.com/920091/a-west-virginia-teen-taught-himself-how-to-build-a-rapping-ai-using-kanye-west-lyrics/

# Let's hear something it made
Okay... Here's a song it wrote *word by word* using kanye's discography - excuse the vulgarities, the neural network wrote it and not me.
https://soundcloud.com/rapping_neural_network/networks-with-attitude

Here are the lyrics;
http://pastebin.com/MUDc9Unt



## Setup

Install (with python 2.x)

    pip install -U -r requirements.txt 

## Usage

### Data preperation
**If you'd like to use Kanye's lyrics - skip this section**
`Lyrics.txt` comes with Kanye's entire discography in it. You can either use this, or fill it with other lyrics.

Guide to using your own lyrics with `lyrics.txt`
* Avoid including things like "[bridge]" or "[intro]" 

* Seperate each line by a newline

* Avoid non alphanumeric characters (besides basic punctuation)

* You don't have to retype everything - just copy and paste from some lyrics website

### Training
**Skip this part if you are using the default kanye lines**

* In `model.py`, change the variable `artist` to the name of the new artist you've used in `lyrics.txt`

* In `model.py`, change the variable `train_mode` to `True`

* Run the program with `python model.py`, and allow training to finish.

### Generating raps

* In `model.py`, if you've trained a new network, the variable `train_mode` will be `True`, set this back to `False`

* Run the program with `python model.py`

* The rap will be written to the output of your terminal, and also to a file called `neural_rap.txt`

### Performing raps

* speech.py will "rap" the generated songs with a text to speech over a generic rap beat (`beat.mp3`), just run `python speech.py`

## How it works

Alright, so basically a markov chain will look at the lyrics you entered and generate new lines. Then, it feeds this to a recurrent neural net that will generate a sequence of tuples in the format of 

    (desired rhyme, desired count of syllables)

The program will then sift through the lines the markov chain generated, and match the lines to their corresponding tuples. The result is the rap.

# Future goals:

1. Use lyrebird.ai to have it rap in Kanye's voice... I'll probably have to hire a Kanye voice impersonator to supply me with 5 minutes of audio to train the net with though... Either that or jailbreak an old iPod and use it to do text to speech with Siri's voice.


2. Bring back the seperate 'verses' and appropriate pauses that the first version had.


3. Generative rap beats that it can rap over.



Once I get the lyrebird.ai thing working where it can rap and imitate someone's voice, I really want to do some type of 'album' where there's a separate track on it for each really popular dead rapper (The 90's had some really good ones, Notorious B.I.G., Big L, etc.) - where each track would have the network rapping with lyrics / flow in the style of the said rapper, and imitating their voice with lyrebird's network (admit it, the current text to speech I have is pretty trash). Kind of like an AI resurrection of dead rappers...
