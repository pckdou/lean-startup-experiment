"""(시뮬레이션) 페르소나 확률에 따라 가상 방문자를 만들어 이벤트 로그를 쌓는다.
사용: python personas/simulate_traffic.py 20   # 하루치 방문자 수
결과 user_id는 sim_ 로 시작하므로 실제 사용자와 구분된다."""
import sys, random, yaml, uuid
from app.app import app

n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
personas = yaml.safe_load(open("personas/personas.yaml", encoding="utf-8"))
client = app.test_client()

for _ in range(n):
    p = random.choice(personas)
    uid = f"sim_{p['id']}_{uuid.uuid4().hex[:6]}"
    client.get(f"/?uid={uid}")
    html = client.get(f"/signup?uid={uid}").get_data(as_text=True)
    variant = "B" if "간단 2단계" in html else "A"
    if random.random() < p[f"signup_prob_{variant}"]:
        client.post(f"/signup?uid={uid}", data={"email": "x", "password": "x"})
        if random.random() < 0.6:
            client.post(f"/use-feature?uid={uid}")
print(f"simulated {n} visitors")
