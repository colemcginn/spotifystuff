import sys
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from collections import OrderedDict
from datetime import datetime

client_id = 'c5c313824e2d4d55af503c4fcde096ab'
client_secret = 'b9d0930596134732a657981a7bcaab69'
redirect_uri = 'http://localhost:8888/callback'
username = ""
client_credentials_manager = SpotifyClientCredentials(client_id,client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

scope = 'user-follow-read user-library-read user-top-read playlist-read-private playlist-modify-public playlist-modify-private'
# scope = 'user-library-read'

def createPlaylistShort():
  userPlaylists = sp.current_user_playlists(limit=50,offset=0)
  deleteID = ''
  for playlist in userPlaylists['items']:
    if playlist['name'] == 'Top 50 Tracks - 4 Weeks':
      deleteID = playlist['id']
      break
  if deleteID != '':
    sp.user_playlist_unfollow(user=username,playlist_id=deleteID)


  topTracks = sp.current_user_top_tracks(limit=50, offset=0, time_range='short_term')
  trackIDs = []
  for track in topTracks['items']:
    trackIDs.append(track['id'])
  newPlaylist = sp.user_playlist_create(user=username,name='Top 50 Tracks - 4 Weeks',public=True)
  # print newPlaylist
  sp.user_playlist_add_tracks(user=username,playlist_id=newPlaylist['id'],tracks=trackIDs,position=None)

def createPlaylistMedium():
  userPlaylists = sp.current_user_playlists(limit=50,offset=0)
  deleteID = ''
  for playlist in userPlaylists['items']:
    if playlist['name'] == 'Top 50 Tracks - 6 Months':
      deleteID = playlist['id']
      break
  if deleteID != '':
    sp.user_playlist_unfollow(user=username,playlist_id=deleteID)

  topTracks = sp.current_user_top_tracks(limit=50, offset=0, time_range='medium_term')
  trackIDs = []
  for track in topTracks['items']:
    trackIDs.append(track['id'])
  newPlaylist = sp.user_playlist_create(user=username,name='Top 50 Tracks - 6 Months',public=True)
  # print newPlaylist
  sp.user_playlist_add_tracks(user=username,playlist_id=newPlaylist['id'],tracks=trackIDs,position=None)

def createPlaylistLong():
  userPlaylists = sp.current_user_playlists(limit=50,offset=0)
  deleteID = ''
  for playlist in userPlaylists['items']:
    if playlist['name'] == 'Top 50 Tracks - Few Years':
      deleteID = playlist['id']
      break
  if deleteID != '':
    sp.user_playlist_unfollow(user=username,playlist_id=deleteID)

  topTracks = sp.current_user_top_tracks(limit=50, offset=0, time_range='long_term')
  trackIDs = []
  for track in topTracks['items']:
    trackIDs.append(track['id'])
  newPlaylist = sp.user_playlist_create(user=username,name='Top 50 Tracks - Few Years',public=True)
  # print newPlaylist
  sp.user_playlist_add_tracks(user=username,playlist_id=newPlaylist['id'],tracks=trackIDs,position=None)

def createRAndBPlaylistMedium():
  userPlaylists = sp.current_user_playlists(limit=50,offset=0)
  deleteID = ''
  for playlist in userPlaylists['items']:
    if playlist['name'] == 'Top R&B - 6 Months':
      deleteID = playlist['id']
      break
  if deleteID != '':
    sp.user_playlist_unfollow(user=username,playlist_id=deleteID)

  topTracks = sp.current_user_top_tracks(limit=50, offset=0, time_range='medium_term')
  trackIDs = []
  for track in topTracks['items']:
    trackIDs.append(track['id'])
  newPlaylist = sp.user_playlist_create(user=username,name='Top 50 Tracks - 6 Months',public=True)
  # print newPlaylist
  sp.user_playlist_add_tracks(user=username,playlist_id=newPlaylist['id'],tracks=trackIDs,position=None)



if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()

token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

if token:
  start = datetime.now()
  sp = spotipy.Spotify(auth=token)

  createPlaylistShort()
  createPlaylistMedium()
  createPlaylistLong()
else:
    print "Can't get token for", username



