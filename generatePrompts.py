'''
이 코드는 긴 텍스트를 n개의 문장 단위로 나누어 프롬프트(prompt)와 정답(completion) 쌍을 만들어주는 Python 스크립트입니다.

주요 기능 설명:

split_into_sentences_with_prompts 함수:
입력 텍스트(text)를 마침표/느낌표/물음표 뒤의 공백 기준으로 문장 단위로 분리합니다.
n개마다 하나씩 프롬프트(prompt)로 선택합니다.
각 프롬프트 뒤에 오는 n-1개의 문장들을 completion(정답)으로 만듭니다.
마지막 프롬프트 뒤에 남은 문장들을 마지막 completion에 넣습니다.
프롬프트와 정답 쌍을 pandas DataFrame으로 반환합니다.
'''
import re  # 정규표현식 사용을 위한 모듈
import pandas as pd  # 데이터프레임 생성을 위한 pandas 모듈

def split_into_sentences_with_prompts(text, n):
    # 입력된 텍스트를 문장 단위로 나누고, n개마다 프롬프트와 컴플리션을 생성하는 함수
    sentences = re.split("(?<=[.!?]) +", text)  # 문장 단위로 텍스트 분할
    prompts = sentences[::n]  # n개마다 프롬프트로 사용할 문장 선택
    completions = []  # 컴플리션을 저장할 리스트
    for i in range(len(prompts) - 1):
        # 각 프롬프트 다음부터 다음 프롬프트 전까지의 문장들을 컴플리션으로 설정
        completion = " ".join(sentences[n*i+1:n*(i+1)])
        completions.append(completion)
    # 마지막 프롬프트에 대한 컴플리션(남은 문장들)
    completions.append(" ".join(sentences[n*(len(prompts)-1)+1:]))
    data = {'prompt': prompts, 'completion': completions}  # 데이터 딕셔너리 생성
    df = pd.DataFrame(data)  # pandas DataFrame으로 변환
    return df  # 결과 반환

text = "This is sentence 1. This is sentence 2. This is sentence 3. This is sentence 4. This is sentence 5. This is sentence 6. This is sentence 7. This is sentence 8. This is sentence 9. This is sentence 10."
n = 5  # 프롬프트마다 포함할 문장 개수
df = split_into_sentences_with_prompts(text, n)  # 함수 실행
print(df)  # 결과 출력


