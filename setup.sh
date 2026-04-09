#!/bin/bash
# Claude Code 환경 초기화 스크립트
# 사용법: bash setup.sh

set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

echo "=== Claude Code 환경 초기화 ==="
echo "대상 디렉토리: $CLAUDE_DIR"
echo ""

# 1. 로컬 플러그인(project-init) 설치
echo "[1/4] project-init 스킬 설치 중..."
PLUGIN_DEST="$CLAUDE_DIR/plugins/cache/local/project-init/1.0.0"
mkdir -p "$PLUGIN_DEST"
cp -r "$REPO_DIR/plugins/local/project-init/1.0.0/." "$PLUGIN_DEST/"
echo "      완료: $PLUGIN_DEST"

# 2. installed_plugins.json 에 project-init 등록
echo "[2/4] 플러그인 등록 중..."
INSTALLED_JSON="$CLAUDE_DIR/plugins/installed_plugins.json"
NOW=$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")

if [ ! -f "$INSTALLED_JSON" ]; then
  # 파일 없으면 새로 생성
  cat > "$INSTALLED_JSON" << EOF
{
  "version": 2,
  "plugins": {
    "project-init@local": [
      {
        "scope": "user",
        "installPath": "$PLUGIN_DEST",
        "version": "1.0.0",
        "installedAt": "$NOW",
        "lastUpdated": "$NOW"
      }
    ]
  }
}
EOF
else
  # 이미 있으면 project-init 항목만 python으로 머지
  python3 - <<PYEOF
import json, sys

path = "$INSTALLED_JSON"
with open(path) as f:
    data = json.load(f)

data.setdefault("plugins", {})["project-init@local"] = [
    {
        "scope": "user",
        "installPath": "$PLUGIN_DEST",
        "version": "1.0.0",
        "installedAt": "$NOW",
        "lastUpdated": "$NOW"
    }
]

with open(path, "w") as f:
    json.dump(data, f, indent=2)
print("      updated: $INSTALLED_JSON")
PYEOF
fi
echo "      완료"

# 3. settings.json 머지 (기존 설정 보존)
echo "[3/4] settings.json 업데이트 중..."
SETTINGS_JSON="$CLAUDE_DIR/settings.json"

if [ ! -f "$SETTINGS_JSON" ]; then
  cp "$REPO_DIR/settings.json" "$SETTINGS_JSON"
else
  python3 - <<PYEOF
import json

repo_path = "$REPO_DIR/settings.json"
target_path = "$SETTINGS_JSON"

with open(repo_path) as f:
    repo = json.load(f)
with open(target_path) as f:
    target = json.load(f)

# enabledPlugins 머지 (기존 값 보존, 새 항목 추가)
target.setdefault("enabledPlugins", {}).update(repo.get("enabledPlugins", {}))

# extraKnownMarketplaces 머지
target.setdefault("extraKnownMarketplaces", {}).update(
    repo.get("extraKnownMarketplaces", {})
)

with open(target_path, "w") as f:
    json.dump(target, f, indent=2)
print("      merged: $SETTINGS_JSON")
PYEOF
fi
echo "      완료"

# 4. 마켓플레이스 플러그인 설치 (claude CLI 필요)
echo "[4/4] 마켓플레이스 플러그인 설치 중..."
if command -v claude &> /dev/null; then
  PLUGINS=("code-review" "code-simplifier" "skill-creator" "hookify")
  for plugin in "${PLUGINS[@]}"; do
    echo "      설치: $plugin"
    claude plugins install "${plugin}@claude-plugins-official" --yes 2>/dev/null || \
      echo "      (이미 설치됨 또는 스킵: $plugin)"
  done
else
  echo "      ⚠️  claude CLI를 찾을 수 없습니다."
  echo "         Claude Code 설치 후 아래 명령어를 수동으로 실행하세요:"
  echo "         claude plugins install code-review@claude-plugins-official"
  echo "         claude plugins install code-simplifier@claude-plugins-official"
  echo "         claude plugins install skill-creator@claude-plugins-official"
  echo "         claude plugins install hookify@claude-plugins-official"
fi

echo ""
echo "=== 완료! ==="
echo "Claude Code를 재시작하거나 /reload-plugins 를 실행하세요."
