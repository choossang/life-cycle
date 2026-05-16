# 사주 Flask 앱 완성 설계서

작성일: 2026-05-16
범위: `tmp_review_files/flask_saju_app_v3/flask_app/` 앱 완성
목표: 기존 단일 Flask 앱을 유지하면서 보안 핫픽스, 입력 검증, 데이터 스키마 확장, 해석 레이어, UI 반영, 로컬 검증까지 완료한다.

## 1. 목표와 완료 정의

### 목표
- 기존 `app.py`와 템플릿 구조를 유지한 채 앱을 완성 상태로 끌어올린다.
- `saju_data.json`의 원점수(`job/gui/hlt`)는 어떤 일기 입력에도 변하지 않게 유지한다.
- 일기 데이터는 해석의 근거로만 사용하고, 점수 계산과는 분리한다.
- 세션 기반 단일 사용자 앱으로서 필요한 보안 기준(XSS, CSRF, 입력 검증, 쿠키 설정)을 충족한다.

### 완료 정의
다음이 모두 충족되면 이 트랙을 완료로 본다.
1. XSS/CSRF/입력 검증이 구현되어 있다.
2. diary 스키마 확장과 안전한 마이그레이션이 구현되어 있다.
3. `GET /api/saju`는 원점수 전용으로 유지된다.
4. `GET /api/diary`는 확장된 일기 데이터와 `interpretation`을 함께 반환한다.
5. 프론트 UI에서 점수와 해석이 분리 표시된다.
6. 로컬에서 로그인, 조회, 저장, 수정, 삭제, 오류 케이스를 검증했다.

## 2. 현재 구조와 변경 원칙

### 현재 구조
- 백엔드: `flask_app/app.py` 단일 파일
- 템플릿: `templates/index.html`, `templates/login.html`
- 데이터:
  - `saju_data.json` — 월별 원점수 데이터
  - `diary.db` — 일기 저장용 SQLite

### 유지 원칙
- 앱 구조를 불필요하게 쪼개지 않는다.
- 핵심 수정은 `app.py`와 `templates/index.html` 중심으로 수행한다.
- 배포 운영에 필요한 환경변수 기반 설정은 유지한다.

## 3. 아키텍처 설계

앱은 파일 구조는 유지하되 내부 책임을 다음 다섯 구역으로 정리한다.

1. 인증/보안 설정
   - 시크릿 로딩
   - 세션 쿠키 설정
   - 로그인/로그아웃
   - CSRF 토큰 발급 및 검증

2. DB 초기화 및 마이그레이션
   - 기본 테이블 생성
   - 누락 컬럼 확인
   - 필요한 경우 `ALTER TABLE`로 확장

3. 사주 API
   - `GET /api/saju`
   - 원점수만 읽어 반환

4. 일기 API
   - `GET /api/diary`
   - `POST /api/diary`
   - `DELETE /api/diary/<date>`

5. 해석 생성
   - 원점수와 일기 근거를 읽어 해석 문자열을 계산
   - DB에 저장하지 않고 응답 시 생성

## 4. 데이터 레이어 분리

### Score Layer
- 소스: `saju_data.json`
- 필드: `job`, `gui`, `hlt`
- 특성: 읽기 전용, 불변

### Evidence Layer
- 소스: `diary` 테이블
- 필드:
  - `date`
  - `f1`, `f2`, `f3`, `f4`
  - `entry_type`
  - `confidence`
  - `source_note`
  - `created_at`
  - `updated`
- 특성: 사용자가 입력/수정 가능

### Interpretation Layer
- 소스: Score Layer + Evidence Layer
- 특성: 요청 시 생성되는 파생 데이터
- 저장 방식: DB 저장 없음, API 응답에 포함

## 5. 스키마 확장 설계

기존 `diary` 테이블을 다음 구조로 확장한다.

