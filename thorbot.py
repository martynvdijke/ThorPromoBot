#-*- coding: utf-8 -*-

import csv
import sys
import PIL
from PIL import Image
from pushbullet import Pushbullet
import urllib2
import urllib
import time
import json
from datetime import datetime, timedelta
import telepot

global titletekst,tekst,lengte,tijd,location,title



def findOccurrences(s, ch):
    ch2 = ch
    working2 = True
    print("Oorspronkelijek tekst :")
    print(s)
    test = [i for i in range(len(s)) if s.startswith(ch, i)]
    test2 = [i for i in range(len(s)) if s.startswith(" ", i)]

    for q in range(0, len(test)):
        p = test[q]
        o = 0
        upper2 = 0
        upper = s[(p+o)].isupper()
        if upper == 1:
            print("We hebben hoofdletter match upper 1")
            print(s[(p+1)])
            working2 = True
        elif upper2 == 1:
            print("WE hebben hoofdletter match upper2")
            working2 = True
            print(s[(p+2)])
        elif (p+1) in test2:
            print("we hebben space match")
            print(test2)
            #print(test[(q+1)])
            working2 = True

        if working2 is True:
            print("Fixing the text")
            s = s[:(p+1+q)] + "\n" + s[(p+1+q):]
            working2 = False
            print("Gefixedte text")
            print(s)

    return s

print("Starting ... ")

def data():
    print("Refershing data")
    url = 'https://thor.edu/calendar_csv2/Calender.csv'
    data = urllib2.urlopen(url)
    cr = csv.reader(data)

    title = []
    tekst = []
    tijd = []
    location = []
    lengte = 0
    titletekst = []
    time2 = []
    #print (cr)


    for row in cr:
        #print(row)

        if row is not None:
            if 'Title' not in row[1]:
                name = row[1] #.split("</a>")
                #print(name)
                #name = name.pop()
                print(name)
                print(row[4])
                title.append(name)
                if "." in row[4]:
                            #print("Een ? gevonden")
                            teskt2 = row[4]
                            print(teskt2)
                            finaltekst = findOccurrences(teskt2, ".")

                if "!" in row[4]:
                            #print("Een . gevonden")
                            finaltekst = findOccurrences(finaltekst, "!")
                            # print(test)
                if "?" in row[4]:
                            #print("Een ! gevonden")
                            finaltekst2 = findOccurrences(finaltekst, "?")
                            # print(test)
                else:
                    finaltekst2 = row[4]

                tekst.append(finaltekst2)
                tijd.append(row[2])
                location.append(row[3])
                lengte += 1
                #print("title tekst :: ")
                print('Lengt tekst: ')
                print(len(title))

    for p in range(0, len(title)):
        if p == 0:
             titletekst = "\n - " + str(title[p])
        else :
            titletekst = str(titletekst) + "\n - " + str(title[p])
    time2 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    titletekst = titletekst # + time2
    dt = datetime.now() + timedelta(hours=12)
    return titletekst,tekst,lengte,tijd,location,title,time2,dt

titletekst,tekst,lengte,tijd,location,title,time2,dt = data()

working = 0
print("clear \n \n \n \n \n ")
print(lengte)
print(title)

