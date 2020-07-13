import praw

from datetime import datetime, timezone

from secrets import secrets

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", dest="password", help="password for reddit account", required=True)
parser.add_argument("-s", dest="subreddit", help="subreddit whose modmails have to be archived(enter multiple subreddits by adding a '+' between each)", required=True)
parser.add_argument("-t", dest="time", help="time old modmails to be archived(in days)", default=0)
parser.add_argument("-n", dest="number", help="maximum number mails to be archived, default", type=int, default=9999)
parser.add_argument("-r", dest="reply", help="reply message if needed", default=None)
args = parser.parse_args()

# assign args to vars
password = args.password
subreddit = args.subreddit
time = args.time
number = args.number
reply = args.reply

# log into reddit
reddit = praw.Reddit(client_id=secrets["client_id"],
                     client_secret=secrets["client_secret"],
                     password=password,
                     user_agent="modmail archiver by u/SaatvikRamani",
                     username="SaatvikRamani")

# obtain all modmail conversations
modmails = reddit.subreddit("all").modmail.conversations(other_subreddits=subreddit, sort="recent", state="all")

# counter to count number of modmails gone through
counter = 0

# actual archiving feature
for modmail in modmails:
    counter = counter + 1

    if counter > number:
        break

    if reply is not None:
        print("reply")
        modmail.reply(reply, author_hidden=True)
    else:
        pass
    if int((datetime.now(timezone.utc) - datetime.fromisoformat(modmail.last_updated)).days) >= int(time):
        print("archive")
        modmail.reply("Auto archiving, someone ran the script", internal=True)
        modmail.archive()
    else:
        pass

    print("{0} modmail(s) archived".format(counter))

print("Successful!!!")
