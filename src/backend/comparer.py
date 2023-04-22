import requests # pip install requests
import time
from collections import Counter

import database
import artist
import album
import track

### IMPORTANT API INFO ###
USER_AGENT = 'wbuop'
API_KEY = 'ebc5386ea6b0af15cae300e0da5a3af5'

headers = {
    'user-agent': USER_AGENT
}
###########################

def compare_and_output_top_50(app, user_id, top_tags, type, input):
    """
    1) Compare input tags and grab the top 5 most common tags
    2) Use the top 5 tags to request for top 50 artists, and output their names
    
    Parameters:
    tags (list): list of tags to compare to
    type (string): output type can be any of these 3 ['artist', 'album', 'track']

    Returns:
    top_5 (list): list of artists or albums or tracks
    """

    if not top_tags:    # if no tags were added to the list
        return []

    # --- PSEUDOCODE ---
    # Append tags from user's favorites to top_tags list
    # ------------------

    # ADJUST LIST AS WE DEBUG AND TEST !!!
    undesirable_tags = []   # list of tags to ignore

    if (type == 'artist'):
        METHOD_KEY = 'tag.getTopArtists'
        JSON_KEY_1 = 'topartists'
        additional_items = False
        undesirable_tags = ["seen live"]
    elif (type == 'album'):
        METHOD_KEY = 'tag.getTopAlbums'
        JSON_KEY_1 = 'albums'
        additional_items = True
        undesirable_tags = ["albums I own", "1001 Albums You Must Hear Before You Die"]
    elif (type == 'track'):
        METHOD_KEY = 'tag.getTopTracks'
        JSON_KEY_1 = 'tracks'
        additional_items = True
        undesirable_tags = []

    undesirable_tags.extend(["favorite", "favourite"]) # Universal tags

    # Get the 5 most common tags
    # Output is a tuple e.g. ('rap', 5) where rap appears 5 times
    counter = Counter(top_tags)
    most_common_tuples = counter.most_common(5)
    print("Most common tuples: ")
    print(most_common_tuples)

    most_common_tags = [t[0] for t in most_common_tuples if not any(t[0].startswith(tag) for tag in undesirable_tags)]	# get the most common tags from the tuples
    print("Most commont tags: ")
    print(most_common_tags)

    # Add next most common tags until most_common_tags has 5 elements
    i = 0
    while len(most_common_tags) < 5:
        if len(counter) >= 6+i:
            next_most_common_tag = counter.most_common(6+i)[5+i][0]
            if next_most_common_tag not in undesirable_tags:
                most_common_tags.append(next_most_common_tag)
                i += 1
                print("New tag added: "+next_most_common_tag)
        else:
            break
        print("Length of most common tags: " + str(len(most_common_tags)))
    print("New most common tags: ")
    print(most_common_tags)

    # Use the tags to search for the top artists in those tags
    # Search the top artists for those tags
    # Find the most common artists from all the tags
    # If no common artists, take the top artists from each tag in sequential order

    top_items = []

    for tag in most_common_tags:
        # Get top 50 artists for tag
        limit = 50

        payload = {
            'api_key': API_KEY,
            'method': METHOD_KEY,
            'format': 'json',
            'limit': limit,
            'tag': tag
        }

        r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)

        if (r.status_code == 200):
            items = r.json()[JSON_KEY_1][type]
            if (additional_items):
                for item in items:
                    top_items.append((item['name'],item['artist']['name'])) # add a tuple to top_items (name, artist)
            else:
                for item in items:
                    top_items.append(item['name'])
        else:
            print(f'Request failed with status code {r.status_code}')

        time.sleep(1)


    counter = Counter(top_items)
    top_50_tuples = counter.most_common(50) # grab 50 most common items
    print(top_50_tuples)

    if(type == 'artist'):
        input_lower = [i.lower() for i in input] # to account for inputs with case variations
        top_50_items = [t[0] for t in top_50_tuples if t[0].lower() not in input_lower]	# get the most common items from the tuples, skips if one of the user inputs
    else:
        input_lower = [i[0].lower() for i in input] # to account for inputs with case variations
        top_50_items = [t[0] for t in top_50_tuples if t[0][0].lower() not in input_lower]   # get the most common items from the tuples, skips if one of the user inputs
    print(top_50_items)

    i = 0
    while len(top_50_items) < 50:
        next_most_common_item = counter.most_common(6+i)[5+i][0]
        if next_most_common_item not in input:
            top_50_items.append(next_most_common_item)
            i += 1
            print("New item added: "+next_most_common_item)
        print("Length of artists: " + str(len(top_50_items)))
    print("New items: ")
    print(top_50_items)

    update_database_with_items(app, user_id, type, top_50_items)


