# rapping-neural-network
I made this for my high school's programming club - which I'm the president/founder of.

It's a neural network that has been trained on rap songs, and can rearrange any lyrics you throw it into a song that rhymes and has a flow (to an extent).

For example: I could feed it the lyrics of around 10 rap songs from various artists and it would in essence, combine lines from all of the songs you feed it to make a new song. There's also another file that helps it actually rap the song on a beat with text to speech.


# How to use

## Write song

    pip install -U -r requirements.txt 
    
    download the trained nn
    https://docs.google.com/uc?id=0B-_m9VM1w1bKR3NTdVJRRDVCeE0&export=download

    Fill "lyrics.txt" with rap lyrics of your choosing - the more the better, as this is used to make a dataset and in this case large datasets return better results. Maybe around 6 or 7 songs is good --

   avoid putting things like "[bridge]" or "[intro]" in there - only put in actual lines from the song - and separate each line by a newline (press the 'enter' key, usually).

    python deeprap.py 
    
    neural_rap.txt contains the text
## generate sound

python speechtest.py, you can replace the mp3 file i've included with your own beat (mp3 format). this is a very small program that just runs a text to speech of the neural network's lyrics over a beat.


# Let's hear something it made
Okay... Here's some lyrics that it made - excuse the vulgarities, the neural network wrote it and not me.
http://pastebin.com/raw/u0Vf7T4L

And here is the recording of "speechtest.py" using those lyrics.
http://vocaroo.com/i/s1liCOwMUhuZ
