# let-reddit-pick-my-wallpaper
python script using the praw python reddit API wrapper to pick daily most upvoted wallpaper and set it locally

works under ubuntu 15.x

Requires to install praw :  
pip install praw

Creates a .wallpapers directory under home folder  
downloads top scoring (last 24hrs) wallpaper from https://www.reddit.com/r/wallpapers/  
and sets it to local desktop using : 

gsettings set org.gnome.desktop.background picture-uri file:///home/username/.wallpapers/downloadedwallpaper.jpg

Make it run at startup by creating mystartupscript.conf:

start on runlevel [2345]
stop on runlevel [!2345]

exec /path/to/script.py


and place it under /etc/init (Use /etc/systemd in Ubuntu 15.x)
manual starting/stopping can be done with sudo service mystartupscript start and sudo service mystartupscript stop
