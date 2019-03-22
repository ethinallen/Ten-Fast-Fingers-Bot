from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
from PIL import Image
import os
import pytesseract

#url of the login page
url = 'https://10fastfingers.com/login'
anticheaturl = 'https://10fastfingers.com/anticheat'

#specify your gmail email so you can log in and save your score
email = 'andrew@andrewemery.io'

#specify your gmail password
password = 'thisismypassword'

#path to geckodriver
pathToDriver = '/Users/drew/Projects/tffBot/venv/geckodriver'

#function to make the driver and initialize at the url I want to go to
def makeDriver(url):
    driver = webdriver.Firefox(executable_path=pathToDriver)
    #set a page timeout
    driver.set_page_load_timeout(10)
    return driver

#gathers all of the words on the page and returns them into a list
def getWords(url):
    driver = makeDriver(url)
    try:
        driver.get(url)
    except TimeoutException:
        driver.execute_script("window.stop();")
    userName = driver.find_element_by_xpath('//*[@id="UserEmail"]')
    userName.send_keys(email)
    userName.send_keys(Keys.RETURN)
    time.sleep(1)
    pw = driver.find_element_by_css_selector('#UserPassword')
    pw.send_keys(password)
    pw.send_keys(Keys.RETURN)
    time.sleep(5)
    driver.get(anticheaturl)
    startTest = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[4]/div/div/div[1]/table/tbody/tr/td[1]/a')
    startTest.click()
    start = driver.find_element_by_xpath('//*[@id="start-btn"]')
    start.click()
    time.sleep(2)
    driver.save_screenshot('ss.png')
    return driver

def cropImage():
    driver = getWords(url)
    img = Image.open('ss.png')
    area = (225, 200, 900, 350)
    img.crop((area)).save('words.png')
    os.remove('ss.png')
    return driver

def decodeWords():
    driver = cropImage()
    words = pytesseract.image_to_string(Image.open('words.png'))
    return words, driver

#sends all of the words to the input field followed by a space so that it advances to the next word
def sendWords():
    words, driver = decodeWords()
    sendWord = driver.find_element_by_xpath('//*[@id="word-input"]')
    sendWord = sendWord.send_keys(words)
    submit = driver.find_element_by_xpath('//*[@id="submit-anticheat"]')
    submit.click()

if __name__ == '__main__':
    sendWords()
    # os.remove('words.png')
