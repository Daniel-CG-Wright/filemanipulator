import filemanipulator as fp
from functools import partial

def printhello():
    print("Hello World")

def Params(param):
    print(str(param))

#ReadFile use

paramchoice = partial(Params, "foobar")#Partials must be used to parse arguments into a function using
files = fp.ReadFile("README.txt", actiontriggers=["small"], actions=[[printhello, paramchoice, "stop"]])
#When 'small' from the readme text file is read, it will cause the printhello and params functions to run, and then stop the reading, returning all previously read strings.

print(files)
#which are then printed here

#Like above, but does not stop until the whole file has been read. Note the nested lists for both, so that the indices for actions and actiontriggers are equal at point 0.
files = fp.ReadFile("README.txt", actiontriggers=["small"], actions=[[printhello, paramchoice]])

print(files)


#Chunksize - used internally but can be used as a free chunking tool for large files!

with open("README.txt", mode="r") as f:
    #Prints the file in chunks of size 10 bytes.
    #Note the use as an iterator.
    for x in fp.FileChunking(f, 10): #(file, bytes per chunk)
        print(str(x))

