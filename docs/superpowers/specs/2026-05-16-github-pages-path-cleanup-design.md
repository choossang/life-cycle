# GitHub Pages 경로 정리 설계서

작성일: 2026-05-16
범위: `life-cycle` 저장소의 GitHub Pages 공개 경로 정리
목표: `docs/`를 단일 배포 루트로 고정하고, 공개 홈·문서 직접 링크·디렉터리 진입 경로의 404를 제거한다.

## 1. 목표와 완료 정의

### 목표
- GitHub Pages 배포 기준을 `docs/` 하나로 통일한다.
- 공개 링크를 모두 `https://choossang.github.io/life-cycle/...` 기준으로 정리한다.
- 사용자가 유지하길 원하는 Markdown 직접 링크가 실제 배포 파일 경로와 일치하도록 맞춘다.
- 사람이 진입할 가능성이 있는 디렉터리 URL에 `index.html`을 제공해 404를 줄인다.

### 완료 정의
다음이 모두 충족되면 이 작업을 완료로 본다.
1. 공개 홈이 `docs/index.html` 기준으로 동작한다.
2. 설치 문서와 공개 설계 문서가 `docs/` 아래 실제 파일로 존재한다.
3. `docs/`, `docs/superpowers/`, `docs/superpowers/specs/` 진입 시 안내 페이지가 열린다.
4. 저장소 내 HTML 링크가 모두 `/life-cycle/` 기준과 `docs/` 배포 구조에 맞게 정리된다.
5. 더 이상 Pages 바깥 경로를 공개 링크로 안내하지 않는다.

## 2. 현재 상태와 문제 원인

### 현재 상태
- 저장소 루트에 `index.html`이 있다.
- `docs/index.html`도 별도로 존재한다.
- 공개 문서 일부는 `docs/` 아래에 있고, 일부는 `writing/INSTALL.md`처럼 `docs/` 밖에 있다.
- `docs/superpowers/specs/*.md`는 배포 루트 기준에서 직접 접근 가능하다.

### 문제 원인
- 이 저장소는 프로젝트 페이지이므로 공개 기본 경로가 `https://choossang.github.io/life-cycle/`인데, 일부 접근은 `https://choossang.github.io/...` 기준으로 시도되고 있다.
- GitHub Pages 소스가 `docs/`일 경우 URL에 다시 `/docs/`를 붙이면 경로가 어긋난다.
- 디렉터리 URL은 해당 디렉터리에 `index.html`이 없으면 404가 난다.
- `writing/INSTALL.md`처럼 배포 루트 밖 파일은 직접 링크로 열 수 없다.

## 3. 변경 원칙

- GitHub Pages 공개 자산은 `docs/` 아래만 둔다.
- Markdown 직접 링크는 가능하면 파일 이동보다 `docs/` 내부 정식 위치를 만드는 방식으로 보존한다.
- 루트 `index.html`은 Pages 실배포 기준과 충돌하지 않도록 `docs/index.html`와 메시지를 맞춘다.
- 불필요한 리다이렉트 체인보다 실제 파일 배치를 우선한다.

## 4. 배포 구조 설계

### 공식 공개 루트
- 공식 사이트 루트: `https://choossang.github.io/life-cycle/`
- 파일 시스템 배포 루트: `docs/`

### 공개 홈
- `docs/index.html`를 공식 홈으로 유지한다.
- 홈에는 다음만 안내한다.
  - 사이트 소개
  - 공개 에세이 링크
  - 공개 문서 인덱스 링크
  - 설치 문서 링크

### 문서 직접 링크
- 현재 공개 유지 대상인 Markdown 파일은 모두 `docs/` 아래 실제 파일로 존재하게 맞춘다.
- `writing/INSTALL.md`는 `docs/INSTALL.md`로 복제 또는 이동해 공개 링크를 안정화한다.
- 공개 설계 문서는 `docs/superpowers/specs/` 아래 현재 구조를 유지한다.

### 디렉터리 진입 경로
다음 디렉터리에는 `index.html`을 둔다.
- `docs/`
- `docs/superpowers/`
- `docs/superpowers/specs/`

각 인덱스 페이지는 해당 디렉터리의 역할과 주요 링크만 간단히 보여준다.

## 5. 파일별 변경 설계

### 수정 대상
- `docs/index.html`
  - 공개 홈 링크를 현재 배포 구조에 맞게 정리한다.
  - 존재하지 않는 경로를 안내하지 않도록 수정한다.
- `index.html`
  - 루트 파일도 `docs/index.html`와 같은 공개 기준을 설명하도록 맞춘다.
  - 저장소를 로컬에서 열었을 때도 혼란이 없도록 한다.

### 추가 대상
- `docs/INSTALL.md`
  - 공개 설치 문서 경로를 고정한다.
- `docs/superpowers/index.html`
  - `superpowers` 하위 공개 문서 진입 페이지를 제공한다.
- `docs/superpowers/specs/index.html`
  - 공개 spec 목록 진입 페이지를 제공한다.

### 유지 대상
- `docs/superpowers/specs/*.md`
  - 기존 직접 링크 경로를 유지한다.
- `docs/essay.html`
  - 현재 공개 에세이 페이지로 유지한다.

## 6. 링크 정책

모든 HTML 링크는 아래 원칙을 따른다.
- `docs/`가 배포 루트이므로 내부 링크에 `/docs/`를 다시 넣지 않는다.
- 홈에서 spec 링크로 갈 때는 `superpowers/specs/<filename>.md` 형식을 사용한다.
- 설치 문서 링크는 `INSTALL.md`를 사용한다.
- 절대 URL을 문서에 표기할 때는 항상 `https://choossang.github.io/life-cycle/...` 기준을 사용한다.

## 7. 검증 계획

### 수동 검증 URL
- `https://choossang.github.io/life-cycle/`
- `https://choossang.github.io/life-cycle/INSTALL.md`
- `https://choossang.github.io/life-cycle/superpowers/`
- `https://choossang.github.io/life-cycle/superpowers/specs/`
- `https://choossang.github.io/life-cycle/superpowers/specs/2026-05-16-saju-flask-app-completion-design.md`

### 로컬 검증 항목
- `docs/index.html` 링크 클릭 시 상대 경로가 올바른지 확인한다.
- 새 `index.html` 파일들이 실제 문서로 연결되는지 확인한다.
- 더 이상 `writing/` 같은 비배포 경로를 공개 링크로 노출하지 않는지 확인한다.

## 8. 비목표

- GitHub Pages 설정 자체를 API나 CLI로 변경하지 않는다.
- Markdown 파일을 HTML로 변환하는 정적 사이트 생성기를 도입하지 않는다.
- 과거의 모든 잘못된 URL을 자동 리다이렉트로 복원하지 않는다.
  - 이번 범위는 사용자가 요청한 Markdown 직접 링크와 공식 진입 경로 정리에 한정한다.
