from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random, time, pyperclip
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import NoSuchElementException
import re
import csv

with open('tweets_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['name','index', 'timestamp', 'content'])

def following_LastData(browser):
    tweets = browser.find_elements(By.CSS_SELECTOR, "article")
    count = 0 
    data_list = [] 

    element = browser.find_element(By.CLASS_NAME,"css-901oao.css-16my406.r-1awozwy.r-18jsvk2.r-6koalj.r-poiln3.r-b88u0q.r-bcqeeo.r-1udh08x.r-3s2u2q.r-qvutc0")
    profile_name = element.text
    for tweet in tweets:
        if count >= 3: 
            break
        time.sleep(4)
        content = tweet.find_element(By.CSS_SELECTOR, "div[lang]").text
        timestamp = tweet.find_element(By.CSS_SELECTOR, "time").get_attribute("datetime")

        first_occurrence = re.search(r'[.\n\t]', content)

        if first_occurrence:
            first_occurrence_index = first_occurrence.start()
            truncated_content = content[:first_occurrence_index] if content[first_occurrence_index] != "." else content[:first_occurrence_index + 1]
        else:
            truncated_content = content

        data_list.append([profile_name, count + 1, timestamp, truncated_content])
        count += 1

    with open('tweets_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(data_list)

# 팔로잉 계정 목록을 가져오기 위해 translateY()를 사용하여 페이지를 아래로 스크롤
def scroll_to_bottom():
    SCROLL_PAUSE_TIME = 1
    last_height = browser.execute_script("return document.body.scrollHeight")
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def login_twitter(browser):
    # 웹 페이지에서 id, pw 입력창 찾고 kisia 값 입력 후 랜덤시간 대기
    id_ = browser.find_element(By.XPATH, '//input[@type="text"]')
    pyperclip.copy("snleeintern")
    id_.send_keys(Keys.CONTROL, 'v')
    time.sleep(random.randint(1, 2))

    btn_click = browser.find_element(By.CLASS_NAME, "css-18t94o4.css-1dbjc4n.r-sdzlij.r-1phboty.r-rs99b7.r-ywje51.r-usiww2.r-2yi16.r-1qi8awa.r-1ny4l3l.r-ymttw5.r-o7ynqc.r-6416eg.r-lrvibr.r-13qz1uu")
    btn_click.click()

    pw = browser.find_element(By.XPATH, '//input[@type="password"]')
    pyperclip.copy("20111004")
    pw.send_keys(Keys.CONTROL, 'v')
    time.sleep(random.randint(1, 2))

    # 로그인 버튼을 xpath로 찾고 클릭
    login_button = browser.find_element(By.XPATH, '//*[@data-testid="LoginForm_Login_Button"]')
    login_button.click()

    try:
        element = browser.find_element(By.CLASS_NAME, "css-1dbjc4n.r-18u37iz.r-1pi2tsx.r-1wtj0ep.r-u8s1d.r-13qz1uu")
        print(element.text)
        if element.text == "휴대폰 번호":
            print("ok")
            input_element = browser.find_element(By.XPATH, "//input[@type='tel']")
            pyperclip.copy("01099274599")
            input_element.send_keys(Keys.CONTROL, 'v')
            time.sleep(random.randint(1, 2))

            btn_click = browser.find_element(By.XPATH, "//span[contains(text(), '다음')]")
            btn_click.click()
    except NoSuchElementException:
        print("휴대폰 번호를 찾을 수 없습니다.")


options = webdriver.ChromeOptions()
browser = webdriver.Chrome(options=options)


# 브라우저를 주소창을 통해 로그인 페이지 접근
browser.get("https://twitter.com/snleeintern/following")
browser.implicitly_wait(5)
time.sleep(random.randint(3, 5))

login_twitter(browser)
scroll_to_bottom()


# 팔로잉 계정의 리스트를 가져오기
following_list = browser.find_elements(By.XPATH, '//div[@data-testid="UserCell"]')

for idx, _ in enumerate(following_list):
    following_list = browser.find_elements(By.XPATH, '//div[@data-testid="UserCell"]')

    following_account = following_list[idx]
    ActionChains(browser).move_to_element(following_account).click().perform()

    time.sleep(4)
    following_list = browser.find_elements(By.XPATH, '//div[@data-testid="UserCell"]')
    #여기 주석이 게시글 들어가는 클릭하는 코드!!! 
    
    post_list = browser.find_elements(By.XPATH, '//div[@data-testid="tweet"]')

    # Loop through each post
    for idt, _ in enumerate(post_list):
        # Re-fetch the post_list after scrolling to avoid StaleElementReferenceException
        post_list = browser.find_elements(By.XPATH, '//div[@data-testid="tweet"]')

        # Click on the current post using ActionChains
        post = post_list[idt]
        ActionChains(browser).move_to_element(post).click().perform()

        # Wait for the new page to load (You may adjust the wait time as needed)
        time.sleep(2)

        # Do your desired actions here
        # For example, you can retrieve information or perform tasks on this post page

        # Go back to the previous page (user's profile page)
        browser.execute_script("window.history.go(-1)")

        # Random wait before clicking the next post
        time.sleep(random.uniform(2, 4))
    

    following_LastData(browser)

    browser.execute_script("window.history.go(-1)")
    time.sleep(random.uniform(2, 4))


browser.close()
