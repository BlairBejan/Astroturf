from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import sqlite3
import datetime

#Should work for any subreddit, just change the URL
USERURL = "https://old.reddit.com/u/"
URL = "https://old.reddit.com/r/uspolitics/new/"


#Reddit blocks requests without a user agent, so we need to fake one
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
def startScrape():
    #Get the page and parse it
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    #Find all posts on the page
    posts = soup.find_all('div', class_='thing')

    for post in posts:
        comments_element = post.find('a', class_='bylink comments may-blank')
        
        # Posts without comments are all paid advertisements and therefore not saved
        if comments_element is not None:
            reddit_post_id = post['data-fullname'].split('_')[-1]
            title = post.find('p', class_='title').a.text
            url = urljoin(URL, post.find('p', class_='title').a['href'])
            author_name = post.find('p', class_='tagline').a.text
            upvotes = post.find('div', class_='score unvoted').text
            
            comments_url = urljoin(URL, comments_element['href'])
            author_url = urljoin(USERURL, author_name)
            
            saveUserDB(author_name)
            
            print(author_name)
            print(author_url)
            print(upvotes)
            print(post_id)


def savePostDB(title, url, comments_url, upvotes, reddit_post_id, author_name):
    # Connect to the database
    conn = sqlite3.connect('astroturf.db')
    c = conn.cursor()
    c.execute("SELECT userid FROM users WHERE username = ?", (author_name,))
    result = c.fetchone()
    userid = result[0]
    date_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO posts (title, url, comments_url, upvotes, date_created, reddit_post_id, userid) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                (title, url, comments_url, upvotes, date_created, reddit_post_id, userid))
    conn.commit()
    
def saveUserDB(username):
    conn = sqlite3.connect('astroturf.db')
    c = conn.cursor()
    date_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO users (username, account_creation_date) VALUES (?, ?)",
                (username, date_created))
    conn.commit()














    # i have url for comments, but i need to get the comments
    
    # i have url for author, but i need to get to the author    
    
    # TO CHECK IF THE POST HAS ALREADY BEEN PARCED AND ADDED TO THE DATABASE BEFORE THE FUNCTION IS RAN WE CAN SELECT THE LAST 10 
    # or so posts from the database and check each post against the post id, it is probably going to be better to use reddits system
    # for the id in our database as well instead of auto incrementing, we should do the same thing for comments, and users it doesnt really,
    # matter because the username itself will be unique
        
