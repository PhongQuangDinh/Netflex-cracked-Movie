import requests
import random

from anti import *
from removeThis import *

TMDB_API_KEY = "972fc764bfdda5b9d34821a243adc607"
account_id = 20574151

# def generate_rebrandly_link(vidsrc_to_link):
#   url = f""
#   # Return the custom redirect link.
#   return custom_redirect_link.short_url

def fetch_video(movie_id, type_call = 'movie'):
  url = f""

def fetch_movie_data(movie_id):
  url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
  # url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}"
  if type(movie_id) == str and not movie_id.isdigit():
    movie_id = movie_id.replace(' ','+')
    # print(movie_id)
    # url = f"https://api.themoviedb.org/3/search/movie?query={movie_id}&include_adult=&api_key={TMDB_API_KEY}" # avoid adult content, but not work idk why
    
    url = f"https://api.themoviedb.org/3/search/movie?query={movie_id}&api_key={TMDB_API_KEY}" # with adult content also
    # url = f"https://api.themoviedb.org/3/search/tv?query={movie_id}&include_adult=false&api_key={TMDB_API_KEY}"
    
    # response = requests.get(url)
    # movie_data = response.json()
    # print(movie_data["title"])
    # url = f"https://api.themoviedb.org/3/movie/{movie_data['id']}?api_key={TMDB_API_KEY}"
  
  print(url)
  response = requests.get(url)
  # rep = requests.get(f"https://api.themoviedb.org/3/account/{account_id}")
  movie_data = response.json()
  
  if 'results' in movie_data and ban_start:
    # far more better but worst in some case
    movie_data['results'] = list(filter(lambda result: result['adult'] == False and NotAdult(result), movie_data['results']))
  
  return movie_data

def fetch_series_data(series_id):
  url = f"https://api.themoviedb.org/3/tv/{series_id}?api_key={TMDB_API_KEY}"
  # url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}"
  if type(series_id) == str and not series_id.isdigit():
    series_id = series_id.replace(' ','+')
    # print(movie_id)
    # url = f"https://api.themoviedb.org/3/search/movie?query={movie_id}&include_adult=&api_key={TMDB_API_KEY}" # avoid adult content, but not work idk why
    
    url = f"https://api.themoviedb.org/3/search/tv?query={series_id}&include_adult=false&api_key={TMDB_API_KEY}"
    
    # response = requests.get(url)
    # movie_data = response.json()
    # print(movie_data["title"])
    # url = f"https://api.themoviedb.org/3/movie/{movie_data['id']}?api_key={TMDB_API_KEY}"
  
  print(url)
  response = requests.get(url)
  # rep = requests.get(f"https://api.themoviedb.org/3/account/{account_id}")
  movie_data = response.json()
  
  if 'results' in movie_data and ban_start:
    # far more better but worst in some case
    movie_data['results'] = list(filter(lambda result: result['adult'] == False and NotAdult(result), movie_data['results']))
  
  return movie_data

# Fetch the movie data for the movie with the ID 12345
# movie_data = fetch_movie_data(878)

# Print the movie title
# print(movie_data)



from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def GetUserGeneralInputMaybe():
  # Fetch the movie data for the movie with the ID 12345
  value = request.form.get('user_input')
  print(value)
  if str(value) != "None":
      # print(value)
      if type(value) == str: 
        movie_data = fetch_movie_data(str(value))
        series_data = fetch_series_data(str(value))
      else: 
        movie_data = fetch_movie_data(int(value))
        series_data = fetch_series_data(int(value))
  else:
      movie_data = fetch_movie_data(166426) # 878 # random.randint(1, 99999) # watching Pirate of the caribbean 5 instead of random
      series_data = fetch_series_data(111110)
  
  return render_template("moviedbTest.html", movie_data=movie_data, series_data=series_data)

@app.route("/watchMovie", methods=['POST','GET'])
def WatchMovie():
  # bla bla bla
  id = request.form.get("I clicked it")
  
  movie_data = fetch_movie_data(id) # 878
  
  #------this is obsolete-------------
  video_url = f"https://api.themoviedb.org/3/movie/{id}/videos?api_key={TMDB_API_KEY}"
  video_data = requests.get(video_url).json()
  #-------------OBSOLETE---------------
  
  # watch_provider = f'https://api.themoviedb.org/3/movie/{id}/watch/providers?api_key={TMDB_API_KEY}'
  # watch_data = requests.get(watch_provider).json()
  
  vidsrc_url = f"https://vidsrc.to/embed/movie/{movie_data['id']}" # one but almost good
  # vidsrc_url = f"https://vidsrc.xyz/embed/movie/{movie_data['id']}" # one but almost good
  # vidsrc_url = f"https://autoembed.to/movie/tmdb/{movie_data['id']}" # another one not very powerful
  # vidsrc_url = f"https://api.ripper.fun/v2/embed/movie?id={movie_data['id']}"
  
  print(vidsrc_url)
  
  # removeThisAtTheEnd(movie_data, video_data) # for real bruh
  
  return render_template("watchMovie.html", movie_data=movie_data, video_data=video_data, vid_url = vidsrc_url)

@app.route("/watchSeries", methods=['POST','GET'])
def WatchSeries():
  id = request.form.get("I clicked it")
  
  movie_data = fetch_series_data(id) # 878
  # print(id)
  
  #------this is obsolete-------------
  video_url = f"https://api.themoviedb.org/3/tv/{id}/videos?api_key={TMDB_API_KEY}"
  video_data = requests.get(video_url).json()
  # print(video_data)
  #------------OBSOLETE--------------
  
  # watch_provider = f'https://api.themoviedb.org/3/tv/{id}/watch/providers?api_key={TMDB_API_KEY}'
  # watch_data = requests.get(watch_provider).json()
  
  vidsrc_url = f"https://vidsrc.to/embed/tv/{movie_data['id']}"
  # vidsrc_url = f"https://show2embed.web.app/watch/{movie_data['id']}"
  # vidsrc_url = f"https://vtbe.to/embed-0ozb9c06zh6z.html"
  
  # SEASON_NUMBER = 1
  # EPISODE_NUMBER = 1
  # vidsrc_url = f"https://autoembed.to/tv/tmdb/{movie_data['id']}-{SEASON_NUMBER}-{EPISODE_NUMBER}"
  
  print(vidsrc_url)
  
  # removeThisAtTheEnd2(movie_data, video_data) # for real bruh
  
  return render_template("watchSeries.html",movie_data=movie_data, video_data=video_data, vid_url = vidsrc_url)

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')