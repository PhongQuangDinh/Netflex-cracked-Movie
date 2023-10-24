import requests
import random

TMDB_API_KEY = "972fc764bfdda5b9d34821a243adc607"
account_id = 20574151

# def generate_rebrandly_link(vidsrc_to_link):
#   url = f""
#   # Return the custom redirect link.
#   return custom_redirect_link.short_url

def fetch_movie_data(movie_id):
  url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
  # url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}"
  if type(movie_id) == str and not movie_id.isdigit():
    movie_id = movie_id.replace(' ','+')
    # print(movie_id)
    url = f"https://api.themoviedb.org/3/search/movie?query={movie_id}&api_key={TMDB_API_KEY}"
    # response = requests.get(url)
    # movie_data = response.json()
    # print(movie_data["title"])
    # url = f"https://api.themoviedb.org/3/movie/{movie_data['id']}?api_key={TMDB_API_KEY}"
  
  print(url)
  response = requests.get(url)
  # rep = requests.get(f"https://api.themoviedb.org/3/account/{account_id}")
  movie_data = response.json()
  # print(movie_data["title"])
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
      if type(value) == str: movie_data = fetch_movie_data(str(value))
      else: movie_data = fetch_movie_data(int(value))
  else:
      movie_data = fetch_movie_data(166426) # 878 # random.randint(1, 99999)
  # Render the template with the movie data
  return render_template("moviedbTest.html", movie_data=movie_data)

@app.route("/watchMovie", methods=['POST','GET'])
def WatchMovie():
  # bla bla bla
  id = request.form.get("I clicked it")
  
  movie_data = fetch_movie_data(id) # 878
  
  video_url = f"https://api.themoviedb.org/3/movie/{id}/videos?api_key={TMDB_API_KEY}"
  video_data = requests.get(video_url).json()
  
  watch_provider = f'https://api.themoviedb.org/3/movie/{id}/watch/providers?api_key={TMDB_API_KEY}'
  watch_data = requests.get(watch_provider).json()
  
  vidsrc_url = f"https://vidsrc.to/embed/movie/{movie_data['id']}"
  print(vidsrc_url)
  
  return render_template("watchMovie.html", movie_data=movie_data, video_data=video_data, watch_data = watch_data, vid_url = vidsrc_url)

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')