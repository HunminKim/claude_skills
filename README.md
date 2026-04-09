# Claude Code 환경 설정

새 환경에서 Claude Code 설정을 빠르게 초기화한다.

## 포함 항목

- **project-init 스킬** — 프로젝트 시작 시 docs/ 구조, CLAUDE.md, verifier 에이전트 자동 생성
- **settings.json** — enabledPlugins, marketplace 설정
- **setup.sh** — 위 설정을 새 환경에 자동 적용

## 새 환경에서 사용하기

```bash
git clone https://github.com/HunminKim/claude.git ~/.claude-config
cd ~/.claude-config
bash setup.sh
```

setup.sh 가 하는 일:
1. `project-init` 스킬을 `~/.claude/plugins/cache/local/` 에 설치
2. `installed_plugins.json` 에 경로 등록 (현재 `$HOME` 기준으로 자동 설정)
3. `settings.json` 머지 (기존 설정 보존)
4. 마켓플레이스 플러그인 설치 (code-review, hookify, skill-creator, code-simplifier)

## 스킬 사용법

```
/project-init
```
또는 "프로젝트 초기화해줘", "프로젝트 시작" 등으로 호출.

실행되면:
- `docs/development_plan.md`, `context_note.md`, `checklist.md` 생성
- `.claude/agents/verifier.md` 생성 (소단위 검증 전담 서브에이전트)
- `CLAUDE.md` 생성 (개발 원칙 요약, 100줄 이내)

## 스킬 수정

```
plugins/local/project-init/1.0.0/skills/project-init/SKILL.md
plugins/local/project-init/1.0.0/skills/project-init/assets/templates/
```

수정 후 `git push` → 다른 환경에서 `git pull` + `bash setup.sh` 재실행.
