# 저장소 설치 및 사용 안내

## 저장소 개요
이 저장소는 다음을 한 번에 담고 있습니다.
- 글쓰기 12단계 스킬 패키지(별도 하위 폴더)
- 글쓰기 실행 결과를 정리한 `writing-workspace/`
- Flask 기반 사주 앱 산출물(`tmp_review_files/flask_saju_app_v3/` 및 공개 배포 페이지)
- 공개 문서와 설계 기록(`docs/`)

## 주요 디렉터리 안내
- `docs/` : 공개 문서, 설계/계획 결과, 공개 배포 허브(`docs/index.html`)
- `writing/` : 글쓰기 스킬 패키지(슬래시 스킬 및 설치 패키지 리소스)
- `writing-workspace/` : 글쓰기 워크플로우 산출물
- `tmp_review_files/flask_saju_app_v3/` : Flask 사주 앱 샘플 코드/산출물
- `INSTALL.md` : 이 저장소의 사용/탐색 가이드(현재 문서)

## 공개 문서 위치
저장소 공개 문서는 기본적으로 `docs/` 폴더에서 관리합니다.
- 공개 문서 허브: `docs/index.html`
- 에세이/설계 보기: `docs/index.html`에서 링크 확인
- 설치 가이드(공개 문서): `writing/INSTALL.md`로 이동 링크 제공

## Flask 사주 앱 관련 위치
- 앱 본문 및 템플릿: `tmp_review_files/flask_saju_app_v3/flask_app/`
- 라우팅/실행 엔트리: `tmp_review_files/flask_saju_app_v3/flask_app/app.py`
- 테스트: `tmp_review_files/flask_saju_app_v3/flask_app/tests/`
- 사주 원자료: `tmp_review_files/flask_saju_app_v3/flask_app/saju_data.json`
- 관련 문서: `docs/superpowers/specs/2026-05-16-saju-flask-app-completion-design.md`

## 글쓰기 스킬 패키지 위치
- 현재 `writing/` 폴더에는 패키지 아카이브(`writing/writing-skills.zip`)와 저장소용 설치 안내(`writing/INSTALL.md`)가 함께 들어 있습니다.
- 패키지 설치와 사용 절차는 `writing/INSTALL.md`를 따르세요.
- `writing/INSTALL.md`에서 스킬 폴더 설치, 점검, 시작 문구를 확인할 수 있습니다.

## 사용 시작 요약
이 저장소를 처음 열었다면 먼저 `docs/index.html`을 열어 공개 산출물의 전체 흐름을 확인하고,
`writing/INSTALL.md`로 이동해 글쓰기 스킬 패키지 설치 가이드를 진행하면 됩니다.