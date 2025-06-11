'''
transcriber.py 전체 코드 설명:

이 파일은 주로 유튜브 영상을 텍스트로 변환(트랜스크립션)하고, 변환된 텍스트를 문장 단위로 분할하여 프롬프트/컴플리션 데이터셋으로 저장하는 기능을 제공합니다. 주요 클래스와 기능은 다음과 같습니다.

---

### 1. LucidateTextSplitter 클래스

- **역할**: 트랜스크립트(텍스트)를 문장 단위로 나누고, 일정 간격(n)마다 프롬프트와 컴플리션을 생성하여 데이터프레임 및 파일로 저장.

- **주요 메소드**
  - `__init__(self, text, n)`: 분할 대상 텍스트와 n(프롬프트 분할 간격) 저장.
  - `split_into_sentences_with_prompts(self)`: 
    - 텍스트를 문장 단위로 분할.
    - n개마다 프롬프트와 컴플리션을 생성.
    - 결과를 pandas DataFrame으로 반환.
  - `save_as_excel(self, filename)`: 위 결과를 엑셀 파일로 저장.
  - `save_as_csv(self, filename)`: 위 결과를 CSV 파일로 저장.
  - `save_as_json(self, filename)`: 위 결과를 JSON 파일로 저장.

---

### 2. LucidateTranscriber 클래스

- **역할**: 유튜브 영상에서 오디오를 추출해 mp3로 저장하고, Whisper 모델로 트랜스크립트 생성 및 문장 분할.

- **주요 메소드**
  - `__init__(self, model_path)`: Whisper 모델 로드.
  - `save_to_mp3(self, url)`: 
    - 유튜브 URL에서 오디오 다운로드(mp3 변환).
    - yt_dlp 라이브러리 사용.
  - `transcribe_youtube_video(self, url, fp16=False, n=5, op_name='transcribe')`: 
    - 유튜브 영상에서 mp3 추출 → Whisper로 텍스트 변환 → LucidateTextSplitter로 문장 분할 및 엑셀 저장.
    - 결과 데이터프레임 반환.

---

### 3. 기타

- whisper, yt_dlp, pandas, re, json 등 다양한 라이브러리 사용
- Whisper로 음성 인식, yt_dlp로 유튜브 오디오 다운로드 및 변환

---

### 전체 흐름

1. 유튜브 URL을 입력받아 오디오(mp3) 추출
2. Whisper로 오디오를 텍스트로 변환
3. 변환된 텍스트를 n문장마다 프롬프트/컴플리션 쌍으로 분할
4. 엑셀/CSV/JSON 등 파일로 저장 가능

'''
import re
import pandas as pd
import json
import whisper
# import youtube_dl per https://github.com/mrspiggot/prompts_and_completions/issues/1
import yt_dlp as youtube_dl

class LucidateTextSplitter:
    def __init__(self, text, n):
        self.text = text
        self.n = n

    def split_into_sentences_with_prompts(self):
        print(self.text)
        print(type(self.text))
        if self.text == "":
            raise ValueError("Input text cannot be empty.")
        if self.n <= 0:
            raise ValueError("n must be a positive integer.")
        sentences = re.split("(?<=[.!?]) +", self.text['text'])
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

class LucidateTranscriber:
    def __init__(self, model_path):
        self.model = whisper.load_model(model_path)

    def save_to_mp3(self, url):
        options = {'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3', 'preferredquality': '192'}]}
        with youtube_dl.YoutubeDL(options) as downloader:
            downloader.download([url])

        return downloader.prepare_filename(downloader.extract_info(url, download=False)).replace(".m4a", ".mp3")

    def transcribe_youtube_video(self, url, fp16=False, n=5, op_name='transcribe'):
        filename = self.save_to_mp3(url)
        text = self.model.transcribe(filename, fp16=fp16)
        splitter = LucidateTextSplitter(text, n)
        splitter.save_as_excel(f'{op_name}.xlsx')

        return splitter.split_into_sentences_with_prompts()

