from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from utility_methods.utility_methods import *
import urllib.request
import os


class InstaBot:

    def __init__(self, username=None, password=None):
        """"
        Creates an instance of InstaBot class.

        Args:
            username:str: The username of the user, if not specified, read from configuration.
            password:str: The password of the user, if not specified, read from configuration.

        Attributes:
            driver_path:str: Path to the chromedriver.exe
            driver:str: Instance of the Selenium Webdriver (chrome 72) 
            login_url:str: Url for logging into IG.
            nav_user_url:str: Url to go to a users homepage on IG.
            get_tag_url:str: Url to go to search for posts with a tag on IG.
            logged_in:bool: Boolean whether current user is logged in or not.
        """

        self.username = config['IG_AUTH']['USERNAME']
        self.password = config['IG_AUTH']['PASSWORD']

        self.login_url = config['IG_URLS']['LOGIN']
        self.nav_user_url = config['IG_URLS']['NAV_USER']
        self.get_tag_url = config['IG_URLS']['SEARCH_TAGS']

        self.driver = webdriver.Chrome(config['ENVIRONMENT']['CHROMEDRIVER_PATH'])
        
        self.logged_in = False


    @insta_method
    def login(self):
        """
        Logs a user into Instagram via the web portal
        """

        self.driver.get(self.login_url)
        self.driver.maximize_window() #For maximizing window
        self.driver.implicitly_wait(30) #gives an implicit wait for 20 seconds
        #username_input = self.driver.find_element_by_id('react-root')
        #username_input.send_keys(Keys.TAB)
        #username_input.send_keys(self.username)
        #username_input.send_keys(Keys.TAB)
        #username_input.send_keys(self.password)
        #username_input.send_keys(Keys.ENTER)
        
        username_input = self.driver.find_element_by_name('username')
        password_input = self.driver.find_element_by_name('password')
        
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
                                                           #//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]
        login_btn = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]') # login button xpath changes after text is entered, find first
        #login_btn = self.driver.find_element_by_css_selector('.L3NKy').click()
        
        self.driver.implicitly_wait(130) #gives an implicit wait for 20 seconds
        
        time.sleep(1)
        
        self.driver.execute_script("arguments[0].click();", login_btn)
        login_btn.click()
        

    @insta_method
    def search_tag(self, tag):
        """
        Naviagtes to a search for posts with a specific tag on IG.

        Args:
            tag:str: Tag to search for
        """
        print('LOG - start search_tag ' + tag)
        self.driver.get(self.get_tag_url.format(tag))
        s_posts = 35
        # Opens images and gives like 'new method'
        imgs = []
        pasoImg = 0
        
        imgs.extend(self.driver.find_elements_by_class_name('_9AhH0'))
        self.driver.implicitly_wait(30)
        for img in imgs[:s_posts]:
            pasoImg += 1
            img.click()
            time.sleep(1)
            try:
                strLike = 'Me gusta'
                
                print('LOG - Img ' + str(pasoImg) + ' read')
                #time.sleep(1)
                #self.driver.implicitly_wait(3)
                
                labelBtn = self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button')
                
                try:
                    likeSvg = self.driver.find_element_by_xpath("//*[@aria-label='Ya no me gusta']")
                    strLike = likeSvg.get_attribute("aria-label")
                    print('Foto ' + str(pasoImg) + ' ya activado boton me gusta')
                except Exception as error:
                    print(error)
                time.sleep(1)
                self.driver.implicitly_wait(3)
                
                #labelBtn.send_keys("\n")
                if strLike != 'Ya no me gusta':
                    labelBtn.click()
                    print('LOG - Click like  ' + str(pasoImg))
            except Exception as e:
                print(e)

            #self.comment_post()
            
            closeBtn = self.driver.find_element_by_xpath('/html/body/div[4]/div[3]/button')
            time.sleep(1)
            #self.driver.implicitly_wait(30)
                
            closeBtn.click()
        print('LOG - end search_tag '+ tag)


    
    @insta_method
    def follow_users(self, tag):
        """
        Navigates to a tag goes to the featured pic and follows profiles that likes this picture

        Args:
            tag:str: Tag to navigate to the featured pic with this tag
        """
        followed = 0
        errorFollowed = 0
        
        print('LOG - start follow_users ' + tag)
        self.driver.get(self.get_tag_url.format(tag))
        s_posts = 1
        # Opens images and gives like 'new method'
        imgs = []
        followButtons = []
        nRefresh = 0
        imgs.extend(self.driver.find_elements_by_class_name('_9AhH0'))
        self.driver.implicitly_wait(3)
        for img in imgs[:s_posts]:
            img.click()
            time.sleep(2)
            try:
                self.driver.implicitly_wait(3)                                
                try:
                    likeIdBtn = self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div')
                    print('First test try')
                except Exception as errorPeople:
                    print(errorPeople)
                    likeIdBtn = self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div[2]/button')
                else:
                    print('Se detecta botón personas que han dado like a la foto')
                time.sleep(1)
                print(likeIdBtn.text)
                likeIdBtn.click()
                print('LOG - Click on the list of people that liked the picture')
                self.driver.implicitly_wait(100)                                
                time.sleep(2)
                numRange = range(0,14)
                while nRefresh < 8:
                    for i in numRange:
                        try:
                            self.driver.implicitly_wait(30)       
                            xpathBtn = '/html/body/div[5]/div/div[2]/div/div/div[' + str(i+1) + ']/div[3]/button'
                            followButton = self.driver.find_element_by_xpath(xpathBtn)
                            print('#' + followButton.text + '#')
                            #time.sleep(1)
                            if followButton.text == 'Seguir':
                                print('#' + followButton.text + '#')
                                print('LOG - Click on follow button')
                                followButton.click()
                                followed += 1
                                #followButton.send_keys(Keys.PAGE_DOWN)
                            time.sleep(1)
                            print(str(i+1))
                            print('User/s read')
                        except Exception as errorFollowButton:
                            print(errorFollowButton)
                            errorFollowed += 1
                    nRefresh +=1
                    self.driver.implicitly_wait(50)
                    time.sleep(2)
                    print('Refresh count / PAGE_DOWN')
                    followButton.send_keys(Keys.PAGE_DOWN)
                    followButton.send_keys(Keys.PAGE_DOWN)

                    
            except Exception as errorFollow:
                print(errorFollow)
        print('LOG - end follow_users ' + tag + ' Follows: ' + str(followed) + ' Errors: ' + str(errorFollowed))        
        

    
    @insta_method
    def nav_user(self, user):
        """
        Navigates to a users profile page

        Args:
            user:str: Username of the user to navigate to the profile page of
        """

        self.driver.get(self.nav_user_url.format(user))


    @insta_method
    def follow_user(self, user):
        """
        Follows user(s)

        Args:
            user:str: Username of the user to follow
        """

        self.nav_user(user)

        follow_buttons = self.find_buttons('Seguir')

        for btn in follow_buttons:
            btn.click()

    
    @insta_method
    def unfollow_user(self, user):
        """
        Unfollows user(s)

        Args:
            user:str: Username of user to unfollow
        """

        self.nav_user(user)

        unfollow_btns = self.find_buttons('Siguiendo')

        if unfollow_btns:
            for btn in unfollow_btns:
                btn.click()
                unfollow_confirmation = self.find_buttons('Dejar de seguir')[0]
                unfollow_confirmation.click()
        else:
            print('No {} buttons were found.'.format('Following'))
    

    @insta_method
    def download_user_images(self, user):
        """
        Downloads all images from a users profile.

        """
    
        self.nav_user(user)

        img_srcs = []
        finished = False
        while not finished:

            finished = self.infinite_scroll() # scroll down

            img_srcs.extend([img.get_attribute('src') for img in self.driver.find_elements_by_class_name('FFVAD')]) # scrape srcs

        img_srcs = list(set(img_srcs)) # clean up duplicates

        for idx, src in enumerate(img_srcs):
            self.download_image(src, idx, user)
    

    @insta_method
    def like_latest_posts(self, user, n_posts, like=True):
        """
        Likes a number of a users latest posts, specified by n_posts.

        Args:
            user:str: User whose posts to like or unlike
            n_posts:int: Number of most recent posts to like or unlike
            like:bool: If True, likes recent posts, else if False, unlikes recent posts

        TODO: Currently maxes out around 15.
        """

        action = 'Me gusta' if like else 'Ya no me gusta'

        self.nav_user(user)

        imgs = []
        imgs.extend(self.driver.find_elements_by_class_name('_9AhH0'))
        self.driver.implicitly_wait(30)
        for img in imgs[:n_posts]:
            img.click()
            time.sleep(2)
            try:
                strLike = 'Me gusta'
                time.sleep(1)
                self.driver.implicitly_wait(3)
                #labelBtn = self.driver.find_element_by_xpath("//*[@aria-label='{}']".format(action))
                labelBtn = self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button')
                
                #labelBtn.send_keys("\n")
                try:
                    likeSvg = self.driver.find_element_by_xpath("//*[@aria-label='Ya no me gusta']")
                    strLike = likeSvg.get_attribute("aria-label")
                    print(strLike)
                except Exception as error:
                    print(error)
                
                time.sleep(1)
                self.driver.implicitly_wait(3)
                
                
                if strLike != 'Ya no me gusta': 
                    labelBtn.click()
            except Exception as e:
                print(e)

            #self.comment_post()
            
            closeBtn = self.driver.find_element_by_xpath('/html/body/div[4]/div[3]/button')
            time.sleep(1)
            self.driver.implicitly_wait(30)
                
            closeBtn.click()
            #self.driver.find_elements_by_class_name('wpO6b ')


    @insta_method
    def comment_post(self):
        """
        Comments on a post that is in modal form
        """
        
        print('LOG - start comment post')
        textList = ['Wow! Amazing picture', 'Awesome car', 'Nice car', 'Niiice', 'Great picture', 'Nice picture','What a picture!']

        text = random.choice(textList) 
        
        comment_input = self.driver.find_elements_by_class_name('Ypffh')[0]
        comment_input.click()
        comment_input2 = self.driver.find_element_by_xpath("//*[@aria-label='Añade un comentario...']")
        comment_input2.send_keys(text)
        comment_input2.send_keys(Keys.ENTER)

        print('LOG - end comment post')


    def download_image(self, src, image_filename, folder):
        """
        Creates a folder named after a user to to store the image, then downloads the image to the folder.
        """

        folder_path = './{}'.format(folder)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        img_filename = 'image_{}.jpg'.format(image_filename)
        urllib.request.urlretrieve(src, '{}/{}'.format(folder, img_filename))


    def infinite_scroll(self):
        """
        Scrolls to the bottom of a users page to load all of their media

        Returns:
            bool: True if the bottom of the page has been reached, else false

        """

        SCROLL_PAUSE_TIME = 1

        self.last_height = self.driver.execute_script("return document.body.scrollHeight")

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(SCROLL_PAUSE_TIME)

        self.new_height = self.driver.execute_script("return document.body.scrollHeight")


        if self.new_height == self.last_height:
            return True

        self.last_height = self.new_height
        return False


    def find_buttons(self, button_text):
        """
        Finds buttons for following and unfollowing users by filtering follow elements for buttons. Defaults to finding follow buttons.

        Args:
            button_text: Text that the desired button(s) has 
        """

        buttons = self.driver.find_elements_by_xpath("//*[text()='{}']".format(button_text))

        return buttons


if __name__ == '__main__':

    config_file_path = './config.ini' 
    logger_file_path = './bot.log'
    config = init_config(config_file_path)
    logger = get_logger(logger_file_path)

    bot = InstaBot()
    bot.login()
    
    #bot.like_latest_posts('hondacivic_fk3', 15, like=True)
    #bot.follow_users('audi')

    #bot.search_tag('audination')
    #bot.search_tag('audia38l')
    bot.search_tag('audifan')
    #bot.search_tag('audilove')
    