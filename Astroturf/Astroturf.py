from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import sqlite3
import datetime

#Should work for any subreddit, just change the URL



#Reddit blocks requests without a user agent, so we need to fake one

def startScrape():
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    USERURL = "https://old.reddit.com/u/"
    URL = "https://old.reddit.com/r/uspolitics/new/"
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
            
            #save all relevant data to the database
            saveUserDB(author_name)
            savePostDB(title, url, comments_url, upvotes, reddit_post_id, author_name)
            
            #switch to parcing comments
            response = requests.get(comments_url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            comments = soup.find_all('div', class_='entry unvoted')
            for comment in comments:
                comment_div = comment.find('div', class_='md')
                if comment_div is not None:
                    comment_content = comment.find('div', class_='md').get_text()
                    comment_author = comment.find('a', class_='author').text
                    comment_author_url = urljoin(USERURL, comment_author)
                    print (comment_content)
                    saveCommentDB(comment_content, comment_author, reddit_post_id)
            
            print(author_name)
            print(author_url)
            print(upvotes)
            

            


def savePostDB(title, url, comments_url, upvotes, reddit_post_id, author_name):
    conn = sqlite3.connect('reddit.db')
    c = conn.cursor()

    # Check if a post with the given reddit_post_id already exists
    c.execute("SELECT * FROM posts WHERE reddit_post_id = ?", (reddit_post_id,))
    result = c.fetchone()

    if result is not None:
        # If the post already exists, update the upvote count
        c.execute("UPDATE posts SET upvotes = ? WHERE reddit_post_id = ?", (upvotes, reddit_post_id))
    else:
        # If the post doesn't exist, insert a new row
        c.execute("SELECT userid FROM users WHERE username = ?", (author_name,))
        result = c.fetchone()
        userid = result[0]
        date_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO posts (title, url, comments_url, upvotes, date_created, reddit_post_id, userid) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                    (title, url, comments_url, upvotes, date_created, reddit_post_id, userid))

    conn.commit()
    
def saveUserDB(username):
    conn = sqlite3.connect('reddit.db')
    c = conn.cursor()

    # Check if a user with the given username already exists
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    result = c.fetchone()

    if result is None:
        # If the user doesn't exist, insert a new row
        date_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO users (username, account_creation_date) VALUES (?, ?)",
                    (username, date_created))

    conn.commit()


def saveCommentDB(comment_content, comment_author, reddit_post_id):
    conn = sqlite3.connect('reddit.db')
    c = conn.cursor()

    # Look up the reddit_post_id and userid from the database
    c.execute("SELECT id FROM posts WHERE reddit_post_id = ?", (reddit_post_id,))
    post_id_result = c.fetchone()

    c.execute("SELECT userid FROM users WHERE username = ?", (comment_author,))
    user_id_result = c.fetchone()

    if post_id_result is not None and user_id_result is not None:
        post_id = post_id_result[0]
        user_id = user_id_result[0]

        # Save the comment content, reddit_post_id, and userid to the database
        date_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO comments (content, date_created, post_id, user_id) VALUES (?, ?, ?, ?)",
                    (comment_content, date_created, post_id, user_id))

    conn.commit()

    
startScrape()