def update_database_with_items(app, user_id, item_type, items):
    for item in items:
        if (item_type == 'artist'):
            # first check if the item exists already in database, then skip adding it, but add it to recommend

            if (database.get_artist_object(app, item) == None):

                info = artist.get_artist_info(item)
                database.add_item(app, 'artist', item, info['image'], info['description'], info['video_link'], info['url_link'])

            cur_artist = database.get_artist_object(app, item)
            database.add_recommended(app, user_id, cur_artist.artist_id, 'artist')

        elif (item_type == 'album'):
            # first check if the item exists already in database, then skip adding it, but add it to recommend
            
            if (database.get_album_object(app, item[0], item[1]) == None):
                
                # check if artist of album exists in database, if not then add it
                if (database.get_artist_object(app, item[1]) == None):
                    time.sleep(0.8)
                    artist_info = artist.get_artist_info(item[1])
                    database.add_item(app, 'artist', item[1], artist_info['image'], artist_info['description'], artist_info['video_link'], artist_info['url_link'])

                cur_artist = database.get_artist_object(app, item[1])
                (info, album_tracks) = album.get_album_info(item[0], item[1])
                # add the album
                database.add_item(app, 'album', item[0], info['image'], info['description'], info['video_link'], info['url_link'], cur_artist.artist_id)
                cur_album = database.get_album_object(app, item[0], item[1])

                """ Currently, adding every track for an album is a feature that costs to many api calls. """
                # # add tracks that belong to the album if it doesnt exist
                # for album_track in album_tracks:
                #     if (database.get_track_object(app, album_track, item[1]) == None):
                #         print("adding track: " + album_track)
                #         time.sleep(0.5)
                #         track_info = track.get_track_info(album_track, item[1])
                #         database.add_item(app, 'track', album_track, track_info['image'], track_info['description'], track_info['video_link'], track_info['url_link'], cur_artist.artist_id, cur_album.album_id)

                #     # ensure the track's album_id is correct
                #     cur_track = database.get_track_object(app, album_track, item[1])
                #     database.set_album_id(app, cur_track.track_id, cur_album.album_id)
                        
            # add the album to recommendation table
            cur_album = database.get_album_object(app, item[0], item[1])
            database.add_recommended(app, user_id, cur_album.album_id, 'album')



        elif (item_type == 'track'):
            # first check if the item exists already in database, then skip adding it, but add it to recommend

            if (database.get_track_object(app, item[0], item[1]) == None):

                
                # check if artist of track exists in database, if not then add it
                if (database.get_artist_object(app, item[1]) == None):
                    time.sleep(0.8)
                    artist_info = artist.get_artist_info(item[1])
                    database.add_item(app, 'artist', item[1], artist_info['image'], artist_info['description'], artist_info['video_link'], artist_info['url_link'])

                cur_artist = database.get_artist_object(app, item[1])
                info = track.get_track_info(item[0], item[1])
                # if album exist, then add the album
                if (info['album_name'] != 'N/A'): 
                    # check if album of track exists in database, if not then add it
                    if (database.get_album_object(app, info['album_name'], item[1]) == None):
                        (album_info, album_tracks) = album.get_album_info(info['album_name'], item[1])
                        database.add_item(app, 'album', info['album_name'], album_info['image'], album_info['description'], album_info['video_link'], album_info['url_link'], cur_artist.artist_id)

                    cur_album = database.get_album_object(app, info['album_name'], item[1])
                    # add the track
                    print(item[0])
                    print("album found!")
                    database.add_item(app, 'track', item[0], info['image'], info['description'], info['video_link'], info['url_link'], cur_artist.artist_id, cur_album.album_id)
                else:
                    # add the track
                    print(item[0])
                    print("album  NOT found!")
                    print(info['image'] + info['description'] + info['video_link'] + info['url_link'])
                    database.add_item(app, 'track', item[0], info['image'], info['description'], info['video_link'], info['url_link'], cur_artist.artist_id)
            print(item[0])
            print(item[1])
            cur_track = database.get_track_object(app, item[0], item[1])
            database.add_recommended(app, user_id, cur_track.track_id, 'track')

    
