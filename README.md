# pypodd

## Grab podcasts from plain text .csv or OPML .xml of RSS feeds

* Run by navigating to directory containing this file and run with `./pypodd.py`
* Edit variables at top of `pypodd.py` to customise system locations
	* `destDir` defines the location that downloads should be saved to
	* `subsLoc` defines the location of the file which holds rss feeds

* The file holding RSS feeds should be a plain text `.csv` which looks like this:

```
URL, Name of Podcast
URL, Name of Podcast
...
```

e.g. 

```
http://rss.acast.com/globalpillage, Global Pillage
http://rss.acast.com/marscorp, Mars Corp
http://www.bbc.co.uk/programmes/b006qgft/episodes/downloads.rss, Open Country
http://www.bbc.co.uk/programmes/b006qnx3/episodes/downloads.rss, The Food Programme
```

* or an OPML `.xml` file which looks like this:

```xml
<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<opml version="1.0">
  <head>
    <title>Pocket Casts Feeds</title>
  </head>
  <body>
    <outline text="feeds">
      <outline type="rss" text="Hospital Records Podcast" xmlUrl="http://podcast.hospitalrecords.com/HospitalRecordsPodcast.xml" />
      <outline type="rss" text="Slow Radio" xmlUrl="https://podcasts.files.bbci.co.uk/p05k5bq0.rss" />
      <outline type="rss" text="The Heart" xmlUrl="http://feeds.theheartradio.org/TheHeartRadio" />
      <outline type="rss" text="Gardeners' Question Time" xmlUrl="https://podcasts.files.bbci.co.uk/b006qp2f.rss" />
    </outline>
  </body>
</opml>
```
