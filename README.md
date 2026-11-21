# Lean Startup Experiment (13주차)

AI 학습 플래너의 **온보딩 단축 가설**을 Feature Flag 기반 A/B 테스트로 검증한 Lean Startup 실험 저장소입니다.

## 1. 과제 수행 범위

| 항목 | 수행 여부 | 위치 |
|---|---|---|
| 사용자 시나리오 기반 코드 생성/평가 | ✅ | `docs/03-user-scenarios.md`, `app/` |
| LLM 페르소나 10명 피드백 수집 | ✅ | `personas/`, `data/feedback/` |
| Feature Flag 기반 A/B 테스트 2주 운영 | ✅ | `flags.json`, `app/`, `data/events/` |
| 핵심 지표 변화 측정 | ✅ | `analysis/report.py`, `docs/reports/` |
| Pivot/Persevere 결정 문서화 | ✅ | `docs/decisions/` |

## 2. 서비스와 가설

- **서비스**: 시험 일정을 입력하면 AI가 학습 계획을 만들어 주는 학습 플래너 (MVP는 핵심 기능 체험 흐름만 구현한 Fake Door 방식)
- **대상 고객**: 시험기간 대학생
- **문제**: 학습 계획을 세우다 포기하거나, 가입 절차가 길어 이탈한다
- **가설**: 온보딩을 5단계에서 2단계로 줄이면 가입 완료율이 15%p 이상 오른다
- **핵심 지표**: 가입 완료율 = `signup_completed` / `visit`
- **보조 지표**: 첫 기능 사용률(`feature_used`)
- **성공 기준**: B안 완료율이 A안보다 +15%p 이상, 각 그룹 n≥30

자세한 내용: [가설](docs/01-hypothesis.md) / [실험 설계](docs/02-experiment-design.md)

## 3. 실험 설계

- **Feature Flag**: `short_onboarding` (`flags.json`, 50:50 롤아웃)
- **A(대조군)**: 가입 입력 필드 5개
- **B(실험군)**: 가입 입력 필드 2개
- **그룹 배정**: user_id를 SHA-256 해시한 값으로 고정 배정 (같은 사용자는 항상 같은 그룹)
- **이벤트**: `visit`, `signup_started`, `signup_completed`, `feature_used` (`data/events/events.jsonl`)
- **통계 검정**: 두 비율 차이 z-검정 (|z| > 1.96이면 유의)

## 4. LLM 사용 내역

| 용도 | LLM | 산출물 |
|---|---|---|
| 앱/스크립트 코드 생성 | Claude | `app/`, `analysis/`, `personas/` |
| 페르소나 10명 피드백 생성 | Gemini (`gemini-3.5-flash-lite`) | `data/feedback/p01~p10.json` |

페르소나 10명은 직업, 성향, 기술 수준이 서로 다르게 설계되었습니다 (`personas/personas.yaml`).

### 페르소나 피드백 요약
- 평균 사용성 점수: **3.1 / 5** (10명)
- 재사용 의사: (N)명 / 10명
- 공통 불만: (data/feedback 확인 후 작성)
- 공통 제안: (data/feedback 확인 후 작성)

## 5. 실험 결과

| 그룹 | 방문자 | 가입 완료 | 가입 완료율 | 첫 기능 사용률 |
|---|---|---|---|---|
| A (5단계) | () | () | ()% | ()% |
| B (2단계) | () | () | ()% | ()% |

- 가입 완료율 차이(B-A): (+/-)%p
- z값: ()
- 성공 기준 달성 여부: (달성 / 미달성)
- 주간 리포트: [docs/reports/](docs/reports/)

> **데이터 출처 주의**: 결과는 (실제 사용자 N명 기준 / 시뮬레이션 N명 포함)입니다. `sim_` 접두사의 user_id는 시뮬레이션 데이터입니다.

## 6. 한계

- 표본 크기가 작아 통계적 신뢰도에 한계가 있음
- 참여자가 지인 중심이라 실제 고객군과 편향이 있을 수 있음
- LLM 페르소나 피드백은 실제 사용자 반응을 대체하지 못함

## 7. 저장소 구조

```
├── app/                  # Flask MVP + Feature Flag
├── personas/             # 페르소나 정의, 피드백 생성 스크립트
├── data/
│   ├── feedback/         # 페르소나 10명 피드백 (JSON)
│   └── events/           # A/B 이벤트 로그 (JSONL)
├── analysis/report.py    # 지표 계산 / 리포트 생성
├── docs/                 # 가설, 실험 설계, 시나리오, 리포트, 결정 기록
├── flags.json            # Feature Flag 설정
└── requirements.txt
```

## 8. 실행 방법

```bash
python -m venv .venv
source .venv/Scripts/activate        # Windows Git Bash (Mac/Linux: source .venv/bin/activate)
pip install -r requirements.txt
cp .env.example .env                 # GEMINI_API_KEY, GEMINI_MODEL 입력

python -m app.app                    # http://localhost:5000
python personas/run_feedback.py      # 페르소나 피드백 생성
python analysis/report.py            # 지표 리포트 생성
```

API 키는 `.env`에만 보관하며 저장소에 커밋하지 않습니다.