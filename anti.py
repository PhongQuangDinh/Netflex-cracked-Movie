import os
ban_start = True

def NotAdult(movie: dict):
  temp = str(os.getenv("ANTI"))
  ban = temp.split(',')
  overview = movie['overview'].lower()
  title = ''
  if 'title' in movie:
    title = movie['title'].lower()
  for warning in ban:
    if warning.lower() in overview or warning.lower() in title:
        return False
  return True