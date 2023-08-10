import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from flask import Flask, render_template, Markup
import re


driver = uc.Chrome()
app = Flask(__name__)

#Tag 변수
Leaked = ['leaked', 'leak', 'database', 'databreach', 'price', 'credit', 'address', 'breach','data', 'deep web', 'access', 'sale', 'sensitive']
Ransom = ['cl0p', 'clop', '8base', 'akira', 'anonymous', 'sudan', 'anonymoussudan', 'anonymous sudan','rhysida', 'lockbit', 'daixin', 'blackcat', 'alphv', 'monti', 'stormus', 'ransom house', 'bian lian','karakurt', 'cuba', 'quantum', 'suncrypt', 'ransomexx', 'snatch', 'blackbyte', 'everest', 'avos locker','medusa blog', 'black basta', 'ragnar locker', 'vice society', 'royal', 'play', 'lorenz', 'money Message','noescape', 'cactus', 'big head', 'movagp', 'siegedsec', 'claim', 'victim','hack','team 1919']
Leaked = ['leaked', 'leak', 'database', 'databreach', 'price', 'credit', 'address', 'breach','data', 'deep web', 'access', 'sale', 'sensitive']
Actor = ['arrest', 'developer', 'taken over', 'seized','shutdown', 'take down','takes down']
DDW = ['promote', 'sale', 'darkweb', 'ddw','stealer','malware','forum','deep web']
ransom_special =['ransom', 'ransomware','targeted', 'target']
Exploit = ['cve', 'exploit', '0day', 'zeroday', 'zero day']
CyberAttacks = ['ddos', 'cyberattacks', 'cyberattack']
IOC = ['hash', 'ioc', 'sha256', 'md5']
Intel = ['newslatter']

def set_tag(content):
    max_tag = 'Intel'
    max_count = 0

    tag_dict = {
        'Actor': Actor,
        'CyberAttacks': CyberAttacks,
        'DDW': DDW,
        'Exploit': Exploit,
        'IOC': IOC,
        'Leaked': Leaked,
        'Ransom': Ransom,
        'Intel': Intel
    }
    
    tag_counts = {tag: 0 for tag in tag_dict}
    if not content:
        return "No content available"
    content = str(content)
    words = content.split()
    has_ransom_special = False
    
    for word in words:
        word_lower = word.lower()
        for tag, tag_words in tag_dict.items():
            if any(tag_word in word_lower for tag_word in tag_words):
                tag_counts[tag] += 1     
        if any(ransom_word in word_lower for ransom_word in ransom_special):
            has_ransom_special = True

    if has_ransom_special:
        return 'Ransom'

    for tag, count in tag_counts.items():
        if count > max_count:
            max_count = count
            max_tag = tag
    
    return max_tag

def split_into_sentences(text):
    if text.endswith(('.', '?', '!')):
        text = text[:-1]
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!|\n)\s', text)
    return sentences

def enter_blank_check():
    chatgpt_text_input =(By.XPATH,'//*[@id="prompt-textarea"]')
    chatgpt_send_button =(By.XPATH,'//*[@id="__next"]/div[1]/div[2]/div/main/div[2]/form/div/div[2]/button')
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(chatgpt_text_input)
    ).send_keys(" ")
    WebDriverWait(driver, 100).until(EC.element_to_be_clickable(chatgpt_send_button))

def continue_btn_check():
    chatgpt_textcontinue_button= (By.XPATH,'//*[@id="__next"]/div[1]/div[2]/div/main/div[2]/form/div/div[1]/div/div[2]/div/button')
    while True:
        try:
            button =WebDriverWait(driver, 10).until(EC.element_to_be_clickable(chatgpt_textcontinue_button))
            if button.text=="Continue generating":
                button.click()
                enter_blank_check()
            else:
                break
        except:
            break

def get_answer():
    elements = WebDriverWait(driver, 40).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'flex.flex-grow.flex-col.gap-3')))
    last_element = elements[-1]
    li_elements = last_element.find_elements(By.TAG_NAME, 'li')
    answer = [element.text for element in li_elements]
    return answer

