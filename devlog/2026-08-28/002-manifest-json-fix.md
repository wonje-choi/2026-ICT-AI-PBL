# 웹 앱 manifest JSON 파싱 오류 수정

- **ID**: 002
- **날짜**: 2026-08-28
- **유형**: 오류 수정

## 작업 요약

존재하지 않는 `/manifest.json` 요청이 SPA HTML로 대체되어 브라우저가 JSON 문법 오류를 출력하던 문제를 수정했다.
유효한 Web App Manifest를 정적 자산 경로에 추가하고 문서의 manifest 링크를 실제 제공 경로로 변경했다.

## 원문 요청사항

```text
Manifest: Line: 1, column: 1, Syntax error.
manifest.json:1 Manifest: Line: 1, column: 1, Syntax error.

해당 오류 수정 작성해줘
```

## 변경 파일 목록

- `src/angular/index.pug`
  - manifest 링크를 `/manifest.json`에서 `/assets/manifest.json`으로 변경
- `src/assets/manifest.json`
  - 앱 이름, 시작 URL, 표시 모드, 테마 색상 및 아이콘 정보를 포함한 유효한 manifest 추가
- `devlog.md`
  - 오류 수정 요약 행 추가
- `devlog/2026-08-28/002-manifest-json-fix.md`
  - 요청, 변경 파일 및 검증 결과 기록

## 확인 결과

- WIZ 일반 빌드 성공
- 소스와 빌드 산출물의 manifest를 `python -m json.tool`로 파싱 성공
- 빌드된 `index.html`이 `/assets/manifest.json`을 참조함을 확인
- 운영 URL이 HTTP 200 및 `Content-Type: application/json`으로 유효한 JSON을 반환함을 확인
- `git diff --check` 이상 없음
