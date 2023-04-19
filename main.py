import praw
import random
import time
from dotenv import dotenv_values

CONFIG = dotenv_values(".env")
SUBREDDIT_NAME = 'AskReddit'
MIN_WAIT_TIME = 15
MAX_WAIT_TIME = 45
POST_LIMIT = 10

SUBJECT_LINES = [
    "How is it going?",
    "How are you?",
]
MESSAGE_TEMPLATE = """Hello {username}, How are you doing?"""

reddit = praw.Reddit(client_id=CONFIG.get("CLIENT_ID"),
                     client_secret=CONFIG.get("CLIENT_SECRET"),
                     user_agent=f"DM for Reddit (by u/{CONFIG.get('USERNAME')})",
                     username=CONFIG.get("USERNAME"),
                     password=CONFIG.get("PASSWORD"))

subreddit = reddit.subreddit(SUBREDDIT_NAME)
moderators = {mod.name for mod in subreddit.moderator()}

post_count = 0
usernames = set()

for post in subreddit.hot(limit=POST_LIMIT):
    post_count += 1
    print(f"Post {post_count}: {post.title}")
    post.comments.replace_more(limit=None)
    for comment in post.comments.list():
        try:
            username = comment.author.name
            if username not in moderators:
                usernames.add(username)
        except AttributeError:
            pass

print(f"Found {len(usernames)} usernames.")

with open('sent_messages.txt', 'r') as f:
    sent_usernames = {line.strip() for line in f}

for username in usernames:
    if username not in sent_usernames:
        # TODO: Don't forget to update the line below according to the message template variables
        message = MESSAGE_TEMPLATE.format(username=username)  
        try:
            reddit.redditor(username).message(random.choice(SUBJECT_LINES), message)
            print(f"Message sent to {username}")    
            with open('sent_messages.txt', 'a') as f:
                f.write(f"{username}\n")
        except Exception as e:
            print(f"Failed to send message to {username}: {e}")
        wait_time = random.randint(MIN_WAIT_TIME, MAX_WAIT_TIME)
        print(f"Waiting {wait_time} seconds...")
        time.sleep(wait_time)