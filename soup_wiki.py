'''
요약:
이 코드는 위키피디아의 Beautiful Soup 문서에서 첫 번째 문단을 가져와, 80자 단위로 줄 바꿈해 출력하는 간단한 웹 스크래핑 예제입니다.
'''
import requests                # 웹 페이지 요청을 위한 라이브러리
from bs4 import BeautifulSoup  # HTML 파싱을 위한 라이브러리
import textwrap                # 텍스트 줄바꿈(포매팅) 라이브러리

# Beautiful Soup 위키피디아 문서의 URL 지정
url = 'https://en.wikipedia.org/wiki/Beautiful_Soup_(HTML_parser)'

# 해당 URL로 GET 요청을 보내고 응답을 받음
response = requests.get(url)

# 응답받은 HTML을 파싱하여 BeautifulSoup 객체 생성
soup = BeautifulSoup(response.content, 'html.parser')

# class가 'mw-parser-output'인 div 내부의 첫 번째 <p> 태그(문단)의 텍스트만 추출
first_paragraph = soup.find('div', class_='mw-parser-output').p.get_text()

# 추출한 문단 텍스트를 80자 기준으로 줄바꿈 처리
wrapped_text = textwrap.fill(first_paragraph, width=80)

# 결과 출력
print(wrapped_text)
