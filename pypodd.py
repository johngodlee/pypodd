#!/usr/local/opt/python/libexec/bin/python

# Modules
import feedparser
import urllib
import os
import csv
from progress.bar import Bar

# Define system location variables
destDir = os.environ['HOME'] + os.sep + "Downloads" + os.sep  # Note trailing `os.sep`
subsLoc = "subscriptions.txt" 
# e.g. subsLoc = os.environ['HOME'] + os.sep + "subscriptions.txt"

# Define progress bar class for urllib.urlretrieve()
class dlProg:
    def get(self, url, to):
        self.p = None

        def update(blocks, bs, size):
            if not self.p:
                self.p = Bar(to, max=size)
            else:
                if size < 0:
                    self.p.update()
                else:
                    self.p.goto(blocks * bs)

        urllib.urlretrieve(url, to, update)
        self.p.finish()

# Import subscriptions list from csv containing [url, name]
with open(subsLoc) as f:
    subs = csv.reader(f)
    subs = list(subs)

# Split subs into URLs and titles
urlList = [x[0] for x in subs]    
subList = [x[1] for x in subs]

# Select a podcast to download, from list of subscriptions
count_subs = 1
input_exit = 1

while input_exit != 2:  # Terminate program if input_exit == 2
    for i in subList:
        print(str(count_subs) + ") " + i)  # Print list of podcasts - could convert to parsed feeds later
        count_subs += 1
    input_subs = input("\nChoose a podcast [1-n]: ")  # Take input
    input_subs = int(input_subs)  # Convert input to integer
    index_subs = input_subs - 1  # For 0-base indexing

    # Parse chosen feed
    feedChooseList = []  # Create empty list
    feedChooseList.append(urlList[index_subs])  # Fill list with URL of chosen podcast

    feedList = []  # Create empty list
    for i in feedChooseList:
        feedList.append(feedparser.parse(i))  # Fill list parsed data from URL

    # Extract episode names from parsed feed
    nameList = []  # Create empty list
    for i in feedList[0]['entries']:  # Fill list with names of episodes
        nameList.append(i['title'])

    # Extract episode links from parsed feed
    linkList = []  # Create empty list
    for i in feedList[0]['entries']:  # Fill list with episode URLs
        linkList.append(i['enclosures'][0]['href'])

    # Select episode to download - most recent or other - menu 1
    count_epi_1 = 1
    optList = ['Most recent episode', 'Another episode']  # Create a list of options

    print("\nMost recent episode: " + nameList[0] + "\n")  # Print name of most recent episode
    for i in optList:  # Choose between most recent or other episode
            print(str(count_epi_1) + ") " + i)
            count_epi_1 += 1
    input_epi_1 = input("\nChoose an episode to download: ")  # Take user input
    input_epi_1 = int(input_epi_1)

    # Select an episode to download - menu 2
    count_epi_2 = 1
    count_epi_3 = 1
    len_nameList = len(nameList)

    if input_epi_1 == 1:  # Outer if statement, if user inputs 1 or 2, do stuff, otherwise, return to beginning
        print ("\nDownloading most recent episode")
        dlExt = ".mp3"
        dlName = nameList[0]
        dlFile = destDir + dlName + dlExt
        dlURL = linkList[0]
        dlProg().get(dlURL, dlFile)
        optList = ['Download more', 'Exit']  # Create a list of options
        for i in optList:  # Give option to download more podcasts (return to main menu or exit
            print(str(count_epi_2) + ") " + i)
            count_epi_2 += 1
        input_exit = input("\nFinished Downloading. Get more?")
        input_exit = int(input_exit)
    elif input_epi_1 == 2:
        for i in nameList:
            print(str(count_epi_2) + ") " + i)
            count_epi_2 +=1
        input_epi_2 = input("\nChoose an episode to download: ")
        input_epi_2 = int(input_epi_2) - 1
        if input_epi_2 <= len_nameList:  # Inner if statement, If user inputs a valid episode number, do stuff, otherwise, try again
            dlExt = ".mp3"
            dlName = nameList[input_epi_2]
            dlFile = destDir + dlName + dlExt
            dlURL = linkList[input_epi_2]
            dlProg().get(dlURL, dlFile)
            optList = ['Download more', 'Exit']  # Create a list of options
            for i in optList:
                print(str(count_epi_3) + ") " + i)
                count_epi_3 += 1
            input_exit = input("\nFinished Downloading. Get more?")
            input_exit = int(input_exit)
        else:
            raw_input("Invalid choice, press Enter to try again...")
    else:
        raw_input("Invalid choice, press Enter to try again...")
