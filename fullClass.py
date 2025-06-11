'''
이 코드는 LucidateTextSplitter라는 클래스를 정의하여, 주어진 긴 텍스트를 n개의 문장 단위로 나누고, 이를 프롬프트(prompt)와 완성(completion) 쌍의 데이터로 변환해 다양한 파일 형식(엑셀, CSV, JSON)으로 저장하는 기능을 제공합니다. 전체 동작은 다음과 같습니다:

### 1. import 및 클래스 정의
- **import re, pandas as pd, json**: 정규식, 데이터프레임, JSON 파일 저장을 위해 필요한 라이브러리들을 불러옵니다.
- **class LucidateTextSplitter**: 텍스트 분할 및 파일 저장을 담당하는 클래스입니다.

### 2. 클래스 생성자
- **__init__(self, text, n)**: 
    - text: 입력할 텍스트(문자열)
    - n: 몇 문장 단위로 나눌지 결정하는 정수

### 3. 주요 메서드 설명
- **split_into_sentences_with_prompts(self)**:
    - 입력 텍스트를 문장 단위로 정규식으로 나눕니다.
    - n개마다 프롬프트로 삼고, 그 사이의 문장들을 완성(completion)으로 만듭니다.
    - 프롬프트와 완성 쌍을 데이터프레임(pandas DataFrame)으로 반환합니다.
    - 예외처리(빈 텍스트, n이 0 이하, 문장 수 부족)도 수행합니다.

- **save_as_excel(self, filename)**: 
    - 위에서 만든 데이터프레임을 엑셀 파일로 저장합니다.

- **save_as_csv(self, filename)**: 
    - 데이터프레임을 CSV 파일로 저장합니다.

- **save_as_json(self, filename)**:
    - 데이터프레임을 JSON 형식으로 저장합니다.

### 4. 사용 예시 (코드 하단)
- 텍스트 예시(여러 문장으로 구성), n=3으로 설정
- LucidateTextSplitter 객체 생성
- split_into_sentences_with_prompts()로 분할 및 데이터프레임 생성
- 데이터프레임을 출력(print)
- JSON, CSV, Excel 파일로 각각 저장

---

### 전체 요약
- 긴 텍스트를 n문장씩 끊어서 "프롬프트-완성" 형태의 데이터셋을 만드는 도구입니다.
- 데이터는 엑셀, CSV, JSON 등 여러 포맷으로 저장할 수 있습니다.
- 텍스트 분할, 파일 저장, 예외처리 등 데이터 전처리에 유용합니다.

'''
import re
import pandas as pd
import json

class LucidateTextSplitter:
    def __init__(self, text, n):
        self.text = text
        self.n = n

    def split_into_sentences_with_prompts(self):
        if self.text == "":
            raise ValueError("Input text cannot be empty.")
        if self.n <= 0:
            raise ValueError("n must be a positive integer.")
        sentences = re.split("(?<=[.!?]) +", self.text)
        if len(sentences) < self.n:
            raise ValueError("Input text must have at least n sentences.")
        prompts = sentences[::self.n]
        completions = []
        for i in range(len(prompts) - 1):
            completion = " ".join(sentences[self.n * i + 1:self.n * (i + 1)])
            completions.append(completion)
        completions.append(" ".join(sentences[self.n * (len(prompts) - 1) + 1:]))
        data = {'prompt': prompts, 'completion': completions}
        df = pd.DataFrame(data)
        return df

    def save_as_excel(self, filename):
        df = self.split_into_sentences_with_prompts()
        df.to_excel(filename, index=False)
    def save_as_csv(self, filename):
        df = self.split_into_sentences_with_prompts()
        df.to_csv(filename, index=False)
    def save_as_json(self, filename):
        df = self.split_into_sentences_with_prompts()
        data = []
        for i in range(len(df)):
            row = {'prompt': df.iloc[i]['prompt'], 'completion': df.iloc[i]['completion']}
            data.append(row)
        with open(filename, 'w') as f:
            json.dump(data, f)



text = "OpenAI's GPT-3 can be fine-tuned for specialized purposes, opening up a new level of AI for industries. " \
       "Chatbots and assistants can be enhanced to better meet user needs and provide more personalized service. " \
       "Fine-tuning also leads to more accurate and precise natural language processing (NLP), enabling complex human-" \
       "like interactions. The implications for future AI technology are immense, with the potential to open up new " \
       "markets and applications. Fine-tuning also makes machine learning more accessible, democratizing the field " \
       "and making it easier to adopt. All of this adds up to a technological milestone that has the potential to s" \
       "ignificantly impact how we interact with AI in the future. With GPT-3's ability to learn and adapt, the " \
       "future looks bright for those who can harness the power of this impressive technology. The process of " \
       "fine-tuning could help revolutionize industries and create new opportunities for innovation. The potential of " \
       "GPT-3's fine-tuning is limitless, and we are only beginning to scratch the surface of what is possible."
n = 3
splitter = LucidateTextSplitter(text, n)
df = splitter.split_into_sentences_with_prompts()
print(df)
splitter.save_as_json("Split.json")
splitter.save_as_csv("Split.csv")
splitter.save_as_excel("Split.xlsx")
