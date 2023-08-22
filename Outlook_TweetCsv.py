from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import random, time, pyperclip
import csv
import requests
from datetime import datetime
from pprint import pprint
import urllib.request
import re
import win32com.client
import re

urlsaaa=[]
# test라는 outlook COM 객체 생성(Dispatch)
# 생성한 test 객체를 통해 Outlook을 제어할 수 있다.
test = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

#6 : 받은 편지함(inbox folder)를 의미함.
root_folder = test.Folders.Item(1)
inboxfolder = root_folder.Folders['DDW']
messages = inboxfolder.Items

#받은편지함에 있는 메일 개수를 입력받는 변수 : msg_count
msg_count = messages.count
print("받은편지함 메시지 수 : " + str(msg_count) + "건")
i =0
#출력을 위한 index 번호
# 받은편지함 messgae를 각각 루프문을 돌아 필요한 내용 파싱
for ms in messages:
    if ms.UnRead:
        #print(str(i) + "번째 메일의 발신인 : " + ms.SenderName)
        #print(str(i) + "번째 메일의 수신인 : " + ms.To)
        #print(str(i) + "번째 메일의 제목 : " + ms.Subject)
        print(str(i) + "번째 메일의 받은시간 : " + str(ms.ReceivedTime))
        #print(str(i) + "번째 메일의 내부내용 : " + ms.Body)

        buf_url='aaa'
        if "https://twitter.com" in ms.Body:
            # URL 추출을 위한 정규 표현식 패턴
            url_pattern = r"(https?://twitter\.com\S+)"
            urls = re.findall(url_pattern, ms.Body)

            # 추출한 URL 출력
            for url in urls:
                print("URL: " + url.replace(')에',''))
                urlsaaa.append(url)
                break
        i = i+1

