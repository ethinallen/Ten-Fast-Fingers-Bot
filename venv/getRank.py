from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time, requests, tenFastBot
from PIL import Image
import os

# url of the page
url = 'https://10fastfingers.com/typing-test/english'

# path to geckodriver
pathToDriver = '/Users/drew/Projects/tffBot/venv/geckodriver'

# makes driver element from main bot program
# unsure if this is awful, awful design if you are reading this
# and this is terrible design please tell me
driver = tenFastBot.makeDriver(url)

# go to url
driver.get(url)

# return the value in the css of the script for highest achieved apm
highestAPM = driver.find_element_by_css_selector('.table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(4)')
