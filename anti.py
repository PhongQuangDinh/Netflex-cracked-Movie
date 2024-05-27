ban_start = True

def NotAdult(movie: dict):
  ban = ['hentai','virgin','nude','fuck','dick', 'sex', 'flower & snake', 'hot night', 'unexpected attraction','porn']
  overview = movie['overview'].lower()
  title = ''
  if 'title' in movie:
    title = movie['title'].lower()
  for warning in ban:
    if warning.lower() in overview or warning.lower() in title:
        return False
  return True