def photos():
            #url = 'http://poster.thor.edu/load_filenames.php?Thor=gaaf&type=posters'
            data2 = urllib.urlopen('http://poster.thor.edu/load_filenames.php?Thor=gaaf&type=posters')
            data3 = json.loads(data2.read())
            #erg dom niet elk evenenement heeft een foto !! -> nodig om te fixen
            print(data3[1])
            baseurl =  "http://poster.thor.edu/"
            #hier loopt het mis.
            for o in range( 0, len(data3)):
                url2 = baseurl + data3[o]
                filename = str(o) + ".jpg"

                urllib.urlretrieve(url2, filename)
                basewidth = 1200
                img = Image.open(filename)
                wpercent = (basewidth/float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
                img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
                img.save(filename)
            print ("Done with the photo's")
            return data3

#data3 = photos()


def handle(msg):
    flavor = telepot.flavor(msg)

    #print 'Got command: %s' % command

    if flavor == 'chat':

        welcomtekst = "The Thor events are : \nType words of the event for more info" + "\nThe latest update of the Thor data was at : " + time2 + "\nType the reset commando in order to obtain new data"
        content_type, chat_type, chat_id = telepot.glance(msg)
        print('Normal Message:', content_type, chat_type, chat_id)
        chat_id = msg['chat']['id']
        command = msg['text']
        from2 = msg['from']
        usernname2 = from2['username']
        if command == '/thor':
            bot.sendMessage(chat_id, welcomtekst)
            #bot.sendMessage(chat_id, "Type words of the event for more info")

            bot.sendMessage(chat_id, titletekst)
        if command == '/thor@Thor_promo_bot':
            bot.sendMessage(chat_id, welcomtekst)
            bot.sendMessage(chat_id, titletekst)
        if command == '/update':
                pushtext = usernname2 + " has updated the script"
                push = pb.push_note("Thor bot", pushtext )

        #     print("Update the script")
        #     bot.sendMessage(chat_id, "Updating the script , the next server reboot will use the new script")
        #     git.Git().clone("git://github.com/martijnvandijke/Thor-promo-bot")

        if command == '/photo':
             for o in range( 0, len(data3)):
                filename = str(o) + ".jpg"
                f = open(filename, 'rb')
                bot.sendPhoto(chat_id, f)

        if command == '/poster':
            for o in range( 0, len(data3)):
                filename = str(o) + ".jpg"
                f = open(filename, 'rb')
                bot.sendPhoto(chat_id, f)

        if command == '/photo@Thor_promo_bot':
             for o in range( 0, len(data3)):
                filename = str(o) + ".jpg"
                f = open(filename, 'rb')
                bot.sendPhoto(chat_id, f)

        if command == '/poster@Thor_promo_bot':
             for o in range( 0, len(data3)):
                filename = str(o) + ".jpg"
                f = open(filename, 'rb')
                bot.sendPhoto(chat_id, f)

        if command == '/about@Thor_promo_bot':
            abouttext = "This Thor bot is made by @Martyn_van_Dijke if you want you can contribute at the github https://github.com/martijnvandijke/Thor-promo-bot \nThe bot is hosted by Frank Boerman thanks for this :) "
            bot.sendMessage(chat_id, abouttext)

        if command == '/about':
            abouttext = "This Thor bot is made by @Martyn_van_Dijke if you want you can contribute at the github https://github.com/martijnvandijke/Thor-promo-bot \nThe bot is hosted by Frank Boerman thanks for this :) "
            bot.sendMessage(chat_id, abouttext)

        if command == '/reset':
            print("Obtaining new data")
            bot.sendMessage(chat_id, "Nieuwe data binnen halen")
            pushtext = usernname2 + " has requested a reload of the data"
            push = pb.push_note("Thor bot", pushtext )
            #photos()
            global titletekst,tekst,lengte,tijd,location,title,time2,dt
            titletekst,tekst,lengte,tijd,location,title,time2,dt = data()


        if command == '/reset@Thor_promo_bot':
            print("Obtaining new data")
            bot.sendMessage(chat_id, "Nieuwe data binnen halen")
            pushtext = usernname2 + " has requested a reload of the data"
            push = pb.push_note("Thor bot", pushtext )
            #photos()
            global titletekst,tekst,lengte,tijd,location,title,time2,dt
            titletekst,tekst,lengte,tijd,location,title,time2,dt = data()

        if datetime.now() > dt:
            print ("Ik ben al 12 uur met dezelfde data ik ga refreshhen")
            pushtext = " I am going to refresh the data -> since i have been 12 hours active"
            push = pb.push_note("Thor bot", pushtext )
            photos()
            global titletekst,tekst,lengte,tijd,location,title,time2,dt
            titletekst,tekst,lengte,tijd,location,title,time2,dt = data()

        for y in range(0, lengte):
            if (command in title[y]) or (command in title[y].lower()) or (command in title[y].upper()):
                print(y)
                print(tekst[y])
                timetext = "The time of the event is : \n" + tijd[y]
                locationtext = "\nThe location of the event is : \n" + location[y]
                overalltext = timetext + locationtext
                bot.sendMessage(chat_id, tekst[y])
                bot.sendMessage(chat_id, overalltext)


    elif flavor == 'inline_query':
        articles = []
        query_id, from_id, query_string = telepot.glance(msg, flavor=flavor)
        print 'Inline Query:', query_id, from_id, query_string
        for i in range(0, len(title)):
            inlinetekst = tekst[i] + " \n \n"
            timetext = "\n The time of the event is : \n" + tijd[i]
            locationtext = "\nThe location of the event is : \n" + location[i]
            overalltext = inlinetekst + timetext + locationtext
            print overalltext
            articles = articles +  [{'type': 'article','id': str(i), 'title': str(title[i]), 'message_text': overalltext }]
            print (articles)

        bot.answerInlineQuery(query_id, articles)

    # chosen inline result - need `/setinlinefeedback`
    elif flavor == 'chosen_inline_result':
        result_id, from_id, query_string = telepot.glance(msg, flavor=flavor)
        print 'Chosen Inline Result:', result_id, from_id, query_string

        # Remember the chosen answer to do better next time

    else:
        raise telepot.BadFlavor(msg)


pb = Pushbullet('pcNx43WLJGG0ciFPu6f8v7cVb9FEFdAF')
bot = telepot.Bot('156170602:AAHuZajQzDsOrSMmkXk8CsBA-ZXdPE3h4m0')
bot.message_loop(handle)
#bot.notifyOnMessage(handle)

print 'I am listening ...'

while 1:
    time.sleep(10)
