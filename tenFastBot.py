from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time, os
import notCheating

#url of the login page
url = 'https://10fastfingers.com/login'

#specify your gmail email so you can log in and save your score
email = 'email@email.email'

#specify your gmail password
password = 'password'

#path to geckodriver
pathToDriver = '/home/drew/geckodriver'

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
    pw = driver.find_element_by_css_selector('#UserPassword')
    pw.send_keys(password)
    pw.send_keys(Keys.RETURN)
    time.sleep(10)
    source = driver.page_source
    soup = BeautifulSoup(source, features="html.parser")
    firstWord = soup.find('span', {'class' : 'highlight'})
    firstWord = firstWord.get_text()
    spans = soup.find_all('span', {'class' : ''})
    text = [span.get_text() for span in spans]
    startingPosition = 0
    endingPosition = 0
    while text[startingPosition] != '(Tiếng Việt)':
        startingPosition += 1
    while text[endingPosition] != 'Top Ranking':
        endingPosition += 1
    startingPosition = startingPosition + 6
    endingPosition = endingPosition - 3
    words = []
    words.append(firstWord)
    for i in range(startingPosition, endingPosition):
        words.append(text[i])
    return words, driver

#sends all of the words to the input field followed by a space so that it advances to the next word
def sendWords(url):
    words, driver = getWords(url)
    for word in words:
        driver.find_element_by_xpath('//*[@id="inputfield"]').clear()
        sendWord = driver.find_element_by_xpath('//*[@id="inputfield"]')
        sendWord = sendWord.send_keys(word)
        sendSpace = driver.find_element_by_xpath('//*[@id="inputfield"]')
        sendSpace.send_keys(Keys.SPACE)
        time.sleep(.125)
    time.sleep(5)
    driver.close()

if __name__ == '__main__':
    sendWords(url)
    notCheating.sendWords()
    # os.remove('words.png')
