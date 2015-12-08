#!/usr/bin/env python
import random
import re
import sys
import lib.markov as markov
from htmlentitydefs import name2codepoint as n2c
from config import *
from lib.connection import get_connection
from lib.queries import *


def entity(text):
    if text[:2] == "&#":
        try:
            if text[:3] == "&#x":
                return unichr(int(text[3:-1], 16))
            else:
                return unichr(int(text[2:-1]))
        except ValueError:
            pass
    else:
        guess = text[1:-1]
        numero = n2c[guess]
        try:
            text = unichr(numero)
        except KeyError:
            pass
    return text

def filter_message(message):
    message = re.sub(r'\b(RT|MT) .+','',message) #take out anything after RT or MT
    message = re.sub(r'(\#|@|(h\/t)|(http))\S+','',message) #Take out URLs, hashtags, hts, etc.
    message = re.sub(r'\n','', message) #take out new lines.
    message = re.sub(r'\"|\(|\)', '', message) #take out quotes.
    message = re.sub(r'\xe9', 'e', message) #take out accented e
    return message



def grab_messages(reader, channel):
    source_messages=[]
    user_messages = reader.chat_channel('singlerider')
    for message in user_messages:
        message = filter_message(message[0])
        if len(message) != 0:
            source_messages.append(message)
    return source_messages

if __name__=="__main__":
    order = ORDER
    if DEBUG==False:
        guess = random.choice(range(ODDS))
    else:
        guess = 0

    if guess == 0:
        if STATIC_TEST==True:
            file = TEST_SOURCE
            print ">>> Generating from {0}".format(file)
            string_list = open(file).readlines()
            for item in string_list:
                source_messages = item.split(",")
        else:
            source_messages = []

            for x in range(17)[1:]:
                reader = Reader()
                source_messages_iter = grab_messages(reader, 'singlerider')
                source_messages += source_messages_iter
            print "{0} messages found".format(len(source_messages))
            if len(source_messages) == 0:
                print "Error fetching messages from Twitter. Aborting."
                sys.exit()
        mine = markov.MarkovChainer(order)
        for message in source_messages:
            if re.search('([\.\!\?\"\']$)', message):
                pass
            else:
                message+="."
            mine.add_text(message)

        for x in range(0,10):
            generated_statement = mine.generate_sentence()

        #randomly drop the last word, as Horse_ebooks appears to do.
        if random.randint(0,4) == 0 and re.search(r'(in|to|from|for|with|by|our|of|your|around|under|beyond)\s\w+$', generated_statement) != None:
           print "Losing last word randomly"
           generated_statement = re.sub(r'\s\w+.$','',generated_statement)
           print generated_statement

        #if a message is very short, this will randomly add a second sentence to it.
        if generated_statement != None and len(generated_statement) < 40:
            rando = random.randint(0,10)
            if rando == 0 or rando == 7:
                print "Short message. Adding another sentence randomly"
                newer_message = mine.generate_sentence()
                if newer_message != None:
                    generated_statement += " " + mine.generate_sentence()
                else:
                    generated_statement = generated_statement
            elif rando == 1:
                #say something crazy/prophetic in all caps
                print "ALL THE THINGS"
                generated_statement = generated_statement.upper()

        #throw out messages that match anything from the source account.
        if generated_statement != None and len(generated_statement) < 110:
            for message in source_messages:
                if generated_statement[:-1] not in message:
                    continue
                else:
                    print "TOO SIMILAR: " + generated_statement
                    sys.exit()

            if DEBUG == False:
                reader = Reader()
                print generated_statement
            else:
                print generated_statement

        elif generated_statement == None:
            print "message is empty, sorry."
        else:
            print "TOO LONG: " + generated_statement
    else:
        print str(guess) + " No, sorry, not this time." #message if the random number fails.
