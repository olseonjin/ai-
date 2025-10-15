import google.generativeai as genai
import time
import json

GOOGLE_API_KEY = "AIzaSyCChSzPdpWaHdQekR3OYZYQ7XOpA4pyZOs"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction="""
        당신은 한국어로 답변하는 친근한 AI입니다. 
        사용자가 입력한 문장을 받으면, 다음을 수행하세요:

    1. 사용자의 MBTI를 글 내용 기반으로 추측합니다.
    2. 추측한 MBTI와 궁합이 좋은 MBTI의 말투와 스타일로 답변을 생성합니다.
    3. 답변은 자연스럽고 부드러운 한국어 말투로 작성합니다. 지나치게 딱딱하거나 과장되지 않게 작성합니다.
    4. 출력 형식은 JSON으로, 다음 구조를 따릅니다:
    {
      "user_mbti": "<추측한 MBTI>",
      "response": "<생성된 답변>"
    }
    점 괄호 영어 쓸대없는 문구 텍스트 없애기
    """
)


user_input = input("사용자 입력: ")

user_prompt = user_input

response = model.generate_content(
    user_prompt,
    generation_config={
        "temperature": 0.1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 1000,
        "response_mime_type": "application/json",
    },
    safety_settings=[
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
    ]
)

start_time = time.time()

try:
    data = json.loads(response.text)
    print(json.dumps({
        "message": "성공",
        "answer": data
    }, ensure_ascii=False, indent=2))
except Exception as e:
    print("JSON 파싱 실패. 원본 응답:")
    print(response.text)
finally:
    end_time = time.time()
    print(f"실행 시간: {end_time - start_time:.2f} 초")