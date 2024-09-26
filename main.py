from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support import expected_conditions as EC

import time

from dotenv import load_dotenv
import os
import random
import string
import re
import unicodedata

load_dotenv()

geckodriver_path = os.getenv('geckodriver_path')
playlist_link = os.getenv('playlist_link')

def wait_random_time():
    time.sleep(random.randint(1, 3))

def get_all_song_names(driver):
    elements = driver.find_elements(By.CSS_SELECTOR, '.encore-text.encore-text-body-medium.encore-internal-color-text-base.btE2c3IKaOXZ4VNAb8WQ.standalone-ellipsis-one-line')
    names = [element.text for element in elements]
    return names

def get_random_song(driver):
    return random.choice(get_all_song_names(driver))

def double_click_song(driver, song_title):
    try:
        if is_hebrew(song_title):
            song_title = unicodedata.normalize("NFC", song_title)

        song_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//div[@data-testid='tracklist-row' and .//div[contains(text(), '{song_title}')]]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", song_div)

        # Optionally, wait a moment to ensure scrolling is complete
        WebDriverWait(driver, 2).until(lambda d: song_div.is_displayed())
        # Within this div, find the time element and click on it
        driver.execute_script("window.scrollBy(0, -100);")
        time.sleep(1)

        time_element = song_div.find_element(By.XPATH, ".//div[@data-encore-id='text' and contains(text(), ':')]")
        actions = ActionChains(driver)
        actions.double_click(time_element).perform()
        print(f"Playing {song_title}")
    except:
        print(f"Song title was not found in playlist: {song_title}")


def initiate_song_play(driver, playlist_link):
    try:
        driver.get(playlist_link)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-testid='tracklist-row']"))
        )
        wait_random_time()
    except:
        print("Error in opening playlist")

import re

def is_hebrew(text):
    hebrew_pattern = re.compile(r'[\u0590-\u05FF]')
    return bool(hebrew_pattern.search(text))

def generate_email():
    # List of domains
    domains = ["yahoo.com", "gmail.com", "outlook.com", "hotmail.com", "walla.co.il"]
    # Generate a random username
    username_length = random.randint(5, 10)
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=username_length))
    # Randomly select a domain
    domain = random.choice(domains)
    return f"{username}@{domain}"


def generate_password(length=12):
    # Define the character set for the password
    characters = string.ascii_letters + string.digits + string.punctuation
    # Generate a random password
    password = ''.join(random.choices(characters, k=length))
    return f'{password}1!'


def generate_birth_year():
    current_year = 2024
    return random.randint(1950, current_year)


def generate_birth_month():
    return random.randint(1, 12)


def generate_birth_day(month):
    if month == 2:
        return random.randint(1, 28)
    elif month in [4, 6, 9, 11]:
        return random.randint(1, 30)
    else:
        return random.randint(1, 31)

def generate_random_username(length=8):
    characters = string.ascii_letters + string.digits  # Includes both uppercase and lowercase letters and digits
    username = ''.join(random.choice(characters) for _ in range(length))
    return username

def create_account(driver):
    driver.get('https://spotify.com/signup')
    username_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "username"))
    )

    email = generate_email()
    password = generate_password()

    username_input.send_keys(email)

    time.sleep(1)

    next_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'ButtonInner-sc-14ud5tc-0') and contains(text(), 'Next')]"))
    )
    next_btn.click()

    password_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "new-password"))
    )
    password_input.send_keys(password)

    time.sleep(1)

    next_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'ButtonInner-sc-14ud5tc-0') and contains(text(), 'Next')]"))
    )
    next_btn.click()

    time.sleep(1)

    name = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "displayName"))
    )
    name.send_keys(generate_random_username())

    time.sleep(1)
    # Create a Select object
    dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "month"))
    )
    select = Select(dropdown)

    month = generate_birth_month()

    # Select the option by value
    select.select_by_value(str(month))

    time.sleep(1)

    day = driver.find_element(By.ID, "day")
    day.send_keys(generate_birth_day(month))

    time.sleep(1)

    day = driver.find_element(By.ID, "year")
    day.send_keys(generate_birth_year())

    time.sleep(1)

    radio_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "gender_option_male"))
    )
    driver.execute_script("arguments[0].click();", radio_button)

    time.sleep(1)

    next_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'ButtonInner-sc-14ud5tc-0') and contains(text(), 'Next')]"))
    )
    next_btn.click()

    next_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'ButtonInner-sc-14ud5tc-0') and contains(text(), 'Sign up')]"))
    )
    next_btn.click()
    time.sleep(5)
    return 


def main():
    service = Service(geckodriver_path)
    driver = webdriver.Firefox(service=service)
    try:
        create_account(driver)
        initiate_song_play(driver, playlist_link)        
        double_click_song(driver, get_random_song(driver))
        while True:
            pass
    finally:
    # Close the browser
        driver.quit()

if __name__ == '__main__':
    main()
