import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.admin_config import settings as admin_settings
from .selenium_driver import chromedriver

def get_driver():
    return chromedriver

def isOnline():
    get_driver().get("https://linkedin.com")
    try:
        WebDriverWait(get_driver(), 2).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/header/div/nav/ul/li[2]/a/span")))
        return True
    except:
        return False

def Login():
    wait = WebDriverWait(get_driver(), 10)
    if not isOnline():
        get_driver().get("https://linkedin.com/uas/login")
        wait.until(EC.element_to_be_clickable((By.ID, "username"))).send_keys(admin_settings.LINKEDIN_USER)
        wait.until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(admin_settings.LINKEDIN_PASS)
        get_driver().find_element(By.XPATH, "//button[@type='submit']").click()

def Scrapping(user):
    Login()

    get_driver().get(f"https://www.linkedin.com/in/{user}")
    time.sleep(1)
    try:
        try:
            connections = get_driver().find_element(By.XPATH, '//*[@id="ember30"]/div[2]/ul/li/span/span').text
        except:
            connections = get_driver().find_element(By.XPATH, '//*[@id="ember31"]/div[2]/ul/li/span/span').text
    except:
        try:
            connections = get_driver().find_element(By.XPATH, '//*[@id="ember31"]/div[2]/ul/li[2]/span/span').text
        except:
            connections = 500

    if '+' in connections:
        connections = connections.replace("+", "") 
    try:
        get_driver().get(f"https://www.linkedin.com/in/{user}/details/certifications/")
        time.sleep(1)
        cerificates = len(get_driver().find_elements(By.CSS_SELECTOR, "ul > li.pvs-list__paged-list-item.artdeco-list__item.pvs-list__item--line-separated"))
    except:
        cerificates = 0
    try:
        get_driver().get(f"https://www.linkedin.com/in/{user}/details/experience/")
        time.sleep(1)
        experience = len(get_driver().find_elements(By.CSS_SELECTOR, "ul > li.pvs-list__paged-list-item.artdeco-list__item.pvs-list__item--line-separated"))
    except:
        experience = 0

    try:
        get_driver().get(f"https://www.linkedin.com/in/{user}/details/projects/")
        time.sleep(1)
        projects = len(get_driver().find_elements(By.CSS_SELECTOR, "ul > li.pvs-list__paged-list-item.artdeco-list__item.pvs-list__item--line-separated"))
    except:
        projects = 0

    return {
        "Connections": connections,
        "Certificates": cerificates,
        "Experience": experience,
        "Projects": projects
    }