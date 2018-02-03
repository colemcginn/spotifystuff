import sys
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from collections import OrderedDict
from datetime import datetime
import numpy
from sklearn.naive_bayes import MultinomialNB

client_id = 'c5c313824e2d4d55af503c4fcde096ab'
client_secret = 'b9d0930596134732a657981a7bcaab69'
redirect_uri = 'http://localhost:8888/callback'

client_credentials_manager = SpotifyClientCredentials(client_id,client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

scope = 'user-follow-read user-library-read user-top-read playlist-read-private playlist-modify-public playlist-modify-private'
# scope = 'user-library-read'

def predict(testingMatrix,ratingMatrix):
  ratingsReturn = [0 for i in range(6)]
  ratings = [[0 for i in range(6)] for j in range(30)]

  for x in range(30):
    maxD = 99999
    avgD = 0
    diff = [[0 for i in range(6)] for j in range(50)]
    for y in range(50):
      # maxD = 99999
      # diff = 0
      for z in range(6):
          diff[y][z] = abs(testingMatrix[x][z] - ratingMatrix[y][z])

    for p in range(6):
      for q in range(50):
        ratings[x][p] += diff[q][p]
      ratings[x][p] = ratings[x][p] / 50

  for x in range(6):
    for y in range(30):
      ratingsReturn[x] += ratings[y][x]
    ratingsReturn[x] = ratingsReturn[x] / 30

  # for x in ratings:
  #   print x

  return ratings





def getTopSongs():
  userPlaylists = sp.current_user_playlists(limit=50,offset=0)
  deleteID = ''
  for playlist in userPlaylists['items']:
    if playlist['name'] == 'Top 50 Tracks - 4 Weeks':
      deleteID = playlist['id']
      break
  # if deleteID != '':
    # sp.user_playlist_unfollow(user='fillerbil',playlist_id=deleteID)


  topTracks = sp.current_user_top_tracks(limit=50, offset=0, time_range='short_term')
  trackIDs = []
  for track in topTracks['items']:
    trackIDs.append(track['id'])
  # newPlaylist = sp.user_playlist_create(user='fillerbil',name='Top 50 Tracks - 4 Weeks',public=True)
  # # print newPlaylist
  # sp.user_playlist_add_tracks(user='fillerbil',playlist_id=newPlaylist['id'],tracks=trackIDs,position=None)
  # 
  # get info for top songs
  audioFeatures = sp.audio_features(trackIDs)
  count = 0
  w, h = 12, 50;
  ratingMatrix = [[0 for x in range(w)] for y in range(h)] 
  ratingClass = [100 for y in range(h)]
  for song in audioFeatures:
    ratingMatrix[count][0] = song['danceability']
    ratingMatrix[count][1] = song['energy']
    ratingMatrix[count][2] = song['liveness'] 
    ratingMatrix[count][3] = song['instrumentalness'] 
    ratingMatrix[count][4] = song['acousticness'] 
    ratingMatrix[count][5] = song['speechiness']
    ratingMatrix[count][6] = song['mode'] 
    ratingMatrix[count][7] = -1*song['loudness']
    ratingMatrix[count][8] = song['key']
    ratingMatrix[count][9] = song['valence']
    ratingMatrix[count][10] = song['tempo']
    # ratingMatrix[count] = rsong
    count+=1

  tracks = sp.tracks(trackIDs)
  # print tracks
  count = 0
  for song in tracks['tracks']:
    # print 'song', song
    ratingMatrix[count][11] = song['popularity']
    count+=1

  # for row in ratingMatrix:
  #   print row
  # train on top songs
  # clf = MultinomialNB()
  # clf.fit(ratingMatrix,ratingClass)
  # get discovery weekly
  userPlaylists = sp.current_user_playlists(limit=50,offset=0)
  discoverID = 0
  for playlist in userPlaylists['items']:
    if playlist['name'] == 'Discover Weekly':
      discoverID = playlist['id']
      break
  if discoverID == 0:
    print "No Discover Weekly - either move to top or doesn't exist"
    sys.exit()
  # print playlist['tracks']
  discoverPlaylist = sp.user_playlist_tracks(user='spotify',playlist_id=discoverID)
  # print discoverPlaylist['items']
  trackIDs = []
  for track in discoverPlaylist['items']:
    # print track
    trackIDs.append(track['track']['id'])

  audioFeatures = sp.audio_features(trackIDs)
  count = 0
  w, h = 12, 30;
  testingMatrix = [[0 for x in range(w)] for y in range(h)] 
  testingClass = [[0 for x in range(2)] for y in range(h)]
  for song in audioFeatures:
    testingMatrix[count][0] = song['danceability'] #0-1
    testingMatrix[count][1] = song['energy'] #0-1
    testingMatrix[count][2] = song['liveness'] #0-1 
    testingMatrix[count][3] = song['instrumentalness'] #0-1 
    testingMatrix[count][4] = song['acousticness'] #0-1
    testingMatrix[count][5] = song['speechiness'] #0-1
    testingMatrix[count][6] = song['mode'] #0/1 
    testingMatrix[count][7] = -1*song['loudness'] #0-12
    testingMatrix[count][8] = song['key'] #0-11
    testingMatrix[count][9] = song['valence'] #0-100
    testingMatrix[count][10] = song['tempo'] #0-100
    # testingMatrix[count] = rsong
    count+=1

  tracks = sp.tracks(trackIDs)
  # print tracks
  count = 0
  for song in tracks['tracks']:
    # print 'song', song
    testingMatrix[count][11] = song['popularity'] #0-100
    # print testingMatrix
    count+=1

  # predict
  ratings = predict(testingMatrix,ratingMatrix)
  

  # return individual ratings
  # count = 0
  # for track in discoverPlaylist['items']:
  #   print track['track']['name'], rating[0]

  # make overall rating
  individualRatings = [0 for i in range(30)] 
  overallRating = 0
  for x in range(30):
    for y in range(6):
      individualRatings[x] += ratings[x][y]
    individualRatings[x] = individualRatings[x] / 6
    overallRating += individualRatings[x]
  overallRating = overallRating / 30
  print 'Overll Rating: ', int(round( (1-(overallRating)) *100))

  count = 0
  for track in discoverPlaylist['items']:
    print track['track']['name'], int(round( (1-(individualRatings[count])) *100))
    count+=1




  dance = 0
  for x in range(30):
    dance += ratings[x][0]
  dance = int(round( (1-(dance / 30)) *100))
  energy = 0
  for x in range(30):
    energy += ratings[x][1]
  energy = int(round( (1-(energy / 30)) *100))
  liveness = 0
  for x in range(30):
    liveness += ratings[x][2]
  liveness = int(round( (1-(liveness / 30)) *100))
  instrum = 0
  for x in range(30):
    instrum += ratings[x][3]
  instrum = int(round( (1-(instrum / 30)) *100))
  acoustic = 0
  for x in range(30):
    acoustic += ratings[x][4]
  acoustic = int(round( (1-(acoustic / 30)) *100))
  speech = 0
  for x in range(30):
    speech += ratings[x][5]
  speech = int(round( (1-(speech / 30)) *100))

  print 'Dance:', dance
  print 'Energy:', energy
  print 'Liveness:', liveness
  print 'Instrumentalness:', instrum
  print 'Acousticness:', acoustic
  print 'Speechiness:', speech





if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    username = 'fillerbil'
    # print "Usage: %s username" % (sys.argv[0],)
    # sys.exit()

token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

if token:
  start = datetime.now()
  sp = spotipy.Spotify(auth=token)

  getTopSongs()

else:
    print "Can't get token for", username



