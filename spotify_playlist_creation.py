# Creates a Spotify playlist based on a user inputted string
# -------------------------------------------------------------------------------------------------------------------#
# Imports
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import string
# -------------------------------------------------------------------------------------------------------------------#
# Spotify Login And Authentication

scope = 'playlist-modify-public'
username = 'spotify-username-here'

token = SpotifyOAuth(client_id='spotify-client-id-here', client_secret='spotify-client-secret-here',
                     redirect_uri='http://127.0.0.1:8080/', scope=scope, username=username)

# Spotify Object
spotifyObject = spotipy.Spotify(auth_manager=token)  
# -------------------------------------------------------------------------------------------------------------------#
# Functions

def StringSplit(string):
    # This function splits the user inputted message into a list with each separate word.
    string_split = string.split(' ')
    return string_split
# -------------------------------------------------------------------------------------------------------------------#

def punctuationStripping(messageList):
    # This function strips any punctuation from any of the words within the user inputted message.
    for i in range(len(messageList)):
        messageList[i] = messageList[i].strip().translate(str.maketrans('', '', string.punctuation))
    return messageList
# -------------------------------------------------------------------------------------------------------------------#

def song_iteration(result, word):
    # This function parses through the spotify search results until a match is found for the inputted word/sentence.
    uri = None
    # Parses through the Spotify search results to find a match
    for i in range(len(result['tracks']['items'])):
        if result['tracks']['items'][i]['name'].strip().lower() == word.lower():
            uri = result['tracks']['items'][i]['uri']
            print('Our uri is here', uri)
            break
    return uri
# -------------------------------------------------------------------------------------------------------------------#

def song_search(word):
    error_flag = False
    # This function searches for songs through the Spotify search result.
    # Strip the word/sentencce of punctuation.
    word = word.strip().translate(str.maketrans('', '', string.punctuation))
    print(f'\nSearching for song with "{word}"')
    uri = None
    print('\nsearching results for a match...')
    offsetLimit = False
    # The offset refers to the number of search results passed by.
    offset = 0
    while offsetLimit is False:
        try:
            result = spotifyObject.search(q=word,offset=offset,limit=50, type='track')
        
            uri = song_iteration(result, word)
            if uri != None:
                offsetLimit = True
            else:
                pass
            
        except:
            print('Invalid search query!')

        offset  += 50
        if  offset > 250:
            offsetLimit = True

    print(word , uri)
    if len(StringSplit(word)) <= 1 and uri is None:
        error_flag = True
    else:
        pass

    return uri,error_flag,word
# -------------------------------------------------------------------------------------------------------------------#
# Playlist Creation

class creation():
    def SpotifyPlaylistCreation(message_input):

        # Defining the playlist name and description
        playlist_name = 'Your-Playlist'
        playlist_description = 'Your own automated playlist'

        # Stripping the user inputted string of punctuation and gathering each word into a list.
        message_list = punctuationStripping(StringSplit(message_input))
        print(message_list)
        uri_append_list = list()
        creatingPlaylist = True
        count = 0
        # We grab the first three words of the string and once a word is matched it is removed from the string. 
        while creatingPlaylist is True:
            message_list_loop = message_list[count:]
            if count != len(message_list):
                try:
                    message_list_iterate = message_list_loop[:3]
                except:
                    message_list_iterate = message_list_loop[:]
                    if len(message_list_iterate) == 0:
                        creatingPlaylist = False
                        break

                for i in range(len(message_list_iterate)):
                    print(i)
                    uri, errorflag,word = song_search(' '.join(message_list_iterate[:len(message_list_iterate) - i]))
                    if errorflag is True:
                        print(f'The word "{word}" was not found as a song!')
                        creatingPlaylist = False
                        break
                    elif uri is None:
                        pass
                    else:
                        uri_append_list.append(uri)
                        count += len(message_list_iterate) - i
                        print(count)
                        break
            else:
                creatingPlaylist = False

        # Creating the playlist
        if errorflag == False:
            print(uri_append_list)
            if len(uri_append_list) < 1:
                print('There are no songs to match your input.\n A playlist has not been created.')
            else:
                # The playlist is created...
                spotifyObject.user_playlist_create(user=username, name=playlist_name, description=playlist_description, public=True)
                prePlaylist = spotifyObject.user_playlists(user=username)
                playlist = prePlaylist['items'][0]['id']

                print(playlist)
                print(uri_append_list)

                # Adds the matched songs to the playlist
                spotifyObject.playlist_add_items(playlist_id=playlist, items=uri_append_list)

                playlist_list = spotifyObject.user_playlists(user=username,limit=5)


                spotifyObject.current_user_unfollow_playlist(playlist_list['items'][0]['id'])

                # Return the link to the Spotify playlist and whether theres any errors
                return str(playlist_list['items'][0]['external_urls']['spotify']), errorflag

        else:
            # Return the link to the Spotify playlist and whether theres any errors
            # In this case there is no link as there was a word that wasn't matched!
            print(f'The word "{word}" was inputted which does not have a song!\nPlease try again!')
            return None, errorflag 