header = ['AttachCheck','Profile','Url','Date','Content', 'Translated_Conten','ImageUrl','AttachTweet','AttachUrl']
sub_link = False
Index = 'X'
with open("twitter_8_10.csv", mode='w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file)
    headers = []
    headers=header
    writer.writerow(header)

def Toko1(egtext):
    client_id = 'cx7ahlDf9_dx1T_JavyS'
    client_secret = 'Ucny4yIyC6'
    kocText = urllib.parse.quote(egtext)
    data = "source=en&target=ko&text=" + kocText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    response = requests.post(url, headers=headers, data=data.encode("utf-8"))
    if response.status_code == 200:
        result = response.json()
        translated_text = result['message']['result']['translatedText']
    else:
        print(f"An error occurred: {response.status_code}")
    return translated_text
#트위터 접속 url을 본 url로 바꿔주는 함수
def extract_real_url(twitter_url):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # 브라우저 창이 뜨지 않도록 headless 모드로 실행
        browser = webdriver.Chrome(options=options)
        browser.get(twitter_url)
        time.sleep(5) 
        real_url = browser.current_url
        browser.quit()
        return real_url
    except Exception as e:
        print(f"An error occurred: {e}")
        return None  
#줄바꿈 없애는 함수
def no_space(text):
    text1 = re.sub('&nbsp; | &nbsp;|\n\n|\t|\r|', '', text)
    text2 = re.sub('\n\n\n', '', text1)
    text3 = re.sub('\n\n', '', text2)
    text3 = re.sub('\n', '', text2)
    text4 = re.sub(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', ' ', text3)
    text5 = re.sub(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\?)\n', '. ', text4)
    return text5
#statu 다음 숫자 가져오는 함수
def extract_status_id_from_url(url):
    try:
        # URL에서 status/ 다음에 있는 숫자 값을 추출하는 정규표현식
        pattern = r'status/(\d+)'
        match = re.search(pattern, url)
        
        if match:
            status_id = match.group(1)
            return int(status_id)
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
def profile(browser):
    buf_profile=''
    for c_box in browser.find_elements(By.CLASS_NAME, "css-901oao.r-1awozwy.r-18jsvk2.r-6koalj.r-37j5jr.r-a023e6.r-b88u0q.r-rjixqe.r-bcqeeo.r-1udh08x.r-3s2u2q.r-qvutc0"):
            try:
                contents = c_box.find_element(By.CLASS_NAME, "css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0")
                buf_profile=contents.text
            except: pass
    return buf_profile
def date(browser):
    month = {"jan": "/1/", "feb": "/2/", "mar": "/3/", "apr": "/4/", "may": "/5/", "jun": "/6/","jul": "/7/", "aug": "/8/", "sep": "/9/", "oct": "/10/", "nov": "/11/", "dec": "/12/"}
    buf_date=''
    for c_box in browser.find_elements(By.CLASS_NAME, "css-1dbjc4n.r-1d09ksm.r-1471scf.r-18u37iz.r-1wbh5a2"):
            try:
                contents = c_box.find_element(By.TAG_NAME, "time")
                date_time = contents.get_attribute("datetime")
                parsed_date_time = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S.000Z")
                formatted_date = parsed_date_time.strftime("%Y") + month[parsed_date_time.strftime("%b").lower()] + parsed_date_time.strftime("%d")
                buf_date=formatted_date
            except: pass
    return buf_date
def maintext(browser):
    buf_OC, buf_TC= '', '' #OrignContent(OC), TranslateContent(TC)
    for c_box in browser.find_elements(By.CLASS_NAME, "css-1dbjc4n.r-1s2bzr4"):
            try:
                contents = c_box.find_element(By.CLASS_NAME, "css-901oao.r-18jsvk2.r-37j5jr.r-1inkyih.r-16dba41.r-135wba7.r-bcqeeo.r-bnwqim.r-qvutc0")
                OC = no_space(contents.text)
                buf_OC = OC
                TC= Toko1(OC)
                buf_TC=TC
            except: pass
    return buf_OC, buf_TC
def attach_tweet(browser,browser_url):
    buf_AT ='' #AttachTweet's Url(AT)
    for c_box in browser.find_elements(By.CLASS_NAME, "css-1dbjc4n.r-1ets6dv.r-1867qdf.r-rs99b7.r-1loqt21.r-adacv.r-1ny4l3l.r-1udh08x.r-o7ynqc.r-6416eg"): 
            try:
                contents = c_box.find_element(By.TAG_NAME, "a")
                AT = contents.get_attribute("href")
                AT = extract_real_url(AT)
                if AT.startswith("https://twitter.com"):
                    if all(item not in AT for item in ["photo", "profile", "pbs"]):
                        buf_AT = AT
                    elif "photo" in AT:
                        browser_id = extract_status_id_from_url(browser_url)
                        AT_id = extract_status_id_from_url(AT)
                        if browser_id == AT_id: continue
                        else: buf_AT = AT
            except:
                pass
    return buf_AT
def attach_externalUrl(browser):
    buf_AE=''
    for c_box in browser.find_elements(By.CLASS_NAME, "css-4rbku5.css-18t94o4.css-901oao.css-16my406.r-1cvl2hr.r-1loqt21.r-poiln3.r-bcqeeo.r-qvutc0"):
            try:
                AE = c_box.get_attribute("href")
                AE = extract_real_url(AE)
                if AE.startswith("https://twitter.com"):
                    continue
                buf_AE=AE
                #BingAI 쓰는 코드(CAPTURE때문에 제외시킴)
            except:
                pass
    for c_box in browser.find_elements(By.CLASS_NAME, "css-1dbjc4n.r-1ets6dv.r-1867qdf.r-1phboty.r-rs99b7.r-1ny4l3l.r-1udh08x.r-o7ynqc.r-6416eg"): 
            try:
                content = c_box.find_element(By.TAG_NAME, "a")
                AE = content.get_attribute("href")
                if AE.startswith("https://t.co/"):
                    AE = extract_real_url(AE)
                elif AE.startswith("https://twitter.com"):
                    continue
                buf_AE=AE
            except:
                pass
    return buf_AE
def image(browser):
    buf_IU=''
    for c_box in browser.find_elements(By.CLASS_NAME, "css-1dbjc4n.r-9aw3ui"):
            try:
                for content in browser.find_elements(By.TAG_NAME, "img"):
                    IU = content.get_attribute("src") 
                    if not IU.startswith("https://pbs.twimg.com"):
                        continue
                    elif IU.startswith("https://pbs.twimg.com/profile_images"):
                        continue
                    buf_IU+=IU + "\t"
            except:
                pass
    return buf_IU

def save_csv(browser_url,browser):
    global sub_link
    global Index 
    row_data = []
    Profile = Date = Origin_Content = Translated_Content = ImageUrl = AttachTweet = AttachUrl = ''
    sub_link =False
    Index = 'X'
    while True:
        browser.get(browser_url)
        browser.implicitly_wait(5)
        row_data=[]
        if sub_link == True: Index = 'O'
    
        Profile = profile(browser)                              #Twitter Profile 함수
        Date = date(browser)                                    #Twitter Date 함수
        Origin_Content, Translated_Content = maintext(browser)  #Twitter Content 함수
        AttachTweet = attach_tweet(browser,browser_url)         #Twitter 또다른 Twitter URL 함수
        AttachUrl = attach_externalUrl(browser)                 #Twitter 본문에 잇는 외부 링크 & #Twitter 본문 밖에 있는 외부 링크(ex. 뉴스) 함수
        ImageUrl = image(browser)

        with open("twitter_8_10_ver2.csv", mode='a', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file)
            row_data.append(Index)
            row_data.append(Profile)
            row_data.append(browser_url)
            row_data.append(Date)
            row_data.append(Origin_Content)
            row_data.append(Translated_Content)
            row_data.append(ImageUrl)
            row_data.append(AttachTweet)
            row_data.append(AttachUrl)
            writer.writerows([row_data])

        if AttachTweet=='':
            sub_link = False
            Index = 'X'
            break
        else:
            browser_url = AttachTweet
            Profile = Date = Origin_Content = Translated_Content = ImageUrl = AttachTweet = AttachUrl = ''
            sub_link = True
            row_data = []

# 팔로잉 계정 목록을 가져오기 위해 translateY()를 사용하여 페이지를 아래로 스크롤
def scroll_to_bottom(browser):
    SCROLL_BY_HEIGHT = 500
    last_height = 0
    while True:
        browser.execute_script(f"window.scrollBy(0, {SCROLL_BY_HEIGHT});")
        time.sleep(2)
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
#timestamp로 최신 트윗의 url 수집
def scroll_to_tweet(browser, date):
    SCROLL_BY_HEIGHT = 1000
    while True:
        browser.execute_script(f"window.scrollBy(0, {SCROLL_BY_HEIGHT});")
        time.sleep(2)
        scroll_position = browser.execute_script("return window.pageYOffset;")
        time_element = browser.find_elements(By.CSS_SELECTOR, "time")
        timestamp_str = time_element[0].get_attribute("datetime") if time_element else "No timestamp found"
        
        if timestamp_str != "No timestamp found":
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            print(timestamp)
        else:
            timestamp = None
        
        if scroll_position >= 5000 or timestamp.date() > date.date():
            break

def login(browser):
    # 브라우저를 주소창을 통해 로그인 페이지 접근
    browser.get("https://twitter.com/snleeintern/following")
    browser.implicitly_wait(5)

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
#수집된 Tweet Url들 데이터 수집
def all_following_tweet_url(browser):
    tweet_urls =[]
    desired_date = datetime.strptime("2023-08-10T03:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")

    following_list = browser.find_elements(By.XPATH, '//div[@data-testid="UserCell"]')
    for idx, _ in enumerate(following_list):
        count = 0
        count_check = True
        following_list = browser.find_elements(By.XPATH, '//div[@data-testid="UserCell"]')

        following_account = following_list[idx]
        ActionChains(browser).move_to_element(following_account).click().perform()
        browser.implicitly_wait(5)
        while count_check:
            for c_box in browser.find_elements(By.CSS_SELECTOR, "article"):
                try:
                    contents = c_box.find_element(By.CLASS_NAME, "css-4rbku5.css-18t94o4.css-901oao.r-14j79pv.r-1loqt21.r-xoduu5.r-1q142lx.r-1w6e6rj.r-37j5jr.r-a023e6.r-16dba41.r-9aw3ui.r-rjixqe.r-bcqeeo.r-3s2u2q.r-qvutc0")
                    time_element = c_box.find_elements(By.CSS_SELECTOR, "time")
                    timestamp_str = time_element[0].get_attribute("datetime")
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                    if timestamp > desired_date:
                        tweet_url = contents.get_attribute("href")
                        if tweet_url not in tweet_urls:
                            tweet_urls.append(tweet_url)
                    else:
                        count=count+1
                        print("pass" + timestamp_str)
                        if(count==3):
                            count_check = False
                except:
                    pass
            scroll_to_tweet(browser, desired_date)
        browser.execute_script("window.history.go(-1)")
        time.sleep(random.uniform(2, 4))
    browser.close()
    print(tweet_urls)
    return tweet_urls


def main():
    options = webdriver.ChromeOptions()
    '''browser = webdriver.Chrome(options=options)
    browser.get("https://twitter.com/snleeintern/following") #following 페이지 접속
    browser.implicitly_wait(5)
    login(browser)  # 로그인 함수
    scroll_to_bottom(browser)  # 계정 리스트 받아오기
    all_tweet=all_following_tweet_url(browser) # 최신 트윗 URL 리스트 받아오기
    browser.quit()'''
    
    print(len(urlsaaa))
    options.add_argument("--headless")
    browser_for_tweets = webdriver.Chrome(options=options)
    for url in urlsaaa:
        print(url)
        if "https" in url:  
            save_csv(url,browser_for_tweets)  # 최신 트윗 URL 접속 및 데이터 수집
        else:
            pass
    browser_for_tweets.quit()


if __name__ == "__main__":
    main()
