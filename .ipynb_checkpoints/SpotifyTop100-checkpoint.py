import spotipy
from spotipy.oauth2 import SpotifyOAuth

os.environ["SPOTIPY_CLIENT_ID"] = "b3cbfb31f3354e3c9aedf34fc44cc047"
os.environ["SPOTIPY_CLIENT_SECRET"] = "e82031b1ad464df1ba4bf671ba89fc2b"

scope = "user-library-read"

#lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'
#sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
#sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)
playlist_id = "spotify:playlist:3ztyaxjpzA3533hemHWW1v"
#track_id = "spotify:track:55ooVBrLU55yIm749tVY0Z"
#album_id = "spotify:album:23sFampStN7THAa5YSgKAk"
