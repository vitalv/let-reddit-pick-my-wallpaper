import praw
import urllib
import os
import subprocess


'''
The praw.Reddit connection requires these:

client_id='2ZMSO5JBG4DR5w'
client_secret='B4m8XSe2N2V1dcgRM-EY10YWAJ8'
my_user = 'reddit_user_name'
my_password = 'not.my.password'
user_agent='pc:r_wallpapers_sets_my_wallpaper:0.1 '

1 either provide them here, or in a praw.ini file residing in the same directory

reddit = praw.Reddit(client_id=client_id,
					client_secret=client_secret,
					password=my_password,
					user_agent=user_agent,
					username=my_user)


2 or read required parameters from praw.ini under [user_data] 

[user_data]
client_id=2ZMSO5JBG4DR5w
client_secret=B4m8XSe2N2V1dcgRM-EY10YWAJ8
username=redit_user_name
password=not.my.password
user_agent=pc:r_wallpapers_sets_my_wallpaper:0.1

'''

reddit = praw.Reddit('user_data')

r_wallpapers = reddit.subreddit('wallpapers')

for submission in r_wallpapers.top(time_filter='day', limit=1):
	preview = submission.preview
	title = submission.title.replace(" ", "_")

url = preview["images"][0]["source"]["url"]

home_dir = os.path.expanduser('~')
wallpapers_dir = os.path.join(home_dir, ".wallpapers")
if not os.path.isdir(wallpapers_dir):
	os.mkdir(wallpapers_dir)
wallpaper_path = os.path.join(wallpapers_dir, str(title)+".jpg")
urllib.urlretrieve(str(url), wallpaper_path )
print "Downloaded \"" + title + "\" from " + url + " \nand saved it to " + wallpapers_dir

change_wallpaper_cmd = "gsettings set org.gnome.desktop.background picture-uri file://" + wallpaper_path

subprocess.call(change_wallpaper_cmd, shell=True)

