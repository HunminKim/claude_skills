# Claude Code 플러그인 마켓플레이스

HunminKim의 개인 Claude Code 플러그인 저장소.

## 새 환경에서 사용하기

### 1. 마켓플레이스 등록

`~/.claude/settings.json` 에 아래 내용을 추가한다:

```json
{
  "extraKnownMarketplaces": {
    "hunminkim": {
      "source": {
        "source": "github",
        "repo": "HunminKim/claude"
      }
    }
  }
}
```

### 2. 플러그인 설치

```bash
claude plugins install project-init@hunminkim
```

### 3. 리로드

Claude Code 재시작 또는 `/reload-plugins`

---

## 플러그인 목록

### project-init

프로젝트 시작 시 개발 환경을 한 번에 초기화한다.

**호출:** `/project-init` 또는 "프로젝트 초기화해줘"

**생성되는 것들:**
- `docs/development_plan.md` — 개발 계획서
- `docs/context_note.md` — 맥락 노트
- `docs/checklist.md` — 체크리스트
- `docs/debug/` — 디버그 패치 노트 폴더
- `.claude/agents/verifier.md` — 소단위 검증 전담 서브에이전트
- `CLAUDE.md` — 개발 원칙 요약 (100줄 이내)

---

## 플러그인 업데이트

```bash
claude plugins update project-init@hunminkim
```
