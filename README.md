# 🚀 离职.Skill

<p align="center">
  <strong>飞书离职交接文档+离职话术自动生成器</strong>
</p>

<p align="center">
  <a href="#快速开始">快速开始</a> •
  <a href="#功能特性">功能特性</a> •
  <a href="#使用文档">使用文档</a> •
  <a href="#作为claude-code-skill使用">Claude Code 集成</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/platform-Feishu-blue.svg" alt="Feishu">
</p>

---

## ✨ 功能特性

### 📁 文档交接功能

- 🔍 **自动抓取** - 通过飞书 API 自动获取文档数据
- 📊 **智能分类** - 按类型、主题、重要程度自动分类整理
- 📝 **一键生成** - 自动生成专业的 Markdown 交接文档
- ☁️ **自动上传** - 直接上传到飞书云文档，便于分享和协作
- 🎯 **重要度评估** - 根据关键词智能判断文档重要性

### 💬 离职话术功能

- 🧠 **MBTI 智能匹配** - 根据老板 MBTI 类型定制个性化话术
- 👤 **多维度分析** - 考虑年龄、性别、性格、沟通风格
- 💭 **多版本话术** - 正式版、轻松版、简短版、微信版
- 📋 **面谈 Q&A** - 提供离职面谈常见问题应对指南
- 🎭 **关系适配** - 根据关系亲疏调整语气和策略
- 🔧 **高度可配置** - 支持自定义分类规则和关键词

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装飞书 CLI
pip install lark-cli

# 克隆本项目
git clone https://github.com/yourname/lark-handover-skill.git
cd lark-handover-skill
```

### 2. 完成飞书授权

```bash
lark-cli auth login --no-wait --domain all
```

按提示在浏览器中完成授权。

### 3. 生成交接文档

```bash
python scripts/generate_handover.py --user 你的姓名
```

✅ 文档将自动生成本地文件并上传到飞书云文档！

### 4. 生成离职话术

```bash
# 交互式使用（推荐）
python scripts/generate_resignation_speech.py --interactive
```

交互式会引导你输入：
- 老板姓氏、性别、年龄段
- MBTI 类型（不知道可以选"未知"）
- 性格特征、沟通风格
- 关系亲疏
- 离职理由
- 最后工作日

然后生成 4 种版本的话术 + 面谈 Q&A 指南。

```bash
# 查看离职理由选项
python scripts/generate_resignation_speech.py --list-reasons
```

---

## 📖 使用文档

### 命令行参数

```bash
python scripts/generate_handover.py --help
```

| 参数 | 说明 | 示例 |
|------|------|------|
| `--user, -u` | 交接人姓名（必需） | `--user 张三` |
| `--email, -e` | 交接人邮箱 | `--email zhangsan@example.com` |
| `--input, -i` | 从 JSON 文件导入 | `--input docs.json` |
| `--output, -o` | 输出文件路径 | `--output 交接清单.md` |
| `--no-upload` | 不上传到飞书 | `--no-upload` |

### 使用示例

#### 基础用法

```bash
python scripts/generate_handover.py --user 张三
```

#### 离线模式（从 JSON 导入）

```bash
# 先导出数据
lark-cli docs +search --format json > docs.json

# 然后离线生成
python scripts/generate_handover.py --user 张三 --input docs.json
```

#### 只生成本地文件

```bash
python scripts/generate_handover.py --user 张三 --no-upload
```

---

## 🧩 作为 Claude Code / Qwen Code Skill 使用

### 安装

```bash
# 复制到 skills 目录
cp -r lark-handover-skill ~/.qwen/skills/

# 或 Windows
xcopy /E /I lark-handover-skill %USERPROFILE%\.qwen\skills\lark-handover
```

### 使用

在 Claude Code / Qwen Code 对话中：

```
用户：帮我生成交接文档

Claude：我来帮你使用 Lark Handover Skill 生成交接文档。

首先，请确认：
1. 你已完成飞书授权（lark-cli auth login）
2. 提供你的姓名用于生成文档

