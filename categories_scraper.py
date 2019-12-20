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
    question_sets = []
    driver.get("https://a2oj.com/categories")
    for i in range(1, 769):
        number = driver.find_element_by_xpath("//table[contains(@class, 'tablesorter')]/tbody/tr["+ str(i) +"]/td[1]").text
        name = driver.find_element_by_xpath("//table[contains(@class, 'tablesorter')]/tbody/tr["+ str(i) +"]/td[2]/a").text
        link = driver.find_element_by_xpath("//table[contains(@class, 'tablesorter')]/tbody/tr["+ str(i) +"]/td[2]/a").get_attribute("href")
        problem_count = int(driver.find_element_by_xpath("//table[contains(@class, 'tablesorter')]/tbody/tr["+ str(i) +"]/td[3]").text)
        question_set = {
            "number" : number,
            "name" : name,
            "link" : link,
            "problem_count" : problem_count
        }
        question_sets.append(question_set)
        print(question_set)


    for ladder in question_sets:

        driver.get(ladder["link"])
        ladder_qns = []

        ladder_name = ladder["name"]
        # ladder_difficulty = driver.find_element_by_xpath("//div[contains(@id,'page')]/font/center/table/tbody/tr[3]").text
        print(ladder_name + ": ")


        for qn in range(1, ladder["problem_count"]+1):
            question = {}
            question['id'] = int(driver.find_element_by_xpath("//table[contains(@class, 'tablesorter')]/tbody/tr["+str(qn)+"]/td[1]").text)
            question['Problem Name'] = driver.find_element_by_xpath("//table[contains(@class, 'tablesorter')]/tbody/tr["+str(qn)+"]/td[2]").text
            question['Problem Link'] = driver.find_element_by_xpath("//table[contains(@class, 'tablesorter')]/tbody/tr["+str(qn)+"]/td[2]/a").get_attribute("href")
            question['Online Judge'] = driver.find_element_by_xpath("//table[contains(@class, 'tablesorter')]/tbody/tr["+str(qn)+"]/td[4]").text
            question['Contest'] = driver.find_element_by_xpath("//table[contains(@class, 'tablesorter')]/tbody/tr["+str(qn)+"]/td[6]").text
            question['Difficulty Level'] = driver.find_element_by_xpath("//table[contains(@class, 'tablesorter')]/tbody/tr["+str(qn)+"]/td[7]").text
            # question['Depends On'] = driver.find_element_by_xpath("//table[contains(@class, 'tablesorter')]/tbody/tr["+str(qn)+"]/td[6]").text

            print(question)

            ladder_qns.append(question)

        ladder_set.append({
            "ladder name" : ladder_name,
            "ladder questions" : ladder_qns
        })


    output = open("categories.txt", "a")
    output.write(json.dumps(ladder_set))
    output.close()