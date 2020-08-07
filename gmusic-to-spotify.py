import csv
import sys
import pprint
import argparse
import itertools

import spotipy
import spotipy.util as util

try:
    import localconfig
except ImportError:
    print("""Create localconfig.py:
client_id = 'aaaaaaaaaaaabbbbbbbccccccccccccc'
client_secret = '1111122222233333444fffaaaeeeeeee'
username = 'blah.username.they.are.all..taken'
""", file=sys.stderr)
    sys.exit(1)

scope = 'user-library-modify'
client_id = localconfig.client_id
client_secret = localconfig.client_secret
username = localconfig.username
redirect_uri = 'http://localhost/'

def login():
    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    if not token:
        raise Exception("Login failed")
    sp = spotipy.Spotify(auth=token)
    return sp

def load(csvfile, sp):
    artist_album = set()
    rows = csv.reader(csvfile)
    for title,artist,album,track,duration,id,idtype,playcount,rating,year,genre,notes,playlist in rows:
        if not artist_album and album == 'album':
            # header line
            continue
        artist_album.add( (artist, album) )

    artist_album = sorted(artist_album)

    for counter, (artist,album) in enumerate(artist_album,1):
        print('Processing {}/{} {} - {}\n'.format(counter, len(artist_album), artist, album))

        albums_data = sp.search('{} - {}'.format(artist, album), type='album')\
                .get('albums').get('items')
        filtered_data = [p for p in albums_data if p.get('album_type') != 'single']

        if len(filtered_data) == 0:
            print('WARNING: No albums found for {} - {}, continuing'.format(artist, album))
            continue

        selection = 0
        if len(filtered_data) > 1:
            print('More than one source found, select from the following (. to skip):\n')
            for count,p in enumerate(filtered_data,1):
                external_url = p.get('external_urls')
                al_name = p.get('name')
                al_artists = p.get('artists')
                artists = "No artist"
                if al_artists:
                    artists = [a['name'] for a in al_artists]
                print('[{}] {} {} {} {}'.format(count, external_url, al_name, artists, p.get('release_date')))
            selection = input('\nSelection: ')
            if selection == '.':
                continue

        sel = int(selection)-1
        album_to_add = filtered_data[sel]

        print()
        print(album_to_add.get('uri'))
        #sp.current_user_saved_albums_add([album_to_add.get('uri')])

        print('\n{}\n'.format('*' * 20))

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)

def add(infile, sp):
    uris = (u.strip() for u in infile)
    for g in grouper(uris, 15):
        toload = [u for u in g if u]
        print(toload)
        sp.current_user_saved_albums_add(toload)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--add', '-a', type=argparse.FileType('r'))
    parser.add_argument('--load', '-l', type=argparse.FileType('r'))
    args = parser.parse_args()

    if not args.add or args.load:
        print("Need --add or --load")

    sp = login()

    if args.load:
        load(args.load, sp)

    if args.add:
        add(args.add, sp)
        

if __name__ == '__main__':
    main()
