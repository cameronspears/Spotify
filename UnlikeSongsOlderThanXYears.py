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

def get_liked_songs_ids_and_unlike(years):
    threshold_date = (datetime.datetime.now() - datetime.timedelta(days=years*365)).isoformat(timespec='seconds') + "Z"
    total_songs = sp.current_user_saved_tracks()['total']
    batch_size = 50
    removed_songs_count = 0

    for offset in range(total_songs - batch_size, -batch_size, -batch_size):
        results = sp.current_user_saved_tracks(limit=batch_size, offset=max(0, offset))
        for idx, item in enumerate(results['items'][::-1]):  # Reverse the order
            track = item['track']
            added_at = item['added_at']
            if added_at < threshold_date:
                sp.current_user_saved_tracks_delete([track['id']])
                removed_songs_count += 1
            else:
                # Stop processing if we reach songs newer than the threshold
                return removed_songs_count

    return removed_songs_count

def main():
    years = int(input("Enter the number of years to set as the timeframe: "))
    removed_songs_count = get_liked_songs_ids_and_unlike(years)
    print(f"Removed {removed_songs_count} songs older than {years} years from liked songs.")

if __name__ == '__main__':
    main()
