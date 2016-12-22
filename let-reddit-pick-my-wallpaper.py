#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import praw
import urllib
import os
import subprocess
from bs4 import BeautifulSoup
import re
import random


parser = argparse.ArgumentParser()
parser.add_argument("--subreddit", required=True, help="name of the subreddit to fetch image from. E.g: 'wallpapers' or 'EarthPorn'")
parser.add_argument("--top", required=True, help="subreddit Top time-limit submission: 'day', 'week', 'year'")


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


def get_top_submission(subreddit, time, limit):

	for submission in subreddit.top(time_filter=time, limit=limit):
		title = submission.title
		url = submission.url
	return url, title



def configure_wallpaper_path(title):
	
	if not os.path.isdir(wallpapers_dir):
		os.mkdir(wallpapers_dir)
	wallpaper_path = os.path.join(wallpapers_dir, str(title)+".jpg")
	return wallpaper_path



def check_img_fits_screen(original_title):

	'''
	checks the image is more or less rectangular (width/height ratio) to be used as wallpaper
	by comparing to local screen dimensions
	'''
	try: 
		original_title = original_title.replace(",", '').replace(".",'') #remove all "," and "." from title
		img_resolution = re.search("\[\d+?[ ]?[*xX][ ]?\d+?\]", original_title).group(0)
		w_by_h = re.compile("[*xX]").split(img_resolution)
		img_w, img_h = int(w_by_h[0][1:]), int(w_by_h[1][:-1])
		screen_dim = subprocess.Popen("xdpyinfo | grep dimensions", shell=True, stdout=subprocess.PIPE).stdout.read()
		screen_dim = re.search("\d+?x\d+? ", screen_dim).group(0).strip(" ")
		screen_w, screen_h = int(screen_dim.split("x")[0]), int(screen_dim.split("x")[1])
		#check if width/height ratios of img and screen are very different:
		ratio_screen = (screen_w + .0) / screen_h
		ratio_img = (img_w + .0) / img_h
		if (screen_w - img_w < 200) and (ratio_screen - ratio_img < 0.5):
			return True
		else:
			return False
	except AttributeError: #'NoneType' object has no attribute 'group' when original title doesnt comply
		return False



def get_imgur_image_url(url):

	'''
	works either for imgur.com/a/ (album) or just a regular imgur page with just one picture imgur.com/something
	in the first case just grabs url for first picture in the album, otherwise grabs 'the' image url
	'''
	html = urllib.urlopen(url).read()
	soup = BeautifulSoup(html)
	matches = soup.find_all('img', attrs={"class": "post-image-placeholder"})
	#pick first image in album:
	url = re.search("i.imgur.com/(.+?\")", str(matches[0])).group(0).strip("\"")
	return  "http://"+url



def download_wallpaper(url, path):

	'''
	first checks the url respnds OK(200), then check it's not html 
	'''
	if urllib.urlopen(url).getcode() == 200:
		if not 'html' in urllib.urlopen(url).read():
			urllib.urlretrieve(url, path)
			return urllib.urlopen(url).getcode()



def change_local_wallpaper(wallpaper_path):

	'''
	runs 
		gsettings set org.gnome.desktop.background picture-uri file://" + wallpaper_path
		or dconf write if gsettings gives the dreaded "GLib-GIO-Message: Using the 'memory' GSettings backend" error message
	'''

	file = 'file://%s'%wallpaper_path
	p = subprocess.Popen(['gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri', file], stderr=subprocess.PIPE)
	err = p.communicate()[1]
	if "GLib-GIO-Message: Using the 'memory' GSettings backend" in err:
		p = subprocess.Popen(['dconf', 'write', '/org/gnome/desktop/background/picture-uri', "\"%s\""%file], stderr=subprocess.PIPE)
		out, err = p.communicate()



def pick_random_wallpaper():

	wallpaper = random.choice(os.listdir(wallpapers_dir))
	wallpaper_path = os.path.join(wallpapers_dir, wallpaper)
	return wallpaper_path, wallpaper



def main():


	subreddit_arg = args.subreddit #subreddit_arg = 'EarthPorn'
	time = args.top	#time = 'day'
	reddit = praw.Reddit('user_data')
	subreddit = reddit.subreddit(subreddit_arg)
	limit = 1

	url, original_title = get_top_submission(subreddit, time, limit)

	img_fits_screen = True #assume by default . also assume images are large enough
	#check only if subreddit is EarthPorn bc function uses resolution from title which is rules for this subreddit
	#and because if subreddit is wallpapers I assume the images are kind of suitable already
	if subreddit.display_name == 'EarthPorn':
		img_fits_screen = check_img_fits_screen(original_title)

	if img_fits_screen == False:#go for second submission if first image does not fit the screen
		limit = 2
		url, original_title = get_top_submission(subreddit, time, limit)
		img_fits_screen = check_img_fits_screen(original_title)

	title = original_title.replace(" ", "_").strip(".")[0:30]#some titles are too long
	
	wallpaper_path = configure_wallpaper_path(title)

	if 'imgur.com' in url and not 'i.imgur.com/' in url: #i.imgur.com/ and i.redd.it/ are images, not html
		if 'html' in urllib.urlopen(url).read():
			url = get_imgur_image_url(url)
		
	if img_fits_screen == True:
		download_wallpaper(str(url), wallpaper_path)
		print "\nDownloaded \"" + title + "\" from " + str(url)

	else: #change to random wallpaper in wallpapers_folder:
		wallpaper_path, title = pick_random_wallpaper()
		print "\nCould not download image. Resolution and/or ratio not suitable for screen or could not find image. Pick random wallpaper"

	change_local_wallpaper(wallpaper_path)
	print "Set \"" + title + "\" as wallpaper"



if __name__ == "__main__":

	args = parser.parse_args()

	home_dir = os.path.expanduser('~')
	wallpapers_dir = os.path.join(home_dir, ".wallpapers")

	main()



