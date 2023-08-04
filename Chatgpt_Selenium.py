from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as SeleniumExceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as SeleniumExceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from markdownify import markdownify
from threading import Thread
import platform
import logging
import weakref
import json
import time
import re
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#options.add_argument("--headless")

driver = uc.Chrome()

def init(email,password,content):
    driver.execute_cdp_cmd(
                'Network.setBlockedURLs',
                {'urls': ['https://chat.openai.com/backend-api/moderations']},
            )
    driver.get('https://chat.openai.com/')
    chatgpt_login_btn = (By.XPATH, '//button[div[text()="Log in"]]')
    chatgpt_username_input=(By.XPATH,'//input[@id="username"]')
    chatgpt_password_input=(By.XPATH,'//input[@id="password"]')
    chatgpt_continue_button=(By.XPATH,'//button[text()="Continue"]')
    chatgpt_Google_button=(By.XPATH,'//button[text()="Continue with Google"]')
    chatgpt_continue2_button=(By.XPATH,'/html/body/div/main/section/div/div/div/form/div[3]/button')
    chatgpt_next_button=(By.XPATH,'//*[@id="radix-:rf:"]/div[2]/div/div[2]/button')
    chatgpt_done_button=(By.XPATH,'//*[@id="radix-:rf:"]/div[2]/div/div[2]/button[2]')
    chatgpt_text_input =(By.XPATH,'//*[@id="prompt-textarea"]')
    chatgpt_send_button =(By.XPATH,'//*[@id="__next"]/div[1]/div[2]/div/main/div[2]/form/div/div[2]/button')
    chatgpt_text_output=(By.CLASS_NAME,'flex flex-grow flex-col gap-3')
    driver.execute_cdp_cmd(
                'Network.setCookie',
                {
                    'domain': 'chat.openai.com',
                    'path': '/',
                    'name': 'cf_clearance',
                    'value': 'copy from cookies',
                    'httpOnly': True,
                    'secure': True,
                },
            )
    all_text=[]
    check=True
    count=0
    WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(chatgpt_login_btn)
            ).click()
    WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(chatgpt_username_input)
            ).send_keys(email)
    WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(chatgpt_continue_button)
            ).click()
    WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(chatgpt_password_input)
            ).send_keys(password)
    WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(chatgpt_continue2_button)
            ).click()
    WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(chatgpt_next_button)
        ).click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(chatgpt_done_button)
    ).click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(chatgpt_done_button)
    ).click()
    for buf in content:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(chatgpt_text_input)
        ).send_keys(f"{buf} 위 내용만을 기반으로 이해하기 쉽게 한국어 정리해줘. 이때 한 문장씩 앞에 '-'를 붙여줘.")
        time.sleep(5)
        WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(chatgpt_send_button)
            ).click()
    all_text=[]
    time.sleep(15)
    
    wait = WebDriverWait(driver, 10)  # Maximum wait time of 10 seconds
    elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'flex.flex-grow.flex-col.gap-3')))
    # Now you can iterate through the elements as before
    for element in elements:
        try:
            all_text.append(element.text)
            print(all_text)
        except Exception as e:
            print("Error:", e)

content=['#VALIC Retirement Services Company was impacted by #MOVEit via #PBI with 798k individuals affected. The total number of individuals affected by MOVEit breaches now stands at >38 million. #VRSCO 1/2 ','#MOVEit stats. 2/2','Another #CalPERS retiree sues PBI <— Via @mayacmiller #MOVEit']

init('unst0pp4bl323@gmail.com','winterlaken23!',content)

# add your own logic of making request and getting response    
time.sleep(2000)
