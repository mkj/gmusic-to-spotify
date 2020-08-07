Based on https://github.com/brk3/gmusic-to-spotify

Usage:
````
gmusic-to-spotify.py --load file.csv | tee blah
grep ^spotify:album blah > toload.txt
gmusic-to-spotify.py --add toload.txt
```

You need to create `localconfig.py`, look at spotipy docs for token details.
```
client_id = 'aaaaaaaaaaaabbbbbbbccccccccccccc'
client_secret = '1111122222233333444fffaaaeeeeeee'
username = 'blah.username.they.are.all..taken'
```

`--load` expects a csv from https://github.com/soulfx/gmusic-playlist.js

```
title,artist,album,track,duration,id,idtype,playcount,rating,year,genre,notes,playlist
Troubled Air,sunn O))),Troubled Air,1,705000,Txp4txpf4vuirtbirqxidkoamfi,7,0,null,2019,Metal,,Library
Phaedra,Tangerine Dream,Dream Sequence,2,86000,Tf6qzmip5esg63s5e4hnu3x6d7i,7,0,null,1985,Rock,,Library
```

`--add` to load the list of urls like
```
spotify:album:7ALFR4o9ZXfqNVv9EOORn1
spotify:album:7A10XxbkAl4hIQRMp4NyKO
```
