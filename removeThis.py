import requests
TMDB_API_KEY = "972fc764bfdda5b9d34821a243adc607"
account_id = 20574151

def check(text):
  if text.endswith(",\n"):
    return text[:-2] + ";\n"
  else:
    return text

def checkContent(text):
  new_text = ""
  for char in text:
    if char == '"':
      new_text += "'"
    else:
      new_text += char
  return new_text

# remove this shit too
genre = {"Action": 1,
"Adventure":2,
"Animation":3,
"Comedy":4,
"Crime":5,
"Documentary":6,
"Drama":7,
"Family":8,
"Fantasy":9,
"History":10,
"Horror":11,
"Music":12,
"Mystery":13,
"Romance":14,
"Science Fiction":15,
"Thriller":16,
"TV Movie":17,
"War":18,
"Western":19,
"Action & Adventure":20,
"Kids":21,
"News":22,
"Reality":23,
"Sci-Fi & Fantasy":24,
"Soap":25,
"Talk":26,
"War & Politics":27}

cnt = 0
season_cnt = 0

def removeThisAtTheEnd(movie_data, video_data): # for movie
  global cnt
  cnt += 1
  #---------JUST FOR DATA ONLY --------------
  FileWrite = open("dbScript.sql","a",encoding="utf-8")
  command = '''
  insert into Movie (title,release_date,rating ,overview ,length ,country ,backdrop_path ,poster_path ,isSeries ,video_link)
  values {0}
  '''
  country = ''
  for i in movie_data['production_countries']:
    country = i['name']
  poster = f"https://image.tmdb.org/t/p/original/{movie_data['poster_path']}"
  backdrop = f"https://image.tmdb.org/t/p/original/{movie_data['backdrop_path']}"
  shit = '''("{0}",'{1}',{2},"{3}",{4},"{5}","{6}","{7}",0,null);'''
  title = checkContent(movie_data['original_title'])
  overview = checkContent(movie_data['overview'])
  # temp = f"('{movie_data['original_title']}','{movie_data['release_date']}',{int(movie_data['vote_average'])},'{movie_data['overview']}',{movie_data['runtime']},'{country}','{backdrop}','{poster}',0,null);"
  temp = shit.format(title,movie_data['release_date'], int(movie_data['vote_average']), overview, movie_data['runtime'], country, backdrop, poster)
  FileWrite.write(command.format(temp))
  
  #-------------Genre--------------------
  command = '''
  insert into Genre_Movie (genre, movie)
  values {0}
  '''
  t = 0
  temp = ''
  for i in movie_data['genres']:
    t += 1
    genre_id = genre[i['name']]
    temp += f'({genre_id},{cnt})'
    temp += ',\n' if t != len(movie_data['genres']) else ';\n'
  FileWrite.write(command.format(temp))
  #-------------Trailer-----------------
  command = '''
  insert into MovieTrailer (movie,trailer_link)
  values {0}
  '''
  t = 0
  temp = ''
  avoid = 0
  for video in video_data['results']:
    t += 1
    if "Official Trailer" not in video['name'] and "Trailer" not in video['name']: continue
    avoid += 1
    link = f"https://www.youtube.com/embed/{video['key']}"
    temp += f"({cnt},'{link}')"
    temp += ',\n' if t != len(video_data['results']) else ';\n'
  temp = check(temp)
  if avoid > 0:
    FileWrite.write(command.format(temp))
  