请告诉我你的姓名，我将立即为你生成交接文档。
```

---

## 📁 生成的文档结构

生成的交接文档包含以下内容：

```
📄 交接清单.md
├── 文档资产清单
│   ├── 我创建的云文档（表格）
│   └── 我参与协作的文档
├── 文档分类汇总
│   ├── 按类型分类
│   ├── 按主题分类
│   └── 按重要程度分类
├── 关键文档说明
│   └── 核心文档详细说明
├── 账号权限交接
├── 待办事项
├── 文档备份建议
└── 交接确认（签字栏）
```

---

## ⚙️ 自定义配置

创建 `config.json` 自定义分类规则：

```json
{
  "importance_keywords": {
    "⭐⭐⭐⭐": ["核心", "关键", "主"],
    "⭐⭐⭐": ["重要", "GEO", "AI"],
    "⭐⭐": ["调研", "方案"],
    "⭐": ["参考", "备份"]
  },
  "category_mapping": {
    "核心工作": ["核心", "主"],
    "技术研究": ["GEO", "AI", "技术"],
    "项目管理": ["项目", "管理"]
  }
}
```

---

## 🏗️ 项目结构

```
lark-handover-skill/
├── skills/
│   └── lark-handover/
│       ├── __init__.py       # 模块入口
│       ├── handover.py       # 核心生成逻辑
│       ├── config.py         # 配置管理
│       └── cli.py            # 命令行接口
├── scripts/
│   └── generate_handover.py  # 一键生成脚本
├── references/               # 参考文档
├── SKILL.md                  # Skill 详细文档
├── README.md                 # 项目说明
└── pyproject.toml            # Python 项目配置
```

---

## 🛠️ Python API

```python
from skills.lark_handover import HandoverGenerator

# 创建生成器
generator = HandoverGenerator(
    user_name="张三",
    user_email="zhangsan@example.com"
)

# 添加文档数据
generator.add_documents(docs_data)

# 生成交接文档
generator.save_markdown("交接清单.md")

# 导出 JSON
json_data = generator.to_json()
```

---

## 📊 智能分类

### 自动识别的文档类型

- 📄 云文档 (DOC/DOCX)
- 📚 知识库 (WIKI)
- 📊 电子表格 (SHEET)
- 📋 多维表格 (BITABLE)
- 📎 文件 (FILE)

### 自动判断的重要程度

| 级别 | 关键词 | 颜色 |
|------|--------|------|
| ⭐⭐⭐⭐ | 核心、关键、中枢、主 | 🔴 核心 |
| ⭐⭐⭐ | GEO、AI、项目、手册 | 🟠 重要 |
| ⭐⭐ | 调研、方案、预算 | 🟡 一般 |
| ⭐ | 参考、备份、草稿 | ⚪ 参考 |

---

## ❓ 常见问题

### Q1: 如何获取飞书授权？

```bash
lark-cli auth login --no-wait --domain all
```

按提示在浏览器中完成授权。

### Q2: 可以离线使用吗？

可以！先用 lark-cli 导出 JSON，然后离线生成：

```bash
# 导出
lark-cli docs +search --format json > docs.json

# 离线生成
python scripts/generate_handover.py --user 张三 --input docs.json
```

### Q3: 支持哪些飞书文档类型？

支持云文档、知识库、电子表格、多维表格、文件等所有飞书文档类型。

### Q4: 生成的文档可以编辑吗？

可以！生成的是标准 Markdown 格式，可以用任何编辑器修改。

### Q5: 如何自定义分类规则？

创建 `config.json` 文件，修改 `importance_keywords` 和 `category_mapping`。详见 [SKILL.md](SKILL.md)。

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

### 开发环境

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
python -m pytest tests/

# 代码格式化
black skills/ scripts/
```

---

## 📄 许可证

[MIT License](LICENSE)

---

## 🔗 相关链接

- [飞书开放平台](https://open.feishu.cn/)
- [lark-cli 文档](https://github.com/larksuite/lark-cli)
- [Claude Code](https://claude.ai/code)

---

<p align="center">
  用 ❤️ 和 🤖 构建
</p>
