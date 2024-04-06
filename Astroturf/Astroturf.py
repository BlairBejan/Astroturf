from weakref import proxy
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests

#Should work for any subreddit, just change the URL
URL = "https://old.reddit.com/r/uspolitics/new/"

#Reddit blocks requests without a user agent, so we need to fake one
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

#Get the page and parse it
response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

#Find all posts on the page
posts = soup.find_all('div', class_='thing')

#For each post, get the title, URL, and comments link
for post in posts:
    comments_element = post.find('a', class_='bylink comments may-blank')
    
    #Posts without comments are all paid advertisements and therefore not saved
    if comments_element is not None:
        title = post.find('p', class_='title').a.text
        url = urljoin(URL, post.find('p', class_='title').a['href'])
        comments_link = urljoin(URL, comments_element['href'])
        
        print(f'Title: {title}\nURL: {url}\nComments Link: {comments_link}\n')

#print(soup.prettify())
