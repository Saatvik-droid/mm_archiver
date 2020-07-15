import praw

from datetime import datetime, timezone, timedelta

from secrets import secrets

# assign args to vars
subreddit = input("subreddit whose modmails have to be archived(enter multiple subreddits by adding a '+' between each)")
time = input("time old modmails to be archived(in days)")
number = input("maximum number mails to be archived")
reply = input("reply message if needed")
password = input("password for reddit account")

if time.lower() == "none":
    time = int(0)
else:
    time = int(time)

if number.lower() == "none":
    number = int(9999)
else:
    number = int(number)

if reply.lower() == "none":
    reply = None
else:
    reply = str(reply)

# log into reddit
reddit = praw.Reddit(client_id=secrets["client_id"],
                     client_secret=secrets["client_secret"],
                     password=password,
                     user_agent="modmail archiver by u/SaatvikRamani",
                     username="SaatvikRamani")

# obtain all modmail conversations
modmails = reddit.subreddit(subreddit).modmail.conversations(other_subreddits=None, limit=1000, sort="recent", state="all")

# counter to count number of modmails gone through
counter = 0

days_before = datetime.now(timezone.utc) - timedelta(days=time)

# actual archiving feature
for modmail in modmails:
    counter = counter + 1
    print(modmail.owner.display_name)
    print(counter)

    if counter > number:
        break

    if datetime.fromisoformat(modmail.last_updated) < days_before:
        if reply is not None:
            modmail.reply(reply, author_hidden=True)
        else:
            pass
        modmail.reply("Auto archiving, someone ran the script", internal=True)
        modmail.archive()
    else:
        pass
    print(f"{counter} modmail(s) archived")


print("Successful!!!")
