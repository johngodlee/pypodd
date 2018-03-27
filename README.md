# pypodd

## Grab podcasts from csv of rss feeds

* Run with `./pypodd.py`
* Edit variables at top of `pypodd.py`
	* `destDir` defines the location that downloads should be saved to
	* `subsLoc` defines the location of the file which holds rss feeds

* The file holding rss feeds should look like this:

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
