import requests
import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
load_dotenv()

ladder_set = []

with webdriver.Firefox() as driver:

    # signin
    driver.get("https://a2oj.com/signin")
    driver.find_element_by_name("Username").send_keys(os.getenv("USER_ID"))
    driver.find_element_by_name("Password").send_keys(os.getenv("USER_PASS") + Keys.ENTER)
    time.sleep(5)

    # get all ladders in the page
    for i in range(11, 33):

        ladder_link = "https://a2oj.com/ladder?ID="
        driver.get(ladder_link + str(i))
        ladder_qns = []

        ladder_name = driver.find_element_by_xpath("//div[contains(@id,'page')]/font/center/table/tbody/tr[1]").text
        ladder_difficulty = driver.find_element_by_xpath("//div[contains(@id,'page')]/font/center/table/tbody/tr[3]").text
        print(ladder_name+" "+ ladder_difficulty +": ")


        for qn in range(1, 101):
            question = {}
            question['id'] = driver.find_element_by_xpath("//table[contains(@class, 'tablesorter')]/tbody/tr["+str(qn)+"]/td[1]").text
            question['Problem Name'] = driver.find_element_by_xpath("//table[contains(@class, 'tablesorter')]/tbody/tr["+str(qn)+"]/td[2]").text
            question['Problem Link'] = driver.find_element_by_xpath("//table[contains(@class, 'tablesorter')]/tbody/tr["+str(qn)+"]/td[2]/a").get_attribute("href")
            question['Online Judge'] = driver.find_element_by_xpath("//table[contains(@class, 'tablesorter')]/tbody/tr["+str(qn)+"]/td[3]").text
            question['Contest'] = driver.find_element_by_xpath("//table[contains(@class, 'tablesorter')]/tbody/tr["+str(qn)+"]/td[4]").text
            question['Difficulty Level'] = driver.find_element_by_xpath("//table[contains(@class, 'tablesorter')]/tbody/tr["+str(qn)+"]/td[5]").text
            question['Depends On'] = driver.find_element_by_xpath("//table[contains(@class, 'tablesorter')]/tbody/tr["+str(qn)+"]/td[6]").text

            print(question)

            ladder_qns.append(question)

        ladder_set.append({
            "ladder name" : ladder_name,
            "ladder difficulty" : ladder_difficulty,
            "ladder questions" : ladder_qns
        })


    output = open("a2oj.txt", "a")
    output.write(json.dumps(ladder_set))
    output.close()