def removeThisAtTheEnd2(movie_data, video_data): # for series
  global cnt
  cnt += 1

  #---------JUST FOR DATA ONLY --------------
  FileWrite = open("dbScript.sql","a",encoding="utf-8")
  command = '''
  insert into Movie (title,release_date,rating ,overview ,length ,country ,backdrop_path ,poster_path ,isSeries ,video_link)
  values {0}
  '''
  country = ''
  for i in movie_data['production_countries']:
    country = i['name']
  runtime = 0 if len(movie_data['episode_run_time']) == 0 else movie_data['episode_run_time'][0]
  poster = f"https://image.tmdb.org/t/p/original/{movie_data['poster_path']}"
  backdrop = f"https://image.tmdb.org/t/p/original/{movie_data['backdrop_path']}"
  shit = '''("{0}",'{1}',{2},"{3}",{4},"{5}","{6}","{7}",1,null);'''
  title = checkContent(movie_data['original_name'])
  overview = checkContent(movie_data['overview'])
  # temp = f"('{movie_data['original_name']}','{movie_data['first_air_date']}',{int(movie_data['vote_average'])},'{movie_data['overview']}',{runtime},'{country}','{backdrop}','{poster}',1,null);"
  temp = shit.format(title,movie_data['first_air_date'],int(movie_data['vote_average']),overview,runtime, country, backdrop, poster)
  FileWrite.write(command.format(temp))
  #-------------Genre--------------------
  command = '''
  insert into Genre_Movie (genre, movie)
  values {0}
  '''
  t = 0
  temp = ''
  for i in movie_data['genres']:
    t += 1
    genre_id = genre[i['name']]
    temp += f'({genre_id},{cnt})'
    temp += ',\n' if t != len(movie_data['genres']) else ';\n'
  FileWrite.write(command.format(temp))
  
  #-------------Trailer-----------------
  command = '''
  insert into MovieTrailer (movie,trailer_link)
  values {0}
  '''
  t = 0
  temp = ''
  avoid = 0
  for video in video_data['results']:
    t += 1
    if "Official Trailer" not in video['name'] and "Trailer" not in video['name']: continue
    avoid += 1
    link = f"https://www.youtube.com/embed/{video['key']}"
    temp += f"({cnt},'{link}')"
    temp += ',\n' if t != len(video_data['results']) else ';\n'
  temp = check(temp)
  if avoid > 0:
    FileWrite.write(command.format(temp))
  
  #--------------Season-Episode-------------------
  command = '''
  insert into Season (`name`,air_date,season_number,average_rating,poster_path,movie)
  values {0}
  '''
  command1 = '''
  insert into Episode (title,overview,length,rating,season,video_link, episode_number)
  values {0}
  '''
  t = 0
  temp = ''
  temp1 = ''
  for season in movie_data['seasons']:
    t += 1
    if season['season_number'] == 0: continue
    global season_cnt
    season_cnt += 1
    poster = f"https://image.tmdb.org/t/p/original/{season['poster_path']}"
    shit = '''('{0}','{1}',{2},{3},'{4}',{5})'''
    # f"('{season['name']}','{season['air_date']}',{season['season_number']},{int(season['vote_average'])},'{poster}',{cnt})"
    air_date = '2000-01-22' if season['air_date'] == None else season['air_date']
    season_name = checkContent(season['name'])
    temp += shit.format(season_name, air_date, season['season_number'],int(season['vote_average']),poster, cnt)
    k = 0
    series = requests.get(f"https://api.themoviedb.org/3/tv/{movie_data['id']}/season/{season['season_number']}?api_key={TMDB_API_KEY}").json()
    for episode in series['episodes']:
      k += 1
      length = 0 if episode['runtime'] == None else episode['runtime']
      shit1 = '''("{0}","{1}",{2},{3},{4},null,{5})'''
      epi_title = checkContent(episode['name'])
      epi_overview = checkContent(episode['overview'])
      # f"('{episode['name']}','{episode['overview']}',{length},{int(episode['vote_average'])},{season_cnt},null,{episode['episode_number']})"
      temp1 += shit1.format(epi_title,epi_overview,length,int(episode['vote_average']),season_cnt,episode['episode_number'])
      temp1 += ',\n' if t != len(movie_data['seasons']) or k != len(series['episodes']) else ';\n'
    
    temp += ',\n' if t != len(movie_data['seasons']) else ';\n'
    
  FileWrite.write(command.format(temp))
  FileWrite.write(command1.format(temp1))