- `date TEXT PRIMARY KEY`
- `f1 TEXT DEFAULT ''`
- `f2 TEXT DEFAULT ''`
- `f3 TEXT DEFAULT ''`
- `f4 TEXT DEFAULT ''`
- `entry_type TEXT DEFAULT 'manual'`
- `confidence REAL DEFAULT 1.0`
- `source_note TEXT DEFAULT ''`
- `created_at TEXT DEFAULT (datetime('now','localtime'))`
- `updated TEXT DEFAULT (datetime('now','localtime'))`

### 무결성 규칙
- `date`는 내부적으로 `YYYY-MM` 형식만 허용한다.
- `entry_type`은 `manual` 또는 `retro`만 허용한다.
- `confidence`는 `0.0 <= x <= 1.0`만 허용한다.
- `f1~f4`, `source_note`에는 최대 길이 제한을 둔다.
- 기존 DB가 이미 있으면 테이블 삭제 없이 필요한 컬럼만 추가한다.

## 6. API 설계

### 유지 API
#### `GET /api/saju`
- 인증 필요
- 응답: 기존과 동일한 원점수 배열
- 변경 없음

### 확장 API
#### `GET /api/diary`
- 인증 필요
- 응답: 일기 배열
- 각 원소는 확장 필드와 `interpretation`을 포함한다.

예시 응답:
```json
[
  {
    "date": "2026-04",
    "f1": "...",
    "f2": "...",
    "f3": "...",
    "f4": "...",
    "entry_type": "manual",
    "confidence": 1.0,
    "source_note": "",
    "created_at": "2026-05-16 10:00:00",
    "updated": "2026-05-16 10:30:00",
    "interpretation": {
      "job": "...",
      "gui": "...",
      "hlt": "..."
    }
  }
]
```

#### `POST /api/diary`
- 인증 필요
- CSRF 필요
- 입력: `date`, `f1`, `f2`, `f3`, `f4`, `entry_type`, `confidence`, `source_note`
- 동작: upsert 저장
- 응답: `{ "ok": true }` 또는 일관된 에러 JSON

#### `DELETE /api/diary/<date>`
- 인증 필요
- CSRF 필요
- 동작: 해당 월 일기 삭제
- 응답: `{ "ok": true }` 또는 일관된 에러 JSON

### 에러 응답 규약
모든 예상 가능한 실패는 다음 구조를 사용한다.
```json
{ "error": "human readable message", "code": "machine_readable_code" }
```

예시 코드:
- `unauthorized`
- `invalid_json`
- `invalid_date`
- `invalid_entry_type`
- `invalid_confidence`
- `field_too_long`
- `csrf_failed`

## 7. 보안 설계

### XSS 차단
- 사용자 입력을 다시 그릴 때 `innerHTML` 문자열 삽입을 사용하지 않는다.
- 텍스트 표시는 `textContent`를 사용한다.
- 현재 `index.html`의 일기 폼/표시 렌더링 방식은 안전한 DOM 조립으로 교체한다.

### CSRF 방어
- 로그인된 세션마다 CSRF 토큰을 생성한다.
- 토큰은 템플릿에서 자바스크립트가 읽을 수 있는 방식으로 전달한다.
- `POST /api/diary`, `DELETE /api/diary/<date>`는 요청 헤더 또는 본문의 토큰을 검증한다.
- 실패 시 403과 `csrf_failed` 코드를 반환한다.

### 세션 쿠키 설정
- `SESSION_COOKIE_HTTPONLY=True`
- `SESSION_COOKIE_SAMESITE='Lax'`
- HTTPS 배포 환경에서 `SESSION_COOKIE_SECURE=True`

### 입력 검증
- JSON 본문이 아닌 경우 400 반환
- `date` 형식은 정규식으로 `YYYY-MM` 검증
- `entry_type` 화이트리스트 검증
- `confidence` 숫자/범위 검증
- 각 텍스트 필드 길이 제한 검증

## 8. 해석 레이어 설계

### 원칙
- 해석은 점수를 수정하지 않는다.
- 해석은 일기의 내용을 요약하거나 점수 맥락을 설명하는 텍스트만 생성한다.
- 값이 없는 경우에도 점수 기반 기본 문구를 제공할 수 있다.

