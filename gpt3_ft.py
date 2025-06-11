'''
이 코드는 YouTube에서 오디오를 다운로드하고, OpenAI API를 이용해 오디오를 텍스트로 변환(트랜스크립션)한 뒤, 변환된 텍스트를 잘라서 프롬프트와 컴플리션 데이터로 만들고, 이를 활용해 GPT-3 모델을 파인튜닝하는 전체 과정을 담고 있습니다.

아래는 주요 동작 단계별 설명입니다:

라이브러리 임포트

youtube_dl: 유튜브 영상에서 오디오 다운로드에 사용
openai: OpenAI API 사용
os: 파일 경로 등 OS 관련 작업
OpenAI API Key 설정

openai.api_key에 본인의 API 키를 입력해야 합니다.
오디오 트랜스크립션 함수 정의

transcribe_audio(audio_file): 오디오 파일을 입력받아, OpenAI의 Completion API를 호출해 텍스트로 변환합니다. 실제로는 audio file path가 아니라 텍스트 스트링이 prompt로 들어가 있으니, 실제 오디오 트랜스크립션에는 적합하지 않습니다.
YouTube에서 오디오 다운로드

youtube_dl 옵션을 설정해서 가장 좋은 오디오 품질로 영상 다운로드 및 wav 파일로 추출합니다.
오디오 트랜스크립션 및 데이터 분할

변환된 텍스트를 일정 길이(prompt_length, completion_length)로 잘라서, 프롬프트와 컴플리션 리스트를 생성합니다.
GPT-3 파인튜닝

위에서 만든 프롬프트, 컴플리션을 사용해 OpenAI의 FineTune API로 모델을 파인튜닝합니다.
파인튜닝 옵션(에폭, 배치 사이즈, 러닝레이트 등)을 직접 지정합니다.
결과 출력

파인튜닝된 모델의 ID를 출력합니다.
주의

실제 OpenAI의 트랜스크립션(음성→텍스트)은 Completion API가 아닌 Whisper API 등 다른 엔드포인트를 사용해야 하며, 이 코드는 예시 수준입니다.
실제로 파인튜닝을 하려면 데이터 포맷, API 사용법 등 추가적인 보완이 필요합니다.
'''
import youtube_dl
import openai
import os

# Set up OpenAI credentials
openai.api_key = "YOUR_API_KEY"

# Define function to transcribe audio using OpenAI
def transcribe_audio(audio_file):
    response = openai.Completion.create(
        engine="davinci",
        prompt="Transcribe the following audio:\n" + audio_file,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

# Download YouTube video and extract audio using youtube_dl
url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(id)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192',
    }],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

# Transcribe audio and chop up text into prompts and completions
audio_file = "YOUR_VIDEO_ID.wav"
transcribed_text = transcribe_audio(audio_file)
prompt_length = 50
completion_length = 20
prompts = [transcribed_text[i:i+prompt_length] for i in range(0, len(transcribed_text), prompt_length)]
completions = [transcribed_text[i:i+completion_length] for i in range(prompt_length, len(transcribed_text), completion_length)]

# Fine-tune GPT-3 using prompts and completions
model_engine = "davinci"
model_name = "YOUR_MODEL_NAME"
model_prompt = "\n".join(prompts)
model_completion = "\n".join(completions)
fine_tuned_model = openai.FineTune.create(
    model=model_name,
    prompt=model_prompt,
    examples=[{"text": model_completion}],
    temperature=0.7,
    max_tokens=1024,
    n_epochs=5,
    batch_size=4,
    learning_rate=1e-5,
    labels=["transcription"],
    create= True
)

# Print the fine-tuned model's ID
print(f"Fine-tuned model ID: {fine_tuned_model.id}")
