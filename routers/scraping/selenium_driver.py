from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def create_driver():
    global chromedriver
    chromedriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

create_driver()