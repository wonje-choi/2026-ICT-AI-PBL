# 대시보드 overview API 500 오류 수정

- **ID**: 001
- **날짜**: 2026-08-30
- **유형**: 버그 수정
- **리뷰 ID**: fhrwidhcrymazmzsaybskqeoujwbgbuc

## 작업 요약
대시보드 게시물 모델이 참조하는 데이터베이스 namespace 설정 누락을 보완했다.
프런트엔드 API 호출에 예외 처리를 추가해 HTTP 오류가 발생해도 Promise rejection과 로딩 상태가 방치되지 않도록 수정했다.

## 원문 요청사항
```text
reviewops-sdk.js:1418 
 POST https://s10.inov.seasonai.net/wiz/api/page.dashboard/overview 500 (Internal Server Error)

page.dashboard.component.ts:30 Uncaught (in promise) 
{readyState: 4, getResponseHeader: ƒ, getAllResponseHeaders: ƒ, setRequestHeader: ƒ, overrideMimeType: ƒ, …}

해당 오류를 수정 작성해줘
```

## 원인
`config/database.py`가 없어 `orm.base("post")`가 데이터베이스 설정을 찾지 못했고, `config.type` 접근에서 `AttributeError`가 발생했다.
프런트엔드는 `wiz.call("overview")` 실패를 처리하지 않아 동일 오류가 Uncaught Promise rejection으로도 노출됐다.

## 변경 파일 목록
- `config/database.py`: `post`, `base` SQLite namespace 설정 추가
- `src/app/page.dashboard/view.ts`: API 호출 예외 처리와 `finally` 기반 로딩 해제 추가
- `devlog.md`: 작업 요약 행 추가
- `devlog/2026-08-30/001-dashboard-overview-500-fix.md`: 작업 상세 기록

## 검증 결과
- WIZ 일반 빌드 성공
- 인증 세션을 포함한 `POST /wiz/api/page.dashboard/overview` 호출 결과 HTTP 200 및 응답 `code: 200`
- 통계 4건과 빈 최근 게시물 배열이 정상 JSON으로 반환됨
