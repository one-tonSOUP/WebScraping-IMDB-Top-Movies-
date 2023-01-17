import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import os
import csv

def display(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    movies = soup.select('td.titleColumn')
    crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
    ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name="ir"]')]

    x = PrettyTable()
    index = 0
    x.field_names = ["S.no", "Title", "Year", "Star", "Rating"]

    for idx in range(0, len(movies)):
        movie_title = movies[idx].select('a')[0].get_text()
        movie_year = movies[idx].select('span')[0].get_text()
        movie_star = crew[idx]
        movie_rating = ratings[idx]
        index = index + 1
        x.add_row([index, movie_title, movie_year, movie_star, movie_rating])

    print(x)

def save_to_csv(url):
    # Make an HTTP GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the container element for the top 250 movies
    movie_container = soup.find('tbody', class_='lister-list')

    # Extract information for each movie
    movies = []
    index = 0
    for movie in movie_container.find_all('tr'):
        title = movie.find('td', class_='titleColumn').find('a').text
        year = movie.find('td', class_='titleColumn').find('span').text[1:-1]
        rating = movie.find('td', class_='ratingColumn imdbRating').find('strong').text
        index = index + 1
        movies.append([index, title, year, rating])

    # write the information to a CSV file
    with open('movies.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['S. No.', 'Title', 'Year', 'IMDb Rating'])
        csv_writer.writerows(movies)
    
    file_path = 'movies.csv'

    # Get the absolute path of the file
    absolute_path = os.path.abspath(file_path)

    # Print the absolute path
    print(f'The absolute path of the CSV file is: {absolute_path}')

def directors_cast(Cast):
    members = Cast.split(',')
    direc = []
    mem = []
    for member in members:
        if '(dir.)' in member:
            direc.append(member.replace('(dir.)', ''))
        else:
            mem.append(member)
    mem = str(mem)
    direc = str(direc)
    filter_list = ['[', ']', '\'']
    for flter in filter_list:
        mem = mem.replace(flter, '')
        direc = direc.replace(flter, '')
    mem = mem.strip()
    direc = direc.strip()
    #print("Director : ", direc)
    #print("Cast : ", mem)
    return direc, mem

def getRank(Rank):
    Rank = Rank.strip()
    return Rank[:Rank.index('.')]

def test(url):
    response = requests.get(url)
    #print(response.content)
    #print("\n\n___________________________________________________________________________________________________________________________________")
    #print("-----------------------------------------------------------------------------------------------------------------------------------\n\n")
    soup = BeautifulSoup(response.text, 'html.parser')
    x = PrettyTable()
    x.field_names = ["Rank", "Title", "Year", "Director", "Cast", "Rating"]
    movie_table = soup.find('tbody', class_ = 'lister-list')
    for movie in movie_table.find_all('tr'):
        #print(str(movie.find('td', class_ = 'titleColumn').text).strip()[0])
        Rank = getRank(movie.find('td', class_ = 'titleColumn').text)
        Title = movie.find('td', class_ = 'titleColumn').find('a').text
        Cast = movie.find('td', class_ = 'titleColumn').find('a').get('title')
        Director, Cast = directors_cast(Cast)
        Year = movie.find('td', class_ = 'titleColumn').text[-6:-2]
        Rating = movie.find('td', class_ = 'ratingColumn imdbRating').text
        x.add_row([Rank, Title, Year, Director, Cast, Rating])
        #print(Rank, ', ', Title, ', ', Year, ', ', Director, ', ', Cast, ', ', Rating)
    print(x)
    #print(movie_table)
    #print(soup.encode("utf-8"))

url = 'https://www.imdb.com/chart/top'

#display(url)
#save_to_csv(url)
test(url)