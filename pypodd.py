#!/usr/local/opt/python/libexec/bin/python

# Modules
import feedparser
import urllib.request
import listparser
import os
import sys
import csv
from progress.bar import Bar
from termcolor import colored

# Define system location variables
destDir = os.environ['HOME'] + os.sep + "Downloads" + os.sep  # Note trailing `os.sep`
subsLoc = "subscriptions.csv" 
# e.g. subsLoc = os.environ['HOME'] + os.sep + "subscriptions.csv"

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

        urllib.request.urlretrieve(url, to, update)
        self.p.finish()

# Import subscriptions list from csv containing [url, name]

if subsLoc.endswith("csv"): 
  with open(subsLoc) as f:
    subs = csv.reader(f)
    subs = list(subs)
  # Split subs into URLs and titles
  urlList = [x[0] for x in subs]    
  subList = [x[1] for x in subs]
elif subsLoc.endswith("xml"):
  with open(subsLoc) as f:
    subs = listparser.parse(f)
  urlList = [x.url for x in subs.feeds]
  subList = [x.title for x in subs.feeds] 
else: 
  print("Subscriptions list is not `.csv` or OPML `.xml`, exiting ...")
  raise SystemExit(0)


# Download all most recent episodes or a specific podcast
def menu_top():
    optListAllNo = ['All most recent episodes', 'Specific episode']  # A list of options
    count_opt = 1
    for i in optListAllNo:
        print(str(count_opt) + ") " + i) 
        count_opt += 1
    global input_all_no  # Needed in menu_one_sel()
    input_all_no = input("\nChoose an option: ")
    input_all_no = int(input_all_no)
    menu_one_sel()
    return

# `menu_top()` selection
def menu_one_sel():
    if input_all_no == 1:
        dl_all()
    elif input_all_no == 2:
        menu_two()
    else:
        input("Invalid choice, press Enter to try again...")
        menu_top()
    return

# Download all most recent episodes of a given podcast
def dl_all():
    feedList = []  # Create empty list
    for i in urlList:
        parseBar = Bar("Parsing feeds", max = len(subList))
        feedList.append(feedparser.parse(i))
        parseBar.next()
    parseBar.finish()
    ep0List = []  # Create empty lists
    name0List = []
    link0List = []
    for i in feedList:
        ep0List.append(i['entries'][0])
    for i in ep0List:
        link0List.append(i['enclosures'][0]['href'])
        name0List.append(i['title'])
    print("\n Downloading all most recent episodes")
    dlExt = ".mp3"
    for i, j in zip(link0List, name0List):
            dlName = j.replace("/", "_")
            dlFile = destDir + dlName + dlExt
            dlURL = i
            dlProg().get(dlURL, dlFile)
    print("\nFinished, exiting")
    raise SystemExit(0)
    return

# Specific podcast menu
def menu_two():
    count_subs = 1
    for i in subList:
        print(str(count_subs) + ") " + i)  # Print list of podcasts - could convert to parsed feeds later
        count_subs += 1
    input_subs = input("\nChoose a podcast [1-n]: ")  # Take input
    input_subs = int(input_subs)  # Convert input to integer
    index_subs = input_subs - 1  # For 0-base indexing
    len_subList = len(subList) - 1
    if index_subs <= len_subList:
        # Parse chosen feed
        feedChooseList = []  # Create empty list
        feedChooseList.append(urlList[index_subs])  # Fill list with URL of chosen podcast

        feedList = []  # Create empty list
        for i in feedChooseList:
            feedList.append(feedparser.parse(i))  # Fill list parsed data from URL

        # Extract episode names from parsed feed
        global nameList
        nameList = []  # Create empty list
        for i in feedList[0]['entries']:  # Fill list with names of episodes
            nameList.append(i['title'])

        # Extract episode links from parsed feed
        global linkList
        linkList = []  # Create empty list
        for i in feedList[0]['entries']:  # Fill list with episode URLs
            linkList.append(i['enclosures'][0]['href'])
        menu_three()
    elif index_subs > len_subList:
        input("Invalid choice, press Enter to try again...")
        menu_two()
    return

# For a specific podcast, download most recent episode or another named episode
def menu_three():
    count_epi_1 = 1
    optList = ['Most recent episode', 'Another episode']  # Create a list of options

    print( colored("\nMost recent episode: " + nameList[0] + "\n", "green"))  # Print name of most recent episode
    for i in optList:  # Choose between most recent or other episode
            print(str(count_epi_1) + ") " + i)
            count_epi_1 += 1
    global input_epi_1
    input_epi_1 = input("\nChoose an episode to download: ")  # Take user input
    input_epi_1 = int(input_epi_1)
    menu_three_sel()
    return

def menu_three_sel():
    count_epi_2 = 1
    len_nameList = len(nameList)
    if input_epi_1 == 1:
        print("\nDownloading most recent episode")
        dlExt = ".mp3"
        dlName = nameList[0].replace("/", "_")
        dlFile = destDir + dlName + dlExt
        dlURL = linkList[0]
        dlProg().get(dlURL, dlFile)
        menu_end()
    elif input_epi_1 == 2:
        for i in nameList:
            print(str(count_epi_2) + ") " + i)
            count_epi_2 +=1
        input_epi_2 = input("\nChoose an episode to download: ")
        input_epi_2 = int(input_epi_2) - 1
        if input_epi_2 <= len_nameList:  # Inner if statement, If user inputs a valid episode number, do stuff, otherwise, try again
            dlExt = ".mp3"
            dlName = nameList[input_epi_2].replace("/", "_")
            dlFile = destDir + dlName + dlExt
            dlURL = linkList[input_epi_2]
            dlProg().get(dlURL, dlFile)
            menu_end()
        elif input_epi_2 > len_nameList:
            input("Invalid choice, press Enter to try again...")
            menu_three_sel()
    else:
        input("Invalid choice, press Enter to try again...")
        menu_three_sel()
    return

def menu_end():
    exit_num = 1
    optList = ['Download more', 'Exit']  # Create a list of options
    for i in optList:
        print(str(exit_num) + ") " + i)
        exit_num += 1
    global input_exit
    input_exit = input("\nFinished Downloading. Get more? \n")
    input_exit = int(input_exit)
    menu_end_sel()
    return

def menu_end_sel():
    if input_exit == 1:
        menu_top()
    elif input_exit == 2:
        raise SystemExit(0)
    else:
        input("Invalid choice, press Enter to try again...")
        menu_end_sel()
    return

menu_top()


