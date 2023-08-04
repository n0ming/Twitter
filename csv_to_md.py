import pandas as pd
from tabulate import tabulate

# CSV 파일로부터 데이터를 읽어옴
data = pd.read_csv('ttwitter.csv')

# 데이터를 원하는 방식으로 정리 (예시: 모든 열을 포함하는 경우)
table = tabulate(data, headers='keys', tablefmt='pipe', numalign='left')  # numalign='left'로 설정

# Markdown 테이블을 파일로 저장 (UTF-8 인코딩)
with open('sample.md', 'w', encoding='utf-8') as file:
    file.write(table)
