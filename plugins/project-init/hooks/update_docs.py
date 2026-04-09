#!/usr/bin/env python3
"""
verifier가 docs/.verifier_result.json 을 생성하면
자동으로 checklist.md, completion_report.md, technical_doc.md 를 업데이트한다.

이 파일은 verifier 외에 아무도 건드려서는 안 된다.
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

# 1. 훅 입력 읽기
try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

tool_name = data.get("tool_name", "")
tool_input = data.get("tool_input", {})
file_path = tool_input.get("file_path", "")

# 2. Write 툴로 .verifier_result.json 을 쓴 경우만 처리
if tool_name != "Write" or not file_path.endswith(".verifier_result.json"):
    sys.exit(0)

result_path = Path(file_path)
if not result_path.exists():
    sys.exit(0)

# 3. 결과 파일 읽기
try:
    with open(result_path) as f:
        result = json.load(f)
except Exception as e:
    print(f"[update_docs] 결과 파일 읽기 실패: {e}", file=sys.stderr)
    sys.exit(1)

docs_dir = result_path.parent
feature_name = result.get("feature_name", "알 수 없음")
timestamp = result.get("timestamp", "")
verdict = result.get("verdict", "❓")
test_items = result.get("test_items", [])
issues = result.get("issues", [])
evidence = result.get("evidence", "")
impl = result.get("implementation", {})

# ── checklist.md 업데이트 ──────────────────────────────────────────────────
checklist_path = docs_dir / "checklist.md"
if checklist_path.exists():
    content = checklist_path.read_text()
    # 해당 기능명이 있는 행 찾아서 테스트 결과 업데이트
    lines = content.splitlines()
    updated = False
    for i, line in enumerate(lines):
        if feature_name in line and "|" in line:
            parts = line.split("|")
            if len(parts) >= 5:
                parts[3] = f" {verdict} "
                parts[4] = f" {timestamp} "
                lines[i] = "|".join(parts)
                updated = True
                break
    if updated:
        checklist_path.write_text("\n".join(lines))
        print(f"[update_docs] checklist.md 업데이트 완료: {feature_name}")

# ── completion_report.md 업데이트 ─────────────────────────────────────────
report_path = docs_dir / "completion_report.md"
if report_path.exists():
    content = report_path.read_text()

    # 테이블 마지막 행 다음에 항목 추가
    issues_text = "\n".join(f"- {i}" for i in issues) if issues else "없음"
    test_rows = "\n".join(
        f"| {t['item']} | {t['result']} | {t.get('note','')} |"
        for t in test_items
    )
    section = f"""
### {feature_name} — {timestamp}
**판정**: {verdict}

**검증 항목**
| 항목 | 결과 | 비고 |
|------|------|------|
{test_rows}

**발견된 문제**: {issues_text}

**검증 근거**: {evidence}

---"""

    # 테이블 아래 빈 행 찾아서 항목 삽입
    marker = "| # | 기능 | 판정 | 완료일 (KST) | 비고 |"
    if marker in content:
        # 테이블 끝 찾기
        lines = content.splitlines()
        for i, line in enumerate(lines):
            if line.strip() == "" and i > content.find(marker):
                # 테이블 다음 첫 빈 줄 이후에 삽입
                lines.insert(i + 1, section)
                break
        else:
            lines.append(section)
        report_path.write_text("\n".join(lines))
        print(f"[update_docs] completion_report.md 업데이트 완료: {feature_name}")

# ── technical_doc.md 업데이트 ─────────────────────────────────────────────
tech_path = docs_dir / "technical_doc.md"
if tech_path.exists():
    content = tech_path.read_text()

    files_text = "\n".join(
        f"- `{f['path']}` — {f['role']}"
        for f in impl.get("files", [])
    ) or "- 없음"
    interface = impl.get("interface", {})

    section = f"""
### {feature_name} — {timestamp}

**구현 내용**
{impl.get('description', '-')}

**주요 로직**
{impl.get('logic', '-')}

**관련 파일**
{files_text}

**인터페이스**
- 입력: {interface.get('input', '-')}
- 출력: {interface.get('output', '-')}

---"""

    content += section
    tech_path.write_text(content)
    print(f"[update_docs] technical_doc.md 업데이트 완료: {feature_name}")

# 4. 결과 파일 삭제 (verifier 전용 임시 파일)
result_path.unlink()
print(f"[update_docs] .verifier_result.json 삭제 완료")
