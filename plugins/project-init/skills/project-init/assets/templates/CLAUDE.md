# CLAUDE.md — {{PROJECT_NAME}}

> 프로젝트 내용 + 개발 원칙을 합쳐 100줄 이내로 유지한다.
> 상세 코드 규칙: @docs/code_rules.md

## 프로젝트 개요

- **프로젝트명**: {{PROJECT_NAME}}
- **기술 스택**: {{TECH_STACK}}
- **목적**: {{PROJECT_DESCRIPTION}}
- **배포**: Docker 기반

## 주요 구조

```
{{PROJECT_STRUCTURE}}
```

## 빌드 및 테스트

```bash
# 빌드
{{BUILD_COMMAND}}

# 테스트 전체
{{TEST_COMMAND}}

# 테스트 단일
{{TEST_SINGLE_COMMAND}}

# 린트
{{LINT_COMMAND}}
```

## 개발 원칙

### 작업 프로세스
- 코드 작성 전 `docs/development_plan.md` 작성 필수
- 여러 파일 수정 시: 계획 → 사용자 승인 → 순차 실행
- 소단위로 분리 → 구현 → **@verifier 검증 위임** → `docs/checklist.md` 업데이트
- **소단위 기능 구현 완료 시 반드시 @verifier를 호출한다. 예외 없음.**
- 완료 후 사용자 최종 확인(완료 사인) → 전체 프로세스 문서 작성
- 연관된 소단위 묶음(기능 그룹)이 완전히 끝나면 `/compact` 실행 — 소단위마다 하지 않는다

### 코드 규칙
- 문서/주석: 한국어 (라이브러리명·API명은 영어)
- 함수: 단일 책임, 50줄 이내, 축약어 금지
- 함수 호출 깊이 1~2단계, Early Return, 중첩 반복 최대 2단계
- 매직넘버 금지 → 상수화, 인덱스 매핑은 Enum+Dict
- 정의부(상수/enum/schema) 확인 없이 코드 수정 금지

### 에러·보안
- 빈 except 금지, 에러 메시지에 원인+상황 포함
- 하드코딩 금지 → config/env, 파일 경로는 pathlib
- 외부 입력 반드시 검증, 민감 정보 출력 금지

### 디버깅
- 발생 시 `docs/debug/YYYYMMDD_이슈명.md` 작성 (원인/수정/범위/재발방지)

### 기타
- 시간 표기: KST 기준
- 1000줄↑ 파일, 5MB↑, 이미지/PDF는 사전 확인 후 진행

## 커밋 형식
```
type: English title
- 한국어 변경 내용 / 변경 이유
```
type: `feat` `fix` `refactor` `docs` `style` `test` `chore`
