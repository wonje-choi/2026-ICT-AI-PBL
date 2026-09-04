# 관리자·일반 회원 권한 분리 및 논문 대본 중심 메인 화면 개편

- **ID**: 001
- **날짜**: 2026-09-04
- **유형**: 기능 개선

## 작업 요약

회원 관리 페이지와 API를 관리자 전용으로 제한하고, 관리자·일반 회원의 가능 작업을 화면에 명시했다.
기존 통계 대시보드는 논문 URL 또는 파일을 입력해 편집 가능한 대본 구성 초안을 생성하는 시작 화면으로 개편했다.

## 원문 요청사항

```text
왜 일반 회원이 관리자와 동일하게 맴버를 보고 제거하고 그런 기능을 할 수 있어?
관리자와 일반 회원의 역활을 분명히 명시하여 가능한 작업을 나누어줘
그리고 메인 페이지에는 대시보드 보다는 논문의 주소나 파일을 넣으면 바로 대본부터해서 나오는 환경으로 구셩해줘
```

## 변경 파일 목록

- `src/app/page.members/app.json`
  - 컨트롤러를 `admin`으로 변경해 페이지/API를 관리자 전용으로 제한
- `src/app/page.members/api.py`
  - 허용 역할을 관리자와 일반 회원으로 한정하고 자기 계정 제거 방지 및 입력 검증 추가
- `src/app/page.members/view.ts`
  - 관리자 권한 확인, 한글 역할명, API 오류 처리 적용
- `src/app/page.members/view.pug`
  - 역할별 가능 작업 설명과 관리자용 역할 선택 UI 추가
- `src/app/page.members/view.scss`
  - 페이지 호스트 레이아웃 정의
- `src/app/component.nav.sidebar/view.ts`
  - 관리자 판별 및 역할명 표시 로직 추가
- `src/app/component.nav.sidebar/view.pug`
  - 일반 회원에게 회원 관리 메뉴를 숨기고 현재 역할 배지 표시
- `src/app/page.dashboard/api.py`
  - 논문 출처를 검증하고 대본 구성 초안을 임시저장하는 `prepare_script` API 추가
- `src/app/page.dashboard/view.ts`
  - URL/파일 입력, 대본 생성 및 편집 화면 이동 로직 구현
- `src/app/page.dashboard/view.pug`
  - 통계 대시보드를 논문 대본 생성 시작 화면과 역할 안내로 전면 개편
- `src/app/page.dashboard/view.scss`
  - 페이지 호스트 레이아웃 정의
- `src/app/page.access/api.py`, `src/app/page.access/view.ts`
  - 일반 회원도 로그인 후 새 메인 화면인 `/dashboard`로 이동하도록 통일
- `devlog.md`
  - 작업 요약 행 추가
- `devlog/2026-09-04/001-role-separation-paper-script-home.md`
  - 상세 작업 기록 추가

## 확인 결과

- WIZ 클린 빌드 산출물 생성 확인 후 일반 빌드 성공
- Python API 3개 파일 `py_compile` 통과
- `git diff --check` 통과
- 비로그인 상태의 회원 관리 API가 내부 응답 코드 401을 반환함을 확인
- 관리자 로그인 후 회원 목록 API가 내부 응답 코드 200을 반환함을 확인
- 잘못된 논문 URL 요청이 내부 응답 코드 400과 검증 메시지를 반환함을 확인
- 빌드 산출물에서 논문 입력 화면, 역할 설명, `admin` 컨트롤러 및 `prepare_script` 함수 반영 확인

## 제한 및 후속 작업

- 현재 생성되는 결과는 URL/파일명과 선택 옵션을 바탕으로 만든 편집용 대본 구성 초안이다.
- PDF·DOCX·HWP 본문 추출과 실제 AI 기반 논문 요약은 별도 분석 엔진 연동이 필요하다.
