import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# Write your code below this line 👇
response = requests.get(URL)
content = response.text

soup = BeautifulSoup(content, "html.parser")
movie_titles = soup.find_all(name="h3", class_="title")

movies = []
for movie_title in movie_titles:
    text = movie_title.getText()
    movies.append(text)

with open("movies_list.txt", "w") as movies_list:
    movies.reverse()
    for movie in movies:
        movies_list.write(movie + "\n")
print(movies)

