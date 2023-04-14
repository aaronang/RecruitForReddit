import praw
import random
import time
from dotenv import dotenv_values

CONFIG = dotenv_values(".env")
SUBREDDIT_NAME = 'cars'
MIN_WAIT_TIME = 15
MAX_WAIT_TIME = 45

SUBJECT_LINES = [
    "EXAMPLE SUBJECT LINE 1",
    "EXAMPLE SUBJECT LINE 2",
]
MESSAGE_TEMPLATE = """Hello {username}, this is an automated message sent by a Python script. Thanks for participating in the {subreddit_name} subreddit!"""

reddit = praw.Reddit(client_id=CONFIG.get("CLIENT_ID"),
                     client_secret=CONFIG.get("CLIENT_SECRET"),
                     user_agent=f"Connect for Reddit (by u/${CONFIG.get('USERNAME')})",
                     username=CONFIG.get("USERNAME"),
                     password=CONFIG.get("PASSWORD"))

subreddit = reddit.subreddit(SUBREDDIT_NAME)

post_count = 0
usernames = set()

for post in subreddit.hot(limit=10):
    post_count += 1
    print(f"Post {post_count}: {post.title}")
    post.comments.replace_more(limit=None)
    comments = post.comments.list()
    for comment in comments:
        try:
            username = comment.author.name
            usernames.add(username)
        except AttributeError:
            pass
        for reply in comment.replies:
            try:
                username = reply.author.name
                usernames.add(username)
            except AttributeError:
                pass

print("Usernames of commenters and repliers:")
for username in usernames:
    print(username)

with open('sent_messages.txt', 'a+') as f:
    f.seek(0)
    sent_usernames = {line.strip() for line in f}

for username in usernames:
    if username not in sent_usernames:
        # Don't forget to update this line according to the message template variables
        message = MESSAGE_TEMPLATE.format(username=username, subreddit_name=SUBREDDIT_NAME)  
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