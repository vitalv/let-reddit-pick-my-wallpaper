import praw
import urllib
import os
import subprocess


client_id='2ZMSO5JBG4DR5w'
client_secret='B4m8XSe2N2V1dcgRM-EY10YWAJ8'
my_user = 'RaserLay'
my_password = 'redi.que?'
user_agent='pc:r_wallpapers_sets_my_wallpaper:0.1 (by /u/RaserLay)'


reddit = praw.Reddit(client_id=client_id,
					client_secret=client_secret,
					password=my_password,
					user_agent=user_agent,
					username=my_user)


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