### 출력 형태
`interpretation`은 월별 객체로 제공한다.
```json
{
  "job": "이번 달 취직운 점수는 높지 않지만, 기록된 사실과 배움 항목을 보면 준비를 다지는 흐름으로 해석할 수 있습니다.",
  "gui": "...",
  "hlt": "..."
}
```

### 생성 규칙
- 점수 구간별 기본 해석 톤을 둔다.
- `f1~f4`가 채워져 있으면 관련 문장을 후행 근거로 덧붙인다.
- `entry_type=retro`도 동일한 가중치로 취급한다.
- `confidence`는 저장은 하되 점수 변경에는 쓰지 않는다. 이번 단계에서는 해석 문구의 단정 강도를 약하게 조정하는 정도까지만 허용한다.

## 9. 프론트엔드 반영 설계

### 테이블
- 기존 월별 테이블 구조는 유지한다.
- 일기 존재 여부 표시는 유지한다.
- 날짜 검색 동작은 유지한다.

### 우측 패널
- 상단: 선택 월, 연주/월주, 점수 배지
- 중단: 해석 영역
- 하단: 4행 일기 입력 영역
- 저장/삭제 버튼은 유지한다.

### 렌더링 원칙
- 사용자 입력을 포함하는 모든 표시 영역은 안전한 DOM 생성으로 처리한다.
- 해석 영역도 문자열 템플릿으로 사용자 입력을 끼워 넣지 않는다.
- 에러 발생 시 토스트나 경고 문구로 원인을 보여준다.

### 데이터 흐름
1. 초기 로드에서 `/api/saju`, `/api/diary`를 병렬 조회한다.
2. 클라이언트는 점수 데이터와 일기 데이터를 월 키 기준으로 결합한다.
3. 월 선택 시 점수 배지, 해석, 일기 폼을 렌더링한다.
4. 저장/삭제 후 관련 상태를 갱신하고 테이블 표시를 다시 렌더링한다.

## 10. 구현 순서

1. `app.py`에 공통 응답/검증/CSRF 유틸 추가
2. DB 초기화와 스키마 마이그레이션 구현
3. `GET /api/diary` 확장 및 해석 생성 구현
4. `POST`/`DELETE` 검증 및 보안 처리 구현
5. `index.html`에서 `innerHTML` 기반 사용자 입력 렌더 제거
6. 해석 영역 UI 추가
7. 로컬 수동 검증

## 11. 테스트 전략

### 기능 테스트
- 로그인 성공/실패/잠금
- 월 선택 후 기존 일기 조회
- 새 일기 저장
- 기존 일기 수정
- 일기 삭제
- 형식 오류/길이 초과/잘못된 타입 거절

### 보안 테스트
- 스크립트 문자열 저장 후 화면에서 실행되지 않는지 확인
- CSRF 토큰 없이 저장/삭제 요청 시 차단되는지 확인
- 비로그인 상태에서 API 접근 시 401 확인

### 정합성 테스트
- 일기 저장 전후 `job/gui/hlt` 값 동일성 확인
- `GET /api/saju` 응답 구조 변화 없음 확인
- `GET /api/diary`의 `interpretation`만 변화하고 원점수는 그대로인지 확인

## 12. 비범위

이번 트랙에서는 다음을 하지 않는다.
- 다중 사용자 계정 시스템
- 점수 산식 변경
- 외부 DB 이전
- LLM 기반 동적 해석 생성
- 대규모 프론트엔드 프레임워크 전환

## 13. 결정 기록

1. 구현 방식은 현재 Flask 앱을 그대로 보강하는 방식으로 한다.
2. `GET /api/saju`는 기존처럼 원점수만 반환한다.
3. 해석 레이어는 `GET /api/diary` 응답에 포함한다.
4. 완료 기준은 보안, 스키마 확장, 해석 레이어, UI 반영, 로컬 검증 완료까지로 잡는다.