def init(email,password,content, command,command2):
    driver.get('https://chat.openai.com/')
    chatgpt_login_btn = (By.XPATH, '//button[div[text()="Log in"]]')
    chatgpt_username_input=(By.XPATH,'//input[@id="username"]')
    chatgpt_password_input=(By.XPATH,'//input[@id="password"]')
    chatgpt_continue_button=(By.XPATH,'//button[text()="Continue"]')
    chatgpt_continue2_button=(By.XPATH,'/html/body/div/main/section/div/div/div/form/div[3]/button')
    chatgpt_next_button=(By.XPATH,'//*[@id="radix-:rf:"]/div[2]/div/div[2]/button')
    chatgpt_done_button=(By.XPATH,'//*[@id="radix-:rf:"]/div[2]/div/div[2]/button[2]')
    chatgpt_text_input =(By.XPATH,'//*[@id="prompt-textarea"]')
    chatgpt_send_button =(By.XPATH,'//*[@id="__next"]/div[1]/div[2]/div/main/div[2]/form/div/div[2]/button')
    all_text1=[]
    all_text2=[]
    result = ' '.join([f"[{i}] {item}" for i, item in enumerate(content, start=1)])  
    driver.execute_cdp_cmd(
                'Network.setCookie',
                {
                    'domain': 'chat.openai.com',
                    'path': '/',
                    'name': 'cf_clearance',
                    'value': 'copy from cookies',
                    'httpOnly': True,
                    'secure': True,
                }
            )
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
    while True:
        #ChatGpt 제목선정 명령어 입력
        WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(chatgpt_text_input)
            ).send_keys(f"{command} 주어진 내용 : {result}")
        WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(chatgpt_send_button)
            ).click()
        
        #답변 로딩 확인
        enter_blank_check()
        continue_btn_check()
        enter_blank_check()

        #답변 가져오기
        all_text1 = get_answer()

        if len(all_text1)==len(content):
            break
        
    #ChatGpt 한국어 요약 명령어 입력
    WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(chatgpt_text_input)
        ).send_keys(f"{command2} 주어진 내용 : {result}")
    WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(chatgpt_send_button)
        ).click() 
    
    #답변 로딩 확인
    enter_blank_check()
    continue_btn_check()
    enter_blank_check()

    #답변 가져오기
    all_text2 = get_answer()

    return all_text1, all_text2

@app.route('/')
def index():
    with open('show.md', 'r', encoding='utf-8') as file:
        markdown_content = file.read()
    return render_template('index.html', markdown_content=Markup(markdown_content))


if __name__ == "__main__":
    content = []
    data = pd.read_csv('tweet.csv')
    content.extend(data['Origin_Content'])
    command1 =f"다음 주어질 {len(content)}개의 모든 내용들은 앞에 [1][2][3]과 같이 순서가 맺겨져있어. 해당 순서 다음에 있는 내용에 대해 하나도 빠짐없이 한문장짜리 짧은 한국어요약 제목을 선정해서 해당 제목앞에 1. 2. 3. 4. .. 순서를 나열해 적어줘. 이때 주어진 문장이 매우 짧거나 빈문장일 경우에는 한국어 번역한 내용을 제목으로 선정 진행해줘. 당연하게도 각각의 제목앞에 숫자를 매기는거니까 딱 결과도 {len(content)}개가 있어야해"
    command2= f"다음 주어질 {len(content)}개의 모든 내용들은 앞에 [1][2][3]과 같이 순서가 맺겨져있어. 해당 번호와 그 다음번호 사이에 있는 내용들에 대해 하나도 빠짐없이 한국어로 이해하기 쉽게 구체적으로 완전한 문장들로 만들어줘. 이때 여러문장이면 줄바꾸지말고 한줄로 나열해줘. 모든 문장끝에는 .을 붙여주고 결과로는 정리된 문장만 나열해줘"
    all_text, all_text2 = init('unst0pp4bl323@gmail.com', 'winterlaken23!', content, command1,command2)

    check =False

    with open('show.md', 'w', encoding='utf-8') as file:
        for a in range(len(all_text2)):
            row = data.iloc[a]  
            if check:
                file.write("###위 첨부트윗 게시글###\n\n")
                check =False
            file.write(f"###{row['Date']}\n- [{set_tag(row['Origin_Content'])}] {all_text[a]}\n")
            print(all_text[a])
            translated_sentences = split_into_sentences(all_text2[a])
            print(all_text2)
            for sentence in translated_sentences:
                file.write(f"  - {sentence}\n")
            if pd.notnull(row['AttachTweet']):
                file.write(f"  - 첨부트윗링크 : ({row['AttachTweet']})\n")
                check =True
            if pd.notnull(row['AttachUrl']):
                file.write(f"  - 첨부외부링크 : ({row['AttachUrl']})\n")
            if pd.notnull(row['ImageUrl']):
                image_urls = row['ImageUrl'].split("	") 
                for image_url in image_urls:
                    image_url_with_https = image_url.strip()
                    if image_url_with_https.startswith("https://"):
                        file.write(f"  - ![Image]({image_url_with_https})\n\n")
            else:
                file.write("\n\n")
    app.run()
