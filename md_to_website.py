from flask import Flask, render_template, Markup
import os

app = Flask(__name__)

@app.route('/')
def index():
    # 마크다운 파일 경로 설정 (여기서는 같은 디렉토리 내의 sample.md 파일로 가정합니다)
    markdown_file = os.path.join(os.path.dirname(__file__), 'aa.md')
    
    # 마크다운 파일 내용 읽기
    with open(markdown_file, 'r', encoding='utf-8') as file:
        markdown_content = file.read()

    return render_template('index.html', markdown_content=Markup(markdown_content))

if __name__ == '__main__':
    app.run(debug=True)
