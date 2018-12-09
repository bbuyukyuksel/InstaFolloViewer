#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
from selenium import webdriver
import time
import numpy as np
from parseProcess import *

def getMyFollows(_source):
    source = BeautifulSoup(_source, 'html5lib')
    source.find_all('a',{'class':'FPmhX'})

def getPhotoLinks(_source,log=False):
    source = BeautifulSoup(_source, 'html5lib')
    photo_row = source.find_all('div', {"class": "Nnq7C weEfm"})
    links = []
    for i in photo_row:
        photo_column = i.find_all('div', {"class": "v1Nh3"})
        for j in photo_column:
            url = j.find('a')
            links.append(str(url).split('">')[0].split('"')[1])
            if log:
                print str(url).split('">')[0].split('"')[1]
    return links
def clickButtons(links,duration=0.5):
    for lnk in links:
        sonra_animsat = browser.find_element_by_xpath(lnk)
        sonra_animsat.click()
        time.sleep(duration)

def login(__username,__password,duration=1.5):

    # //*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a
    giris_yap = browser.find_elements_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a')
    giris_yap[0].click()
    time.sleep(duration)

    username = browser.find_element_by_name('username')
    password = browser.find_element_by_name('password')
    giris_yap = browser.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/button')
    username.send_keys(__username)
    password.send_keys(__password)
    giris_yap.click()
    time.sleep(duration)

def scroll_down(eula, duration= 0.8):
    print "Phase : 04 collecting users to like photos.."
    SCROLL_PAUSE_TIME = duration
    #eula = browser.find_element_by_class_name('wwxN2')
    # Get scroll height
    last_height = browser.execute_script("return arguments[0].scrollHeight", eula)
    first = True
    second = False
    while True:
        # Scroll down to bottom
        browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", eula)

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return arguments[0].scrollHeight", eula)
        print new_height
        if new_height == last_height:
            if second:
                break
            if first:
                curr_heigh = browser.execute_script("return arguments[0].scrollTop", eula)
                x1 = np.linspace(curr_heigh,0,200)
                x2 = np.linspace(0,curr_heigh,200)
                pos= []
                pos.extend(list(x1))
                pos.extend(list(x2))
                pos.extend(list(x1))
                pos.extend(list(x2))

                for i in pos:
                    browser.execute_script("arguments[0].scrollTop = {};".format(i), eula)
                    new_height = browser.execute_script("return arguments[0].scrollHeight", eula)
                    time.sleep(0.05)
                    if last_height != new_height:
                        second = True
                        print "Wait please!"
                        time.sleep(3)
                        break
                first = False


        last_height = new_height
if __name__ == '__main__':

    __username = 'username'
    __password = 'password'

    driver_path = "D:/LIBS/chromedriver"
    url = 'https://www.instagram.com/'

    try:
        os.rmdir('photos')
        time.sleep(2)
        print "Photos Dizini Silindi."
    except:
        os.mkdir('photos')
        print "Photos dir is created."

    time.sleep(2)

    browser = webdriver.Chrome(executable_path=driver_path)
    browser.get(url)
    time.sleep(1)
    login(__username,__password)


    #simdi degil
    xpaths = ['/html/body/div[2]/div/div/div/div[3]/button[2]','//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[3]/a']

    clickButtons(xpaths,duration=1.5)

    with open('page_source.html','w') as f:
        f.write(browser.page_source.encode('utf8'))

    print "Phase : 01 collecting photo links.."
    links = getPhotoLinks(browser.page_source)

    ################## Fotolara Ait Begeni Listelerini Cek
    print "Phase : 02 collecting users to like photos.."
    counter = 0
    for lnk in links:
        browser.get(url + __username + lnk)
        browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[2]/div/div/a').click()
        time.sleep(1.5)
        filename = 'src_{}.html'.format(str(counter)+'_' +lnk.replace('/p/','').replace('/',''))
        
        SCROLL_PAUSE_TIME = 0.8
        eula = browser.find_element_by_class_name('wwxN2')
        # Get scroll height
        last_height = browser.execute_script("return arguments[0].scrollHeight",eula)
        while True:
            # Scroll down to bottom
            browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;",eula)

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = browser.execute_script("return arguments[0].scrollHeight",eula)
            if new_height == last_height:
                break
            last_height = new_height
        #############################################################################################
        time.sleep(1.5)
        print filename
        with open('./photos/' + filename, 'w') as f:
            f.write(browser.page_source.encode('utf8'))
        counter += 1
    #################################################################################################

    print "Phase : 03 collecting your follows.."
    time.sleep(0.5)
    browser.get(url + __username)

    #Takipcilerim
    time.sleep(3)
    browser.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a')[0].click()
    time.sleep(3)
    browser.refresh()
    time.sleep(3)
    browser.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a')[0].click()
    time.sleep((3))
    eula = browser.find_element_by_class_name('isgrP')
    time.sleep(2)
    scroll_down(eula,1.2)
    with open('myFollows.html','w') as f:
        f.write(browser.page_source.encode('utf8'))
    #getMyFollows(browser.page_source)

    print "Phase: 05 Parsing.."
    getMyListandNoneFollowers()
    print "It's done!"
    browser.close()

