import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import os
import csv
from datetime import datetime
import urllib.request

def save_to_csv(movies):
    page_visit_details = datetime.now().strftime("%B %d %Y, %H-%M-%S")

    file_path = 'IMDB Top-rated Movies(Visited on ' + str(page_visit_details) + ').csv'
    # write the information to a CSV file
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Rank', 'Title', 'Year', 'Director', 'Cast', 'Rating', 'Poster'])
        csv_writer.writerows(movies)
    
    # Get the absolute path of the file
    absolute_path = os.path.abspath(file_path)
    # Print the absolute path
    print("\n\n___________________________________________________________________________________________________________________________________")
    print("-----------------------------------------------------------------------------------------------------------------------------------\n\n")
    print(f'The absolute path of the CSV file is: {absolute_path}\nVisited on {page_visit_details}')

def download_image(image_url, file_path, file_name):
    full_path = file_path + file_name + '.jpg'
    os.system('cls')
    print("Accessing : ", image_url)
    print("\n\t\t\t\t\tD O W N L O A D I N G  . . .")
    print("\nSaving to : ", full_path)
    print("\n\t\t\t\t\tS A V E D . . .")
    urllib.request.urlretrieve(image_url, full_path)

def list_to_str(directors_list, members_list):
    # First converting the list into a string type..
    members_list = str(members_list)
    directors_list = str(directors_list)
    # Removing the unwanted characters from the string..
    filter_list = ['[', ']', '\'']
    for flter in filter_list:
        members_list = members_list.replace(flter, '')
        directors_list = directors_list.replace(flter, '')
    # Removing the initial and last space if exists..
    members_list = members_list.strip()
    directors_list = directors_list.strip()

    return directors_list, members_list

def directors_cast(Cast):
    # Splitting the members of a single movie and storing in a list..
    members = Cast.split(',')
    directors_list = []
    members_list = []
    for member in members:
        # Put the name in 'directors_list' list if the person is a director..
        if '(dir.)' in member:
            directors_list.append(member.replace('(dir.)', ''))
        # Put the name in 'members_list' list if the person is not a director..
        else:
            members_list.append(member)
    director, cast = list_to_str(directors_list, members_list)
    return director, cast

def get_rank(Rank):
    Rank = Rank.strip()
    return Rank[:Rank.index('.')]

def get_path():
    img_path = str(os.getcwd() + '\Posters\\')
    if os.path.exists(img_path) == True:
        return img_path
    else:
        os.mkdir(img_path)
        return img_path

def scrape(url):
    # Make an HTTP GET request to the URL..
    response = requests.get(url)
    #print(response.content)
    # Parse the HTML content of the page..
    soup = BeautifulSoup(response.text, 'html.parser')

    movies_list = []

    # For printing in a tabular format in the terminal..
    x = PrettyTable()
    x.field_names = ["Rank", "Title", "Year", "Director", "Cast", "Rating"]

    # Extract information for each movie..
    movie_table = soup.find('tbody', class_ = 'lister-list')
    for movie in movie_table.find_all('tr'):
        Rank = get_rank(movie.find('td', class_ = 'titleColumn').text)
        Title = movie.find('td', class_ = 'titleColumn').find('a').text
        Cast = movie.find('td', class_ = 'titleColumn').find('a').get('title')
        Director, Cast = directors_cast(Cast)
        Year = movie.find('td', class_ = 'titleColumn').text[-6:-2]
        Rating = movie.find('td', class_ = 'ratingColumn imdbRating').text.strip()

        image_url = movie.find('td', class_ = 'posterColumn').find('img').get('src')
        file_name = Title
        file_path = get_path()
        download_image(image_url, file_path, file_name)
        print("Position - ", Rank)

        movies_list.append([Rank, Title, Year, Director, Cast, Rating, ('\Posters\\' + file_name)])
        x.add_row([Rank, Title, Year, Director, Cast, Rating])
    # Printing in tabular format in the terminal..
    print(x)

    # Saving as csv..
    save_to_csv(movies_list)

# The URL to scrape..
url = 'https://www.imdb.com/chart/top'

if __name__ == "__main__":
    #display(url)
    #save_to_csv(url)
    scrape(url)