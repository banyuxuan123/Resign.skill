#!/bin/bash
# Lark Handover Skill 安装脚本
# 适用于 macOS/Linux

set -e

echo "🚀 开始安装 Lark Handover Skill..."

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装 Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python 版本过低，需要 3.8+，当前 $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python 版本检查通过: $PYTHON_VERSION"

# 检查并安装 lark-cli
echo "📦 检查 lark-cli..."
if ! command -v lark-cli &> /dev/null; then
    echo "   安装 lark-cli..."
    pip3 install lark-cli
else
    echo "✅ lark-cli 已安装"
fi

# 创建 Skill 目录
SKILL_DIR="$HOME/.qwen/skills/lark-handover"
echo "📁 创建 Skill 目录: $SKILL_DIR"

mkdir -p "$SKILL_DIR"

# 复制文件
echo "📂 复制文件..."
cp -r skills/ "$SKILL_DIR/"
cp -r scripts/ "$SKILL_DIR/"
cp -r references/ "$SKILL_DIR/"
cp SKILL.md "$SKILL_DIR/"
cp README.md "$SKILL_DIR/"
cp LICENSE "$SKILL_DIR/"
cp pyproject.toml "$SKILL_DIR/"

# 设置权限
echo "🔧 设置权限..."
chmod +x "$SKILL_DIR/scripts/generate_handover.py"

# 创建命令别名
echo "🔗 创建命令..."
SHELL_RC=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
fi

if [ -n "$SHELL_RC" ]; then
    ALIAS_LINE="alias lark-handover='python3 $SKILL_DIR/scripts/generate_handover.py'"
    if ! grep -q "alias lark-handover" "$SHELL_RC"; then
        echo "" >> "$SHELL_RC"
        echo "# Lark Handover Skill" >> "$SHELL_RC"
        echo "$ALIAS_LINE" >> "$SHELL_RC"
        echo "✅ 已添加命令别名到 $SHELL_RC"
    fi
fi

echo ""
echo "✨ 安装完成！"
echo ""
echo "📋 下一步："
echo "   1. 运行: lark-cli auth login --no-wait --domain all"
echo "   2. 完成飞书授权"
echo "   3. 运行: lark-handover --user 你的姓名"
echo ""
echo "📖 查看文档: cat $SKILL_DIR/README.md"
echo ""
