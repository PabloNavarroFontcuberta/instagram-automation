# instagram-automation
Instagram automation built with Python 3.7 and the Selenium package. 


# Current Features
- Follow a user
- Unfollow a user
- Search and like posts by tag 
- Comment posts by tag
- Like a users latest posts
- Unlike a users latest posts
- Download a users image media


# Important note 
- Maybe there are changes in HTML code of Instagram, review the code, everything is explained. If you have any doubt contact #pablonavarrofontcuberta@gmail.com 

# Instructions for Use
- Download driver for your respective version of Google Chrome into the root directory of the project. To see your Google Chrome version, go to chrome://version/ in your browser. To download the respective driver, go here: http://chromedriver.chromium.org/downloads. 
- Change the name of the file named `config_.ini` to `config.ini`, and add the username and password values in the config.ini file that the Instagram account the bot will use. Username and password combinations can also be passed when creating instances of the `InstaBot` class in `instagram_bot.py`.
- Install the dependencies in `requirements.txt`, with `pip install -r requirements.txt` from the root directory of the project, preferably in a Python 3.7 virtual environment.
- In the `instagram_bot.py` file, add the lines for the functionality desired at the bottom of the file.
