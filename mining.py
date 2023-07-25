import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time

def get_random_user_id():
    url = "https://www.imdb.com/chart/moviemeter"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    user_links = soup.find_all("a", href=True, attrs={"class": "hover-over-ellipsis"})
    print(user_links)
    random_link = random.choice(user_links)
    user_id = random_link['href'].split('/')[2]
    return user_id

def get_user_ratings(user_id):
    url = f"https://www.imdb.com/user/{user_id}/ratings"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    rating_items = soup.find_all("div", class_="lister-item-content")
    ratings = []
    for item in rating_items:
        title = item.find("a").text
        rating = float(item.find("span", class_="ipl-rating-star__rating").text)
        date = item.find("span", class_="lister-item-year text-muted unbold").text.strip()
        if int(date[-5:-1]) >= 2020 and int(date[-5:-1]) <= 2022:
            ratings.append([user_id, title, rating, date])
    return ratings

def save_ratings_to_csv(ratings):
    df = pd.DataFrame(ratings, columns=["User ID", "Movie Title", "Rating", "Date"])
    df.to_csv("imdb_ratings.csv", mode='a', header=False, index=False)

if __name__ == '__main__':
    user_id = get_random_user_id()
    ratings = get_user_ratings(user_id)
    while len(ratings) <= 20:
        user_id = get_random_user_id()
        ratings = get_user_ratings(user_id)
    save_ratings_to_csv(ratings)
    print(f"Saved {len(ratings)} ratings from user {user_id} to imdb_ratings.csv.")
    time.sleep(1)
