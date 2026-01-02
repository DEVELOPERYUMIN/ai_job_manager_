# services.py

import os
import openai
from dotenv import load_dotenv

# 1) .env 파일에서 OPENAI_API_KEY 읽기
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise RuntimeError("환경변수에 OPENAI_API_KEY가 설정되어 있지 않습니다. (.env 파일 확인)")

openai.api_key = OPENAI_API_KEY

class GPTClient:
    """
    OpenAI v1.0+ 인터페이스용 GPT 클라이언트.
    openai.chat.completions.create(...) 로 요청합니다.
    """
    def __init__(self):
        # 원하시는 모델로 바꿔도 됩니다. (예: "gpt-4o-mini" 등)
        # 처음 테스트할 땐 "gpt-3.5-turbo"가 더 무난합니다.
        self.model_name = "gpt-3.5-turbo"
        self.max_tokens = 512
        self.temperature = 0.7

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        """
        system_prompt와 user_prompt를 합쳐서 ChatCompletion 요청.
        v1.0 이상부터는 openai.chat.completions.create를 사용해야 합니다.
        반환값: GPT 응답 텍스트(문자열).
        """
        try:
            response = openai.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": user_prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"GPT 호출 중 오류 발생: {str(e)}"

# 전역 인스턴스
gpt_client = GPTClient()


def give_resume_feedback(original_text: str) -> dict:
    """
    두 단계 GPT 호출을 통해:
    1) 자소서를 매끄럽게 고친 'edited_text' 생성
    2) 원본과 수정본을 비교한 'feedback' 생성

    반환값: { "edited_text": str, "feedback": str }
    """
    # 1) edited_text 생성
    system_prompt_edit = (
        "당신은 뛰어난 글쓰기 전문가입니다. "
        "사용자가 올린 자기소개서를 더 자연스럽고 매끄럽게 고쳐 주십시오. "
        "불필요한 중복을 제거하고, 표현을 풍부하게 만들어 주세요."
    )
    user_prompt_edit = original_text
    edited_text = gpt_client.chat(system_prompt_edit, user_prompt_edit)

    # 2) feedback 생성
    system_prompt_feedback = (
        "당신은 뛰어난 글쓰기 전문가입니다. "
        "아래의 “원본”과 “수정된 문장”을 비교하여, "
        "무엇을 어떻게 고쳤는지 간략하지만 구체적으로 설명해 주세요.\n"
        "예시 형식:\n"
        "1) “~한 부분”을 “~로” 바꾸어 …\n"
        "2) “~”를 삭제하고 …\n"
        "3) “~”라는 표현을 추가해 …"
    )
    user_prompt_feedback = (
        f"원본:\n{original_text}\n\n"
        f"수정된 문장:\n{edited_text}"
    )
    feedback = gpt_client.chat(system_prompt_feedback, user_prompt_feedback)

    return {
        "edited_text": edited_text,
        "feedback": feedback
    }


def generate_resume(name: str, role: str, experience_years: int, experience_list: str) -> str:
    """
    GPT를 이용해 새 자기소개서를 생성합니다.
    입력:
      - name (이름)
      - role (희망 직무)
      - experience_years (경력 연차)
      - experience_list (경력 및 경험 요약)
    반환값: 생성된 자소서 문자열
    """
    system_prompt = (
        "당신은 전문 자기소개서 작성 코치입니다. 사용자의 이름, 희망 직무, 경력 정보를 받아 "
        "그에 맞는 포맷으로 깔끔하고 설득력 있는 자기소개서를 작성해 주세요."
    )
    user_prompt = (
        f"이름: {name}\n"
        f"희망 직무: {role}\n"
        f"경력 연차: {experience_years}년\n"
        f"경력 요약: {experience_list}\n\n"
        "위 정보를 토대로 한 편의 완성된 자기소개서를 작성해 주세요."
    )
    generated_text = gpt_client.chat(system_prompt, user_prompt)
    return generated_text


def generate_interview_questions(user_id: int, company: str, role: str) -> list:
    """
    GPT를 이용해 면접 질문 리스트를 생성합니다.
    입력:
      - company (지원 회사)
      - role (지원 직무)
    반환값: 질문 문자열 리스트
    """
    system_prompt = (
        "당신은 기업 면접관 교육을 담당하는 전문가입니다.  "
        "면접 질문은 행동 기반이어야 하며, 지원자가 직접 경험한 상황을 이끌어내는 데 초점을 맞춥니다.  " 
        "각 질문은 반드시 어떤 상황이었나요? 또는 어떻게 대응했나요? 처럼 구체적인 행동을 유도하는 형식이어야 합니다.  질문은 모호하지 않고, 지원 직무의 실제 상황을 반영해야 합니다."
    )
    user_prompt = (
        f"지원 직무: {role}\n"
        f"회사명: {company}\n\n"
        "위 직무와 회사에 적합한 행동면접 질문 5개를 만들어 주세요."
        "각 질문은 지원자가 실제 경험을 바탕으로 답할 수 있도록 구체적이고 직무 연관성이 있어야 합니다."
    )
    response = gpt_client.chat(system_prompt, user_prompt)

    # GPT가 “1. 질문… 2. 질문…” 형태로 반환해 줄 것이므로,
    # 줄바꿈('\n')을 기준으로 분리하거나, 간단히 콤마로 분할할 수도 있습니다.
    # 여기서는 줄바꿈을 기준으로 리스트화하는 예시:
    lines = [line.strip() for line in response.split("\n") if line.strip()]
    # "1. ~", "2. ~" 와 같은 형식을 제거하고, 질문 텍스트만 추출
    questions = []
    for line in lines:
        # "1. 질문 내용" -> "질문 내용"으로
        if "." in line:
            parts = line.split(".", 1)
            question_text = parts[1].strip()
        else:
            question_text = line
        questions.append(question_text)
    return questions


def evaluate_interview_answer(answer_text: str) -> dict:
    """
    GPT를 이용해 사용자 답변을 채점하고 피드백을 생성합니다.
    입력:
      - answer_text (사용자가 입력한 면접 답변 내용)
    반환값: { "score": float, "feedback": str }
    """
    system_prompt = (
        "당신은 면접관입니다. 아래 면접 답변을 5점 만점으로 채점하고, "
        "왜 그 점수를 주었는지 구체적인 피드백을 작성해 주세요."
    )
    user_prompt = f"면접 답변: {answer_text}"
    response = gpt_client.chat(system_prompt, user_prompt)

    # 예시로 응답이 "점수: 4.0\n피드백: ~~~" 형태로 온다고 가정하고 파싱합니다.
    # 실제 응답 형식에 맞춰 아래 파싱 로직을 조정해야 할 수 있습니다.
    lines = [line.strip() for line in response.split("\n") if line.strip()]
    score = 0.0
    feedback = ""
    for line in lines:
        if line.lower().startswith("점수") or line.lower().startswith("score"):
            # "점수: 4.0" 또는 "Score: 4.0" 같은 형식 처리
            parts = line.split(":", 1)
            try:
                score = float(parts[1].strip())
            except:
                score = 0.0
        else:
            # 나머지 라인은 피드백으로 합칩니다.
            feedback += line + " "
    feedback = feedback.strip()

    return {
        "score": score,
        "feedback": feedback
    }

