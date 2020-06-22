import praw

from secrets import  client_secret

password = input("Enter password including 2FA")

reddit = praw.Reddit(client_id="c10F5e8h6dVDKQ",
                     client_secret=client_secret,
                     password=password,
                     user_agent="modmail archiver by u/SaatvikRamani",
                     username="SaatvikRamani")

print(reddit.user.me())