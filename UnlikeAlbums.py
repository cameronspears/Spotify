import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime

# Replace these with your own credentials
client_id = 'SPOTIFY_CLIENT_ID'
client_secret = 'SPOTIFY_CLIENT_SECRET'
redirect_uri = 'http://localhost:8080/callback/'

# Setting up the Spotify client
scope = 'playlist-modify-public,playlist-modify-private,user-library-read,user-library-modify'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

def get_albums_with_multiple_liked_songs(min_songs_from_album):
    albums = {}
    results = sp.current_user_saved_tracks()
    while results:
        for idx, item in enumerate(results['items']):
            track = item['track']
            album_id = track['album']['id']
            if album_id in albums:
                albums[album_id].append(track['id'])
            else:
                albums[album_id] = [track['id']]
        if results['next']:
            results = sp.next(results)
        else:
            results = None

    return {album_id: tracks for album_id, tracks in albums.items() if len(tracks) >= min_songs_from_album}

def remove_songs_from_albums(albums_to_remove):
    removed_songs_count = 0
    for album_id, track_ids in albums_to_remove.items():
        album = sp.album(album_id)
        print(f"Removing {len(track_ids)} songs from album '{album['name']}' by {', '.join(artist['name'] for artist in album['artists'])}")
        sp.current_user_saved_tracks_delete(track_ids)
        removed_songs_count += len(track_ids)

    return removed_songs_count

def main():
    min_songs_from_album = 5
    albums_to_remove = get_albums_with_multiple_liked_songs(min_songs_from_album)
    removed_songs_count = remove_songs_from_albums(albums_to_remove)
    print(f"Removed {removed_songs_count} songs from albums with {min_songs_from_album} or more liked songs.")

if __name__ == '__main__':
    main()
