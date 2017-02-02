import pyttsx
import subprocess
import threading
from time import sleep
from threading import Thread

# VARIABLES
beat = "beat.mp3" 
slowdown_rate = 30 #higher value means slower speech... keep it between ~50 and 0 depending on how fast the beat is.
intro = 14 #amount in seconds it takes from the start of the beat to when the rapping should begin... how many seconds the AI waits to start rapping.


def play_mp3(path):
    subprocess.Popen(['mpg123', '-q', path]).wait()


engine = pyttsx.init()

def letters(input):
    valids = []
    for character in input:
        if character.isalpha() or character == "," or character == "'" or character == " ":
            valids.append(character)
    return ''.join(valids)

lyrics = open("neural_rap.txt").read().split("\n") #this reads lines from a file called 'neural_rap.txt'
#print lyrics
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - slowdown_rate)
voices = engine.getProperty('voices')

wholesong = ""
for i in lyrics:
    wholesong += i + " ... "


def sing():
    for line in wholesong.split(" ... "):
        engine.say(str(line))
    engine.runAndWait()

def beat():
    play_mp3("beat.mp3")


Thread(target=beat).start()
sleep(intro) # just waits a little bit to start talking
Thread(target=sing).start()
