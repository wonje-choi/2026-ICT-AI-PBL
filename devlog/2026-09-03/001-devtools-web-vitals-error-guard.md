# Chrome DevTools Web Vitals 반복 예외 호환 처리

- **ID**: 001
- **날짜**: 2026-09-03
- **유형**: 버그 수정
- **리뷰 ID**: oarkbidmxznbmkehjrrnlkknxfexnyub

## 작업 요약
Chrome DevTools Live Metrics가 동적으로 주입한 web-vitals 코드에서 발생하는 알려진 `reportAllChanges` 예외를 확인했다.
문서 초기화 시 해당 메시지와 스택이 모두 일치하는 오류만 처리하여 콘솔과 ReviewOps로 반복 전파되지 않도록 호환 가드를 추가했다.

## 원문 요청사항
```text
VM2622:2 Uncaught TypeError: Cannot read properties of undefined (reading 'startTime')
    at et.reportAllChanges (<anonymous>:2:19429)
    at <anonymous>:2:13070
    at <anonymous>:2:331
    at d (<anonymous>:2:6141)
    at <anonymous>:2:6326
    at <anonymous>:2:2895
    at n.timeout (<anonymous>:2:5652)

VM2623:2 Uncaught TypeError: Cannot read properties of undefined (reading 'startTime')
    at et.reportAllChanges (<anonymous>:2:19429)
    at <anonymous>:2:13070
    at <anonymous>:2:331
    at d (<anonymous>:2:6141)
    at <anonymous>:2:6326
    at <anonymous>:2:2895
    at n.timeout (<anonymous>:2:5652)
VM2624:2 Uncaught TypeError: Cannot read properties of undefined (reading 'startTime')
    at et.reportAllChanges (<anonymous>:2:19429)
    at <anonymous>:2:13070
    at <anonymous>:2:331
    at d (<anonymous>:2:6141)
    at <anonymous>:2:6326
    at <anonymous>:2:2895
    at n.timeout (<anonymous>:2:5652)
﻿

Press ctrl i to turn on code suggestions. Press ctrl x to disable code suggestions.
ctrl
i
 to turn on code suggestions. Don’t show again NEW

수정 작성해줘
```

## 원인
- 프로젝트 소스에는 `reportAllChanges`, Web Vitals, `PerformanceObserver` 호출이 없다.
- 오류의 `VM*`, `<anonymous>`, `et.reportAllChanges`, `n.timeout` 스택은 Chrome DevTools가 주입하는 Live Metrics용 web-vitals 코드의 공개된 알려진 오류와 일치한다.
- 애플리케이션 동작 오류가 아니라 DevTools가 수집한 성능 엔트리가 없는 상태에서 `startTime`을 읽는 외부 도구 오류다.

## 변경 파일 목록
- `src/angular/index.pug`: 알려진 DevTools Web Vitals 예외만 선별 처리하는 초기 오류 이벤트 가드 추가
- `devlog.md`: 작업 요약 행 추가
- `devlog/2026-09-03/001-devtools-web-vitals-error-guard.md`: 작업 상세 기록

## 검증 결과
- WIZ 일반 빌드 성공
- 생성된 `bundle/www/index.html`에 호환 가드가 앱 번들보다 먼저 반영된 것을 확인
- 모의 오류 이벤트로 대상 오류의 `preventDefault` 및 `stopImmediatePropagation` 호출 확인
- 동일 메시지여도 `reportAllChanges` 스택이 아닌 일반 오류는 차단하지 않음을 확인
- `git diff --check` 통과
