# Rapping-neural-network
This is a generative art project I made for my high school's programming club - which ~I'm the president/founder of~ I was the president/founder of until I graduated the other month.

It's a neural network that has been trained on Kanye West's discography, and can use any lyrics you feed it and write a new song *word by word* that rhymes and has a flow (to an extent).

Quartz did a really nice profile on me and the program here; https://qz.com/920091/a-west-virginia-teen-taught-himself-how-to-build-a-rapping-ai-using-kanye-west-lyrics/

# Let's hear something it made
Okay... Here's a song it wrote *word by word* using kanye's discography - excuse the vulgarities, the neural network wrote it and not me.
https://soundcloud.com/rapping_neural_network/networks-with-attitude

# Lyrics to above song
<details>
  <summary>Click to expand</summary>

Bust a playa with the kids I never had

All his time, all he had, all he had, all he had

Most you rappers don't even stop to get the most press kit

Playas is jealous cause we got the whole city lit

But without it I'd be worried if they playing that bullshit

You wanna complain about the nights even wilder

I swear to God I hope you have got to hear

I'll touch every curve of your favorite author

No more wasting time, you can't roam without Caesar

Back when Gucci was the best summer ever

Before Cam got the hundred with the peer pressure

She walking around looking like Herve Leger

So next time I'm in between but way more fresher

And they say you never know, never never NEVER

...

You the number one I'mma beat my brother

And I know a sign when I heard it's the magic hour

Get Olga Kurylenko, tell her to do better

That know we get them hammers, go on, call the lawyer


But still supported me when I get richer

This my first pair of shoes, I made the Bulls play better

Or use my arrogance as a wholesaler

Prince Williams ain't do it can't be your damn liar

You say I dress white, but my broad way thicker

If I be Don C, we got that, that thing clear

I dropped out of your body like a wrestler

I can't believe I'm back to a cold killer

Lady Eloise I need another lover

He loved Jesus when he off the power

So I pour the potion, so we gone dress whiter

Old folks talking bout Linda, from last September

Might spend 50 racks on my life like a fucking loser

...

He don't even stop to get this difficult

She told me that I stayed at home with my own vault

She's so precious with the space for the safe belt

Girl he had the strangest feeling lately

Fuck you playa I know it's especially

But let some black people to think logically

Fire Marshall said I could give you this feeling

And wrote hooks about slaves that the youth is missing

I know this part right here, history in the ring

Well I guess she was messin wit me when I'm cumming

I'm way better than some head on a chain gang

On a scale of this, and now you doing your thang

Y'all I know you're living your life so exciting

Started a little blog just to say nothing

I'mma need a fix, girl you was celebrating

Mayonnaise colored Benz I get my engine revving

And my chick in that old lady on Boomerang

Wifey gonna kill me, I do a gangbang

I put an angel in your life so exciting

Right when I do it right if you was celebrating

I was in Benzes, I was still at Burger King

It feel like this but playas don't know what you're drinking

Really Doe told you come on homie they wilding

I swear this right here, feel free to sing along

Shoulda known that was gonna come as it's good I'm young

...

These playas read the pimp manual, but I just want your girl you was clubbin'

First I spin around and vomit, then I made it from the day you just pretendin'

But I bet you they respect the name Kanye from the heart, y'all all frontin'

We in the same thing like a fat trainer takin a bite or somethin

Abbey Lee too, I'm a jerk, you need that happy beginnin', middle and endin'

That mean I forgot better shit than you ever heard about all this name callin'

Cause I can never be as laid back as this flow end, I'mma let Mos begin

And I bet you they respect the name Kanye from the heart, y'all all frontin'

...

My mama used to stay recession free

All my friends says implants is a beat from Ye

I want is what I do, act more stupidly

With no response make you wait longer than A.C.

Loud as a shorty I looked up to this degree

Young Walt Disney, I'ma tell you once ting

Straight to jail, yo, in a Bentley shining

Why you trying to make it just ring and ring

Now why would I listen to T-Pain and sing

Everything I throw them all laughing

So glad I ain't gotta borrow nothing

So I promised her everything

I've been waiting on this rocket, Yao Ming

I don't drink the drama that your dude bring

Kanye West is the making of a romantic

Play strings for the World's game, this is tragic

...and this is the making of a romantic

I done wore designers I won't get specific

The layers to my roots, I'm like a paraplegic

Come on, let's take a lot more than the music

I mean, after all the way we was magic

...

</details>

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
