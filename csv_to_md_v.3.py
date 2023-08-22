import pandas as pd
import undetected_chromedriver as uc
from flask import Flask, render_template, Markup
import re
import webbrowser
import threading
import time

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


import pandas as pd
import undetected_chromedriver as uc
from flask import Flask, render_template
import re


app = Flask(__name__)

# ... (태그 변수 및 함수 정의는 그대로 유지)

@app.route('/K')
def index1():
    with open('aabb.md', 'r', encoding='utf-8') as file:
        markdown_content = file.read()
    return render_template('index.html', markdown_content=Markup(markdown_content))
@app.route('/E')
def index2():
    with open('aacc.md', 'r', encoding='utf-8') as file:
        markdown_content = file.read()
    return render_template('index.html', markdown_content=Markup(markdown_content))

if __name__ == "__main__":
    content = []
    data = pd.read_csv('three.csv')
    content.extend(data['Translated_Content'])
    all_text2 = data  # 이 부분을 수정하지 않습니다.
    print(all_text2)
    check = False
    
    with open('aabb.md', 'w', encoding='utf-8') as file:
        for index, row in all_text2.iterrows():
            if check:
                file.write(f"###위 첨부트윗 게시글###  >> {buf}\n\n")
                check = False
            file.write(f"### ###{row['Date']}\n <ul><li><h5>[{set_tag(row['Origin_Content'])}] Title</h5></li>\n")
            buf =""
            translated_sentences = split_into_sentences(row['Translated_Content'])
            for sentence in translated_sentences:
                if pd.isnull(row['AttachTweet']) and pd.isnull(row['AttachUrl']) and pd.isnull(row['ImageUrl']):
                    file.write(f"<ul><li>{sentence}</li></ul></ul>\n")
                else:
                    file.write(f"<ul><li>{sentence}</li>\n")
            if pd.notnull(row['AttachTweet']):
                buf=row['AttachTweet']
                check = True
            if pd.notnull(row['AttachUrl']):
                text = re.sub(r'\s+', '', row['AttachUrl'])
                if pd.isnull(row['ImageUrl']):
                    file.write(f"<li>{text}</li>\n<ul><li>요약..</li></ul></ul></ul>\n")
                else:
                    file.write(f"<li>{text}<ul><li>요약..</li></li>\n")
            if pd.notnull(row['ImageUrl']):
                image_urls = row['ImageUrl'].split("    ")  # 수정이 필요할 수 있음
                for image_url in image_urls:
                    image_url_with_https = image_url.strip()
                    url_pattern = r'https://\S+'
                    urls = re.findall(url_pattern, image_url)
                    for index, url in enumerate(urls):
                        if index == len(urls) - 1:
                            if pd.notnull(row['AttachUrl']):
                                file.write(f"<li> <img src=\"{url}\" alt=\"Image\"></li></ul></ul></ul>\n\n")
                            else:
                                file.write(f"<li> <img src=\"{url}\" alt=\"Image\"></li></ul></ul>\n\n")
                        else:
                            file.write(f"<li> <img src=\"{url}\" alt=\"Image\"></li>\n\n")
            else:
                file.write("\n\n")
    
    with open('aacc.md', 'w', encoding='utf-8') as file:
        for index, row in all_text2.iterrows():
            if check:
                file.write(f"###위 첨부트윗 게시글###  >> {buf}\n\n")
                check = False
            file.write(f"### ###{row['Date']}\n{row['Url']}\n<ul><li><h5>[{set_tag(row['Origin_Content'])}] Title</h5></li>\n")
            buf =""
            translated_sentences = split_into_sentences(row['Origin_Content'])
            for sentence in translated_sentences:
                if pd.isnull(row['AttachTweet']) and pd.isnull(row['AttachUrl']) and pd.isnull(row['ImageUrl']):
                    file.write(f"<ul><li>{sentence}</li></ul></ul>\n")
                else:
                    file.write(f"<ul><li>{sentence}</li>\n")
            if pd.notnull(row['AttachTweet']):
                buf=row['AttachTweet']
                check = True
            if pd.notnull(row['AttachUrl']):
                text = re.sub(r'\s+', '', row['AttachUrl'])
                if pd.isnull(row['ImageUrl']):
                    file.write(f"<li>{text}</li>\n<ul><li>요약..</li></ul></ul></ul>\n")
                else:
                    file.write(f"<li>{text}<ul><li>요약..</li></li>\n")
            if pd.notnull(row['ImageUrl']):
                image_urls = row['ImageUrl'].split("    ")  # 수정이 필요할 수 있음
                for image_url in image_urls:
                    image_url_with_https = image_url.strip()
                    url_pattern = r'https://\S+'
                    urls = re.findall(url_pattern, image_url)
                    for index, url in enumerate(urls):
                        if index == len(urls) - 1:
                            if pd.notnull(row['AttachUrl']):
                                file.write(f"<li> <img src=\"{url}\" alt=\"Image\"></li></ul></ul></ul>\n\n")
                            else:
                                file.write(f"<li> <img src=\"{url}\" alt=\"Image\"></li></ul></ul>\n\n")
                        else:
                            file.write(f"<li> <img src=\"{url}\" alt=\"Image\"></li>\n\n")
            else:
                file.write("\n\n")
    app_thread = threading.Thread(target=app.run)
    app_thread.start()

    # 웹 브라우저 자동 열기를 별도 스레드에서 처리
    def open_browser():
        time.sleep(2)  # 앱이 실행되기를 기다립니다.
        webbrowser.open("http://127.0.0.1:5000/K")
        webbrowser.open("http://127.0.0.1:5000/E")

    browser_thread = threading.Thread(target=open_browser)
    browser_thread.start()
