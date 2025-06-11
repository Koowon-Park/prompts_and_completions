# prompts_and_completions
Some sample code to accompany the 'Prompts and Completions' GPT-3 video on YouTube

# __프로젝트 요약:__

이 프로젝트는 GPT-3 모델을 미세 조정하기 위한 프롬프트와 완료를 생성하는 데 사용되는 다양한 스크립트와 클래스를 포함합니다. 스크립트는 웹사이트에서 텍스트를 스크랩하고, YouTube 비디오에서 오디오를 추출하고, 오디오를 텍스트로 변환하고, 텍스트를 문장으로 분할하고, 문장을 프롬프트와 완료로 나누어 데이터프레임으로 저장하는 기능을 제공합니다. 또한, 데이터프레임을 엑셀, CSV, JSON 파일로 저장하는 기능도 제공합니다.

## 이 프로젝트는 다음과 같은 주요 기능을 제공합니다.

- 웹사이트에서 텍스트 스크랩 (`scrape_5quotes.py`, `scrape_quotes.py`, `soup_wiki.py`)
- YouTube 비디오에서 오디오 추출 (`gpt3_ft.py`, `transcriber.py`)
- 오디오를 텍스트로 변환 (`gpt3_ft.py`, `transcriber.py`)
- 텍스트를 문장으로 분할 (`para2sentence.py`, `fullClass.py`, `promptsClass.py`, `transcriber.py`)
- 문장을 프롬프트와 완료로 분할 (`fullClass.py`, `promptsClass.py`, `transcriber.py`)
- 데이터프레임을 엑셀, CSV, JSON 파일로 저장 (`fullClass.py`, `guardian.py`, `news_api.py`, `transcriber.py`)
- 뉴스 기사 수집 (`guardian.py`, `news_api.py`)

이 프로젝트는 GPT-3 모델을 미세 조정하기 위한 데이터를 생성하는 데 유용한 도구 모음입니다.

## 파일 설명
`.gitignore` 파일은 `detailed script.txt`, `sample.json`, `venv/`, `.env` 파일을 무시하도록 설정되어 있습니다.

`fullClass.py` 파일은 `LucidateTextSplitter` 클래스를 정의합니다. 이 클래스는 텍스트를 문장으로 분할하고, 문장을 프롬프트와 완료로 나누어 데이터프레임으로 저장합니다. 또한, 데이터프레임을 엑셀, CSV, JSON 파일로 저장하는 기능을 제공합니다. 파일 하단에는 예시 텍스트를 사용하여 클래스를 테스트하고 결과를 파일로 저장하는 코드가 있습니다.


`generatePrompts.py` 파일은 `split_into_sentences_with_prompts` 함수를 정의합니다. 이 함수는 텍스트와 정수 n을 입력으로 받아, 텍스트를 문장으로 분할하고, 문장을 프롬프트와 완료로 나누어 데이터프레임으로 저장합니다. 파일 하단에는 예시 텍스트와 n 값을 사용하여 함수를 테스트하고 결과를 출력하는 코드가 있습니다.

`gpt3_ft.py` 파일은 YouTube 비디오에서 오디오를 추출하고, OpenAI를 사용하여 오디오를 텍스트로 변환한 다음, GPT-3 모델을 미세 조정하는 스크립트입니다. 스크립트는 `youtube_dl` 라이브러리를 사용하여 YouTube 비디오를 다운로드하고, `openai` 라이브러리를 사용하여 오디오를 텍스트로 변환하고, GPT-3 모델을 미세 조정합니다.

`guardian.py` 파일은 Guardian API를 사용하여 비즈니스 관련 기사를 검색하고, 기사의 제목과 내용을 추출하여 엑셀 파일로 저장하는 스크립트입니다. 스크립트는 `requests` 라이브러리를 사용하여 API에 요청을 보내고, `BeautifulSoup` 라이브러리를 사용하여 HTML을 파싱하고, `pandas` 라이브러리를 사용하여 데이터를 데이터프레임으로 저장합니다.

`news_api.py` 파일은 News API를 사용하여 미국의 기술 관련 최신 기사를 검색하고, 기사의 제목과 내용을 추출하여 엑셀 파일로 저장하는 스크립트입니다. 스크립트는 `requests` 라이브러리를 사용하여 API에 요청을 보내고, `BeautifulSoup` 라이브러리를 사용하여 HTML을 파싱하고, `pandas` 라이브러리를 사용하여 데이터를 데이터프레임으로 저장합니다.

`para2sentence.py` 파일은 텍스트를 문장으로 분할하는 `split_into_sentences` 함수를 정의합니다. 이 함수는 정규 표현식을 사용하여 텍스트를 문장으로 분할합니다. 파일 하단에는 예시 텍스트를 사용하여 함수를 테스트하고 결과를 출력하는 코드가 있습니다.

`promptsClass.py` 파일은 `TextSplitter` 클래스를 정의합니다. 이 클래스는 텍스트를 문장으로 분할하고, 문장을 프롬프트와 완료로 나누어 데이터프레임으로 저장합니다. 파일 하단에는 예시 텍스트를 사용하여 클래스를 테스트하고 결과를 출력하는 코드가 있습니다.

`README.md` 파일은 이 프로젝트가 YouTube의 'Prompts and Completions' GPT-3 비디오에 대한 샘플 코드임을 나타냅니다.

`scrape_5quotes.py` 파일은 `quotes.toscrape.com` 웹사이트에서 처음 5개의 인용구를 스크랩하고 인용구와 작성자를 출력하는 스크립트입니다. 스크립트는 `requests` 라이브러리를 사용하여 웹사이트에 요청을 보내고, `BeautifulSoup` 라이브러리를 사용하여 HTML을 파싱합니다.

`scrape_quotes.py` 파일은 `quotes.toscrape.com` 웹사이트에서 첫 번째 인용구를 스크랩하고 인용구와 작성자를 출력하는 스크립트입니다. 스크립트는 `requests` 라이브러리를 사용하여 웹사이트에 요청을 보내고, `BeautifulSoup` 라이브러리를 사용하여 HTML을 파싱합니다.

`soup_wiki.py` 파일은 Wikipedia에서 Beautiful Soup에 대한 첫 번째 단락을 스크랩하고 텍스트를 80자 폭으로 래핑하여 출력하는 스크립트입니다. 스크립트는 `requests` 라이브러리를 사용하여 웹사이트에 요청을 보내고, `BeautifulSoup` 라이브러리를 사용하여 HTML을 파싱합니다.

`transcriber.py` 파일은 YouTube 비디오를 다운로드하고, Whisper 모델을 사용하여 오디오를 텍스트로 변환한 다음, 텍스트를 문장으로 분할하고, 문장을 프롬프트와 완료로 나누어 엑셀 파일로 저장하는 스크립트입니다. 스크립트는 `whisper` 라이브러리를 사용하여 오디오를 텍스트로 변환하고, `youtube_dl` 라이브러리를 사용하여 YouTube 비디오를 다운로드합니다. 또한 `LucidateTextSplitter` 클래스를 사용하여 텍스트를 분할하고 저장합니다.

