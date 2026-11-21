"""10명의 LLM 페르소나(Gemini 무료 API)가 서비스를 평가하고 피드백 JSON을 data/feedback/ 에 저장한다."""
import os, json, time, yaml, pathlib
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"], http_options=types.HttpOptions(timeout=60000))

def pick_model():
    """GEMINI_MODEL 환경변수가 있으면 우선 사용, 없으면 사용 가능한 flash 모델을 자동 선택."""
    if os.getenv("GEMINI_MODEL"):
        return os.environ["GEMINI_MODEL"]
    names = []
    for m in client.models.list():
        n = m.name.replace("models/", "")
        actions = getattr(m, "supported_actions", None) or []
        if "generateContent" in actions and "flash" in n:
            if not any(x in n for x in ["image", "tts", "live", "audio", "embedding", "lite"]):
                names.append(n)
    stable = sorted(n for n in names if "preview" not in n and "exp" not in n)
    cand = stable or sorted(names)
    if not cand:
        raise SystemExit("사용 가능한 flash 모델을 못 찾았습니다. AI Studio에서 모델명을 확인해 .env에 GEMINI_MODEL=모델명 으로 넣으세요.")
    return cand[-1]

MODEL = pick_model()
print("사용 모델:", MODEL)

personas = yaml.safe_load(open("personas/personas.yaml", encoding="utf-8"))
product = open("docs/01-hypothesis.md", encoding="utf-8").read()
scenario = open("docs/03-user-scenarios.md", encoding="utf-8").read()
out = pathlib.Path("data/feedback"); out.mkdir(parents=True, exist_ok=True)

for p in personas:
    prompt = f"""당신은 '{p['name']}' 페르소나입니다. 특징: {p['traits']}.
아래 서비스와 사용 시나리오를 체험했다고 가정하고, 이 페르소나의 관점에서 솔직하게 평가하세요.
반드시 JSON 객체 하나만 출력하세요.
키: persona_id, usability_score(1-5 정수), would_use_again(true/false),
pain_points(문자열 리스트), liked(문자열 리스트), suggestions(문자열 리스트), comment(2문장)

[서비스/가설]
{product}

[사용자 시나리오]
{scenario}"""
    print("요청 중:", p["id"], flush=True)
    data = None
    for attempt in range(4):
        try:
            r = client.models.generate_content(
                model=MODEL, contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json"))
            text = r.text
            data = json.loads(text[text.find("{"): text.rfind("}") + 1])
            break
        except Exception as e:
            print(f"  재시도 {attempt+1}/4 ({p['id']}): {str(e)[:120]}")
            time.sleep(15 * (attempt + 1))   # 무료 한도(분당 요청 수) 초과 대비
    if data is None:
        print("실패:", p["id"]); continue
    data["persona_id"] = p["id"]; data["persona_name"] = p["name"]; data["llm_model"] = MODEL
    (out / f"{p['id']}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("done", p["id"], p["name"])
    time.sleep(5)   # 무료 한도 여유
