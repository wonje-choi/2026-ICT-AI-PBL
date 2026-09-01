# main.js 불완전 캐시 로드 오류 방지

- **ID**: 001
- **날짜**: 2026-09-01
- **유형**: 버그 수정
- **리뷰 ID**: sasoltylpswvywltnaqdrtxemgxmpxfs

## 작업 요약
내용이 없는 `/sw.js`를 반복 등록하던 코드를 제거했다.
기존 브라우저에 남아 있는 Service Worker 등록과 Cache Storage를 1회 정리하고, 구 Service Worker가 현재 문서를 제어할 때만 한 번 새로고침하도록 변경했다.

## 원문 요청사항
```text
Uncaught SyntaxError: Unexpected end of input (at main.js:1:2)
해당 오류도 수정해줘
```

## 원인
배포 서버의 `main.js`는 로컬 빌드 파일과 크기 및 SHA-256이 동일하고 문법 검사도 통과했다.
그러나 앱은 실제 내용이 0바이트인 `/sw.js`를 계속 등록하고 있어, 기존 Service Worker 또는 Cache Storage에 남은 불완전한 번들이 브라우저에 제공될 수 있었다.

## 변경 파일 목록
- `src/angular/index.pug`: 빈 Service Worker 등록 제거 및 기존 등록·캐시 정리 로직 추가
- `devlog.md`: 작업 요약 행 추가
- `devlog/2026-09-01/001-main-js-cache-cleanup.md`: 작업 상세 기록

## 검증 결과
- WIZ 일반 빌드 성공
- 생성된 `main.js`의 `node --check` 문법 검사 성공
- 배포된 `main.js`와 로컬 산출물의 크기 및 SHA-256 일치 확인
- 배포 페이지에서 신규 정리 로직 반영 및 기존 `serviceWorker.register` 제거 확인
- `git diff --check` 통과
