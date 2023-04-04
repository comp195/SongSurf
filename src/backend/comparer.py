import requests # pip install requests
import time
from collections import Counter

#debugging
import artist
import album

### IMPORTANT API INFO ###
USER_AGENT = 'wbuop'
API_KEY = 'ebc5386ea6b0af15cae300e0da5a3af5'

headers = {
    'user-agent': USER_AGENT
}
###########################

def compare_and_output_top_5(top_tags, type, input):
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
        undesirable_tags = ["favorite albums", "albums I own", "favourite albums", "1001 Albums You Must Hear Before You Die"]
    elif (type == 'track'):
        METHOD_KEY = 'tag.getTopTracks'
        JSON_KEY_1 = 'tracks'
        additional_items = True
        
        

    # Get the 5 most common tags
    # Output is a tuple e.g. ('rap', 5) where rap appears 5 times
    counter = Counter(top_tags)
    most_common_tuples = counter.most_common(5)
    print("Most common tuples: ")
    print(most_common_tuples)

    most_common_tags = [t[0] for t in most_common_tuples if t[0] not in undesirable_tags]	# get the most common tags from the tuples
    print("Most commont tags: ")
    print(most_common_tags)

    # Add next most common tags until most_common_tags has 5 elements
    i = 0
    while len(most_common_tags) < 5:
        next_most_common_tag = counter.most_common(6+i)[5+i][0]
        if next_most_common_tag not in undesirable_tags:
            most_common_tags.append(next_most_common_tag)
            i += 1
            print("New tag added: "+next_most_common_tag)
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
    top_5_tuples = counter.most_common(5) # grab 5 most common items
    print(top_5_tuples)
    top_5_items = [t[0] for t in top_5_tuples if t[0] not in input]	# get the most common items from the tuples, skips if one of the user inputs
    print(top_5_items)

    i = 0
    while len(top_5_items) < 5:
        next_most_common_item = counter.most_common(6+i)[5+i][0]
        if next_most_common_item not in input:
            top_5_items.append(next_most_common_item)
            i += 1
            print("New item added: "+next_most_common_item)
        print("Length of artists: " + str(len(top_5_items)))
    print("New items: ")
    print(top_5_items)

    #print("Testing info retriever: ")
    #artist.get_artist_info(top_5_items[0])
    #album.get_album_info(top_5_items[0])

    return top_5_items
