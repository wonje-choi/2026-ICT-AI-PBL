# 일반 회원 역할 표시명을 회원으로 변경

- **ID**: 003
- **날짜**: 2026-09-07
- **유형**: 기능 수정
- **리뷰 ID**: ojfgbxlgrvaeijavunpajitxghsvaoqv

## 작업 요약
사용자 화면에 노출되는 `일반 회원` 역할 별칭을 `회원`으로 통일했습니다.
`관리자` 표시와 내부 권한값 `user`는 기존대로 유지했습니다.

## 원문 요청사항
```text
일반회원이란 별칭도 이상한거같아 그냥 회원 아님 사용자로 변경해줘
관리자는 변경 안해도 괜찮을꺼같아
```

## 변경 파일 목록
- `src/app/page.dashboard/view.pug`: 대시보드 역할 배지 문구 변경
- `src/app/page.members/view.pug`: 회원 안내 및 초대 선택지 문구 변경
- `src/app/page.members/view.ts`: 역할 필터 및 표시 함수 문구 변경
- `src/app/component.nav.sidebar/view.ts`: 사이드바 역할 문구 변경
- `devlog.md`: 작업 요약 행 추가
- `devlog/2026-09-07/003-member-role-label.md`: 작업 상세 기록 추가

## 검증 결과
- 프로젝트 소스 및 설정에서 `일반 회원`, `일반회원` 문구가 남아 있지 않음을 확인
- 관리자 표시와 내부 권한값 `user`가 유지됨을 diff로 확인
- WIZ 일반 빌드(`clean: false`) 성공
- `git diff --check` 통과
