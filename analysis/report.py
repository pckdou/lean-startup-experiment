import json, math, collections, datetime, pathlib

LOG = pathlib.Path("data/events/events.jsonl")
users = collections.defaultdict(lambda: {"variant": None, "events": set()})
if LOG.exists():
    for line in LOG.open(encoding="utf-8"):
        e = json.loads(line)
        u = users[e["user_id"]]; u["variant"] = e["variant"]; u["events"].add(e["event"])

def stats(v):
    vs = [u for u in users.values() if u["variant"] == v]
    n = len(vs)
    s = sum("signup_completed" in u["events"] for u in vs)
    f = sum("feature_used" in u["events"] for u in vs)
    return n, s, f

nA, sA, fA = stats("A"); nB, sB, fB = stats("B")
rate = lambda a, b: a / b if b else 0
pA, pB = rate(sA, nA), rate(sB, nB)

# 두 비율 차이 z-검정
z = 0.0
if nA and nB:
    p = (sA + sB) / (nA + nB)
    se = math.sqrt(p * (1 - p) * (1 / nA + 1 / nB)) or 1
    z = (pB - pA) / se
sig = "유의함(|z|>1.96)" if abs(z) > 1.96 else "유의하지 않음"

lines = [f"# 주간 리포트 ({datetime.date.today()})", "",
         "| 그룹 | 방문자 | 가입완료 | 가입완료율 | 첫기능 사용 | 사용률 |", "|---|---|---|---|---|---|",
         f"| A (5단계) | {nA} | {sA} | {pA*100:.1f}% | {fA} | {rate(fA,nA)*100:.1f}% |",
         f"| B (2단계) | {nB} | {sB} | {pB*100:.1f}% | {fB} | {rate(fB,nB)*100:.1f}% |", "",
         f"- 가입완료율 차이(B-A): **{(pB-pA)*100:+.1f}%p**",
         f"- z = {z:.2f} → {sig}",
         "- 성공 기준: B가 A보다 +15%p 이상, 각 그룹 n≥30",
         "- ※ user_id가 sim_ 으로 시작하는 데이터는 시뮬레이션입니다."]
out = pathlib.Path("docs/reports"); out.mkdir(parents=True, exist_ok=True)
path = out / f"report-{datetime.date.today()}.md"
path.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
