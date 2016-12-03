#!/usr/bin/env python
# -*- coding: utf-8 -*-

import praw
import urllib
import os
import subprocess
from bs4 import BeautifulSoup


'''
The praw.Reddit connection requires these:

client_id='2ZMSO5JBG4DR5w'
client_secret='B4m8XSe2N2V1dcgRM-EY10YWAJ8'
my_user = 'reddit_user_name'
my_password = 'not.my.password'
user_agent='pc:r_wallpapers_sets_my_wallpaper:0.1 '

1 either provide them here, or in a praw.ini file residing in the same directory (or at ~/.config/)

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


def get_top_submission(subreddit):

	for submission in subreddit.top(time_filter='day', limit=1):
		#preview = submission.preview
		title = submission.title.replace(" ", "_").strip(".")
		url = submission.url
	return url, title


def configure_wallpaper_path(title):
	
	if not os.path.isdir(wallpapers_dir):
		os.mkdir(wallpapers_dir)
	wallpaper_path = os.path.join(wallpapers_dir, str(title)+".jpg")
	return wallpaper_path


def download_wallpaper(url, path):

	if urllib.urlopen(url).getcode() == 200:
		urllib.urlretrieve(url, path )
		return urllib.urlopen(url).getcode()


def change_local_wallpaper(wallpaper_path):
	
	change_wallpaper_cmd = "gsettings set org.gnome.desktop.background picture-uri file://" + wallpaper_path
	subprocess.call(change_wallpaper_cmd, shell=True)


def main():

	reddit = praw.Reddit('user_data')
	r_wallpapers = reddit.subreddit('wallpapers')
	url, title = get_top_submission(r_wallpapers)
	wallpaper_path = configure_wallpaper_path(title)
	
	if 'http://imgur.com/a/' in url: #link to imgur album
		html = urllib.urlopen(url).read()
		soup = BeautifulSoup(html)
		matches = soup.find_all('img', attrs={"class": "post-image-placeholder"})
		#pick first image in album:
		url = re.search("i.imgur.com/(.+?\")", str(matches[0])).group(0).strip("\"")
		url = "http://"+url
	#elif 'http://i.imgur.com/' or 'https://i.redd.it/' in url: #direct link to image, no imgur page

	status_code = download_wallpaper(str(url), wallpaper_path)

	if status_code == 200:
		print "\nDownloaded \"" + title + "\" from " + str(url)
		change_local_wallpaper(wallpaper_path)
		print "Set \"" + title + "\" as wallpaper"
	else: #change to random wallpaper in wallpapers_folder:
		wallpaper = random.choice(os.listdir(wallpapers_dir))
		wallpaper_path = os.path.join(wallpapers_dir, wallpaper)
		change_local_wallpaper(wallpaper_path)
		print "Set \"" + title + "\" as wallpaper"



if __name__ == "__main__":

	home_dir = os.path.expanduser('~')
	wallpapers_dir = os.path.join(home_dir, ".wallpapers")

	main()



