#!/usr/bin/env bash
# 生成国内可访问的临时公网链接（cpolar 免费隧道）
# 用法：./share.sh <cpolar-authtoken>
# 先在 https://www.cpolar.com/ 免费注册，登录后在「验证」页复制 authtoken
set -euo pipefail
cd "$(dirname "$0")"

PORT="${PORT:-4173}"
TOKEN="${1:-${CPOLAR_TOKEN:-}}"

if [ -z "$TOKEN" ]; then
  cat <<'MSG'
缺少 cpolar authtoken。

1. 打开 https://www.cpolar.com/ 免费注册并登录
2. 进入「验证」页面，复制 authtoken
3. 运行：./share.sh <你的 authtoken>

脚本会自动启动本地预览服务（端口 4173）并输出一个 https://*.cpolar.cn 链接。
MSG
  exit 1
fi

# 1) 本地预览服务
if ! curl -fsS "http://127.0.0.1:${PORT}/" >/dev/null 2>&1; then
  echo "启动本地预览服务 0.0.0.0:${PORT} ..."
  python3 -m http.server "$PORT" --bind 0.0.0.0 >/tmp/game-qa-server.log 2>&1 &
  echo $! > /tmp/game-qa-server.pid
  sleep 1
fi

# 2) cpolar 客户端
ARCH="arm64"
[ "$(uname -m)" = "x86_64" ] && ARCH="amd64"
BIN=".cache/cpolar"
if [ ! -x "$BIN" ]; then
  mkdir -p .cache
  echo "下载 cpolar 客户端 ..."
  curl -fL --retry 2 -o .cache/cpolar.zip \
    "https://www.cpolar.com/static/downloads/releases/3.3.12/cpolar-stable-darwin-${ARCH}.zip"
  unzip -oq .cache/cpolar.zip -d .cache
  chmod +x "$BIN"
fi

# 3) 绑定 token 并开隧道
"$BIN" authtoken "$TOKEN"
exec "$BIN" http "$PORT"
