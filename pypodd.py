#!/usr/local/opt/python/libexec/bin/python

# Modules
import feedparser
import urllib
import os
from progress.bar import Bar

# Define location variables
destDir = os.environ['HOME'] + os.sep 
subsLoc = os.environ['HOME'] + os.sep + "subscriptions" 

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


# Import subscriptions list
with open(subsLoc) as f:
	subList = f.read().splitlines()


# Get names of subscriptions
feedList = []

parseBar = Bar('Parsing feeds', max=len(subList))
for i in subList:  # Parse all feeds
    feedList.append(feedparser.parse(i))
    parseBar.next()
parseBar.finish()

feedNameList = []
for i in feedList:  # Extract names
    feedNameList.append(i['feed']['title'])
    

# Select a podcast to download, from list of subscriptions
count_subs = 1

for i in feedNameList:
	print(str(count_subs) + ") " + i)  # Print list of podcasts - could convert to parsed feeds later
	count_subs += 1
input_subs = input("\nChoose a podcast [1-n]: ")  # Take input
input_subs = int(input_subs)  # Convert input to integer

index_subs = input_subs - 1  # For 0-base indexing


# Parse chosen feed
feedChooseList = []
feedChooseList.append(feedList[index_subs])


# Extract episode names from parsed feed
nameList = []
for i in feedChooseList[0]['entries']:
    nameList.append(i['title'])


# Extract episode links from parsed feed
linkList = []
for i in feedChooseList[0]['entries']:
    linkList.append(i['enclosures'][0]['href'])


# Select episode to download - menu 1
count_epi_1 = 1
optList = ['Most recent episode', 'Another episode']  # Create a list of options

print("\nMost recent episode: " + nameList[0] + "\n")
for i in optList:
	print(str(count_epi_1) + ") " + i)
	count_epi_1 += 1
input_epi_1 = input("\nChoose an episode to download: ")
input_epi_1 = int(input_epi_1)


# Select an episode to download - menu 2
count_epi_2 = 1

if input_epi_1 == 1:
    print ("\nDownloading most recent episode")
    dlExt = ".mp3"
    dlName = nameList[0]
    dlFile = destDir + dlName + dlExt
    dlURL = linkList[0]

    dlProg().get(dlURL, dlFile)
    print("\nFinished Downloading. Exiting...")
elif input_epi_1 == 2:
    for i in nameList:
        print(str(count_epi_2) + ") " + i)
        count_epi_2 +=1
    input_epi_2 = input("\nChoose an episode to download: ")
    input_epi_2 = int(input_epi_2) - 1	

    dlExt = ".mp3"
    dlName = nameList[input_epi_2]
    dlFile = destDir + dlName + dlExt
    dlURL = linkList[input_epi_2]

    dlProg().get(dlURL, dlFile)
    print("\nFinished Downloading. Exiting...")
else:
    print ("Invalid choice, exiting...")

