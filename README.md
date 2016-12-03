# let-reddit-pick-my-wallpaper
python script using the praw python reddit API wrapper to pick daily most upvoted wallpaper and set it locally

works under ubuntu 15.x

Requires to install praw :  
pip install praw

Creates a .wallpapers directory under home folder  
downloads top scoring (last 24hrs) wallpaper from https://www.reddit.com/r/wallpapers/  
and sets it to local desktop using : 

gsettings set org.gnome.desktop.background picture-uri file:///home/username/.wallpapers/downloadedwallpaper.jpg

Make it run at startup :  

-copy praw.ini file to ~/.config/

-Add it to Startup Applications 

or

-Add it as a cron task:
crontab -e
@reboot python /home/vital/let-reddit-pick-my-wallpaper/r_wallpapers_sets_my_wallpaper.py &


