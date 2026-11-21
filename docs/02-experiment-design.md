# 실험 설계

- Feature Flag: `short_onboarding` (flags.json)
- A(대조군): 5개 입력 필드 / B(실험군): 2개 입력 필드
- 배정: user_id 해시 기반 고정 배정, 50:50
- 기간: 2주 (Day0 ~ Day14)
- 이벤트: visit, signup_started, signup_completed, feature_used
- 데이터: data/events/events.jsonl
- 리포트: 매주 월요일 자동 생성(docs/reports/)

## 일정
| 기간 | 내용 |
|---|---|
| Day 0 | flag 50/50 배포 |
| Day 1~7 | 데이터 수집, 주간 리포트 #1 |
| Day 8~14 | 데이터 수집, 주간 리포트 #2 |
| Day 15 | 최종 분석, Pivot/Persevere 결정 |
