# pypodd

## Grab podcasts from csv of RSS feeds

* Run by navigating to directory containing this file and run with `./pypodd.py`
* Edit variables at top of `pypodd.py` to customise system locations
	* `destDir` defines the location that downloads should be saved to
	* `subsLoc` defines the location of the file which holds rss feeds

* The file holding RSS feeds should look like this, an example is found in `subscriptions.txt`:

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


