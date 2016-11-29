import pyttsx
import subprocess
import threading
import string
from time import sleep
from threading import Thread

def play_mp3(path):
    subprocess.Popen(['mpg123', '-q', path]).wait()


engine = pyttsx.init()
lyrics = open("neural_rap.txt").read().split("\n") #this reads lines from a file called 'neural_rap.txt'
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 30)
voices = engine.getProperty('voices')

wholesong = ""
for i in lyrics:
    wholesong += i
    wholesong += " ... ... "

printable = set(string.printable)


def sing():
    for i in lyrics:
        engine.say(str(filter(lambda x: x in printable, wholesong)))
        engine.runAndWait()

def beat():
    play_mp3("beat.mp3")


Thread(target=beat).start()
sleep(14) # just waits a little bit to start talking
Thread(target=sing).start()
