from selenium import webdriver
from selenium.webdriver.common.by import By
import time, random
import requests
import os
from datetime import datetime
import asyncio, json
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
from pprint import pprint
import urllib.request
import sys
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import win32com.client
import re
import csv   
import pandas as pd

browser_url="https://twitter.com/BrettCallow/status/1686204534673248256"

month = {"jan": "1월", "feb": "2월", "mar": "3월", "apr": "4월", "may": "5월", "jun": "6월",
        "jul": "7월", "aug": "8월", "sep": "9월", "oct": "10월", "nov": "11월", "dec": "12월"}
url_num = 0
img_num = 0
profile =''
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
sub_twitter_url=''
client_id = 'cx7ahlDf9_dx1T_JavyS'
client_secret = 'Ucny4yIyC6'
sub_link=False
# 폴더 생성
folder_path = "이미지 저장 경로"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

#csv
header = ['Index','Profile','Date','Origin_Content','Translated_Content','ImageUrl','AttachTweet','AttachUrl']
row_data = []
Profile =''
Date=''
Origin_Content=''
Translated_Content=''
ImageUrl=''
AttachTweet=''
AttachUrl=''
Index=0
csv_file = f"twitter.csv"

with open(csv_file, mode='w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file)
    headers = []
    headers.append(header)
    writer.writerow(header)  # 헤더를 CSV 파일에 작성


#url edge gpt 요약
async def main(href):
    try:
        cookies = json.loads(open("./bing_cookies_test.json", encoding="utf-8").read())
        bot = await Chatbot.create(cookies=cookies)

        prompt = href + "Summarize the contents of the URL in Korean"
        response = await bot.ask(prompt=prompt, conversation_style=ConversationStyle.creative, simplify_response=True)
        print(response["text"])
        buf = response["text"]

        await bot.close()
        return buf
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
#트위터 접속 url을 본 url로 바꿔주는 함수
def extract_real_url(twitter_url):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # 브라우저 창이 뜨지 않도록 headless 모드로 실행
        browser = webdriver.Chrome(options=options)
        browser.get(twitter_url)
        time.sleep(5)  # 웹 페이지 로딩 대기 (적절한 대기 시간을 설정해주세요)

        real_url = browser.current_url
        browser.quit()
        return real_url
    except Exception as e:
        print(f"An error occurred while fetching the real URL: {e}")
        return None
#한국어로 번역
def Toko1(egtext):
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
        print('Twitter_Content 번역 후:', translated_text)
    else:
        print("Error Code:", response.status_code)
    return translated_text
#줄바꿈 없애는 함수
def no_space(text):
    text1 = re.sub('&nbsp; | &nbsp;|\n\n|\t|\r|', '', text)
    text2 = re.sub('\n\n\n', '', text1)
    text3 = re.sub('\n\n', '', text2)
    text3 = re.sub('\n', '', text2)

    # Modify the regex to check for a period before a newline
    text4 = re.sub(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', ' ', text3)

    # Check if a period exists before a newline and add it if not
    text4 = re.sub(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\?)\n', '. ', text4)
    text4 = re.sub(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.)\n', '. ', text4)

    return text4
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
            print("Status ID not found in the URL.")
            return None
    except Exception as e:
        print(f"Error while extracting status ID: {str(e)}")
        return None
def replace_decimal_with_zero(num):
    str_num = str(num)
    if '.' in str_num:
        integer_part, decimal_part = str_num.split('.')
        if len(decimal_part) > 0 and int(decimal_part[0]) >= 1:
            return int(integer_part)  # Convert back to integer if the decimal part is 1 or greater
    return num  # Return the original number if the condition is not met

while True:
    img_num = 0
    browser = webdriver.Chrome()
    browser.get(browser_url)
    browser.implicitly_wait(5)
    time.sleep(random.randint(3, 5))

    with open('html_code.txt', 'a', encoding='utf-8') as file:
        url_num+=1
        if sub_link == True:
            file.write("\n================================================================\n")
            file.write(f"Twitter 추가 게시글 : {browser_url}")
            Index = Index + 0.1 - 1.0 - 0.1
        else:
            file.write("\n================================================================")
        #Twitter Profile
        for c_box in browser.find_elements(By.CLASS_NAME, "css-901oao.r-1awozwy.r-18jsvk2.r-6koalj.r-37j5jr.r-a023e6.r-b88u0q.r-rjixqe.r-bcqeeo.r-1udh08x.r-3s2u2q.r-qvutc0"):
            try:
                contents = c_box.find_element(By.CLASS_NAME, "css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0")
                print("Twitter_Profile : "+contents.text)
                profile = contents.text
                file.write("\n"+"[Twitter_Profile]\n"+contents.text+"\n")
                Profile=contents.text
                if sub_link == False:
                    replace_decimal_with_zero(Index)
                    Index= Index + 1.0
                else:
                    Index = Index +1.0
                break
            except:
                pass
        #Twitter Date
        for c_box in browser.find_elements(By.CLASS_NAME, "css-1dbjc4n.r-1d09ksm.r-1471scf.r-18u37iz.r-1wbh5a2"):
            try:
                contents = c_box.find_element(By.TAG_NAME, "time")
                date_time = contents.get_attribute("datetime")
                parsed_date_time = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S.000Z")
                formatted_date = parsed_date_time.strftime("%Y년 ") + month[parsed_date_time.strftime("%b").lower()] + parsed_date_time.strftime(" %d일")
                print("Twitter_Date : " + formatted_date)
                file.write("\n"+"[Twitter_Date]\n"+formatted_date+"\n")
                Date=formatted_date
            except:
                pass
        #Twitter 내용
        for c_box in browser.find_elements(By.CLASS_NAME, "css-1dbjc4n.r-1s2bzr4"):
            try:
                contents = c_box.find_element(By.CLASS_NAME, "css-901oao.r-18jsvk2.r-37j5jr.r-1inkyih.r-16dba41.r-135wba7.r-bcqeeo.r-bnwqim.r-qvutc0")
                cleaned_content = no_space(contents.text)
                print("Twitter_Content : "+cleaned_content)
                Origin_Content = cleaned_content
                file.write("\n[Twitter 원본 내용]\n"+ cleaned_content+"\n")
                translate_text = Toko1(cleaned_content)
    
                # 여러 줄일 경우 다 못가져옴. 특히 해쉬태그 : contents = c_box.find_element(By.CLASS_NAME, "css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0")
                file.write("\n[Twitter 번역 내용]\n"+ translate_text+"\n")
                Translated_Content=translate_text
            except:
                pass
        #Twitter 또다른 Twitter URL
        for c_box in browser.find_elements(By.CLASS_NAME, "css-1dbjc4n.r-1ets6dv.r-1867qdf.r-rs99b7.r-1loqt21.r-adacv.r-1ny4l3l.r-1udh08x.r-o7ynqc.r-6416eg"): 
            try:
                contents = c_box.find_element(By.TAG_NAME, "a")
                twitter_url = contents.get_attribute("href")
                print("Twitter_href : " + twitter_url)
                real_url = extract_real_url(twitter_url)
                if real_url.startswith("https://twitter.com"):
                    if not "photo" in real_url and not "profile" in real_url and not "pbs" in real_url:
                        sub_twitter_url = real_url 
                        print("sub_twitter_url : " + sub_twitter_url)
                        file.write("\n[Twitter 추가 게시글]\n"+ sub_twitter_url+"\n")
                        AttachTweet=sub_twitter_url
                    elif "photo" in real_url:
                        status_id = extract_status_id_from_url(browser_url)
                        statusSub_id = extract_status_id_from_url(real_url)
                        if status_id == statusSub_id:
                            file.write("\n[Twitter 추가 게시글]\n없습니다\n")
                            continue
                        else:
                            sub_twitter_url = real_url 
                            print("sub_twitter_url : " + sub_twitter_url)
            except:
                file.write("\n[Twitter 추가 게시글]\n없습니다\n")
                pass
        #Twitter 본문에 잇는 외부 링크
        for c_box in browser.find_elements(By.CLASS_NAME, "css-4rbku5.css-18t94o4.css-901oao.css-16my406.r-1cvl2hr.r-1loqt21.r-poiln3.r-bcqeeo.r-qvutc0"):
            try:
                twitter_url = c_box.get_attribute("href")
                real_url = extract_real_url(twitter_url)
                if real_url.startswith("https://twitter.com"):
                    continue
                file.write("\n[Out_href]\n"+real_url+"\n")
                AttachUrl=real_url
                #asyncio.run(main('https://unit42.paloaltonetworks.com/cloaked-ursa-phishing/'))
                #file.write("\n"+asyncio.run(main(real_url))+"\n")
            except:
                pass

        #Twitter 본문 밖에 있는 외부 링크(ex. 뉴스)
        for c_box in browser.find_elements(By.CLASS_NAME, "css-1dbjc4n.r-1ets6dv.r-1867qdf.r-1phboty.r-rs99b7.r-1ny4l3l.r-1udh08x.r-o7ynqc.r-6416eg"): 
            try:
                contents = c_box.find_element(By.TAG_NAME, "a")
                twitter_url = contents.get_attribute("href")
                if twitter_url.startswith("https://t.co/"):
                    print(twitter_url)
                    real_url = extract_real_url(twitter_url)
                elif real_url.startswith("https://twitter.com"):
                    continue
                print("Out_href : " + real_url)
                AttachUrl=real_url
                #file.write("\n"+"[Outr_href]\n"+real_url +"\n"+ asyncio.run(main(real_url))+"\n")
                file.write("\n"+"[Outr_href]\n"+real_url +"\n")
            except:
                pass
        image_index = 0
        for c_box in browser.find_elements(By.CLASS_NAME, "css-1dbjc4n.r-9aw3ui"):
            try:
                for a in c_box.find_elements(By.TAG_NAME, "a"):
                    href_value = a.get_attribute("href")
                    print("href_value : "+href_value)
                    ImageUrl+=href_value+" || "
                    image_index+=1
                    # 여기서부터 이미지 다운로드 등의 작업 수행
                    # ...
            except:
                pass

        #Twitter Image
        for c_box in browser.find_elements(By.CLASS_NAME, "css-1dbjc4n.r-9aw3ui"):
            try:
                for a in browser.find_elements(By.TAG_NAME, "img"):
                    img_src = a.get_attribute("src") 
                    if not img_src.startswith("https://pbs.twimg.com"):
                        continue
                    elif img_src.startswith("https://pbs.twimg.com/profile_images"):
                        continue
                    response = requests.get(img_src, headers=headers)
                    if response.status_code == 200:
                        img_num += 1
                        file_name = f"{url_num}_{profile}_{img_num}.jpg"  # 저장할 이미지 파일명
                        file_path = os.path.join(folder_path, file_name)
                        with open(file_path, "wb") as f:
                            f.write(response.content)
                        time.sleep(random.randint(3, 5))
                        if img_num > 1:
                            file.write("\n"+file_name)
                        else :
                            file.write("\n"+"[Twitter image]\n"+file_name)
                            ImageUrl+=img_src+" || "
                        print(file_name)
                    if img_num == image_index:
                        break
                        # print(response.content, response.headers)
            except:
                pass
        with open(csv_file, mode='a', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file)
            row_data.append(Index)
            row_data.append(Profile)
            row_data.append(Date)
            row_data.append(Origin_Content)
            row_data.append(Translated_Content)
            row_data.append(ImageUrl)
            row_data.append(AttachTweet)
            row_data.append(AttachUrl)
            writer.writerows([row_data])
        browser.close()

    if sub_twitter_url=='':
        sub_link = False
        break
    else:
        browser_url=sub_twitter_url
        sub_link = True
        sub_twitter_url=''
        row_data = []
        Profile =''
        Date=''
        Origin_Content=''
        Translated_Content=''
        ImageUrl=''
        AttachTweet=''
        AttachUrl=''
