# Lark Handover Skill

> **飞书离职交接文档自动生成器**
>
> 自动抓取飞书文档，智能分类整理，一键生成专业离职交接清单

---

## 概述

Lark Handover Skill 是一个全面的离职辅助工具，包含两大核心功能：

1. **📁 文档交接清单生成** - 自动整理飞书文档，生成交接清单
2. **💬 离职话术生成** - 根据老板性格特征，生成个性化离职话术

### 核心功能

#### 文档交接功能
- 🔍 **自动抓取**：通过飞书 API 自动获取你创建和协作的文档
- 📊 **智能分类**：按类型、主题、重要程度自动分类
- 📝 **一键生成**：自动生成 Markdown 格式的交接文档
- ☁️ **自动上传**：直接上传到飞书云文档，便于分享
- 🎯 **重要度评估**：根据标题关键词智能判断文档重要性

#### 离职话术功能
- 🧠 **MBTI 匹配**：根据老板 MBTI 类型定制话术
- 👤 **性格分析**：考虑年龄、性别、沟通风格等因素
- 💭 **智能生成**：生成正式版、轻松版、简短版、微信版多种话术
- 📋 **Q&A 指南**：提供离职面谈常见问题的应对策略
- 🎭 **角色扮演**：根据关系亲疏调整语气

### 适用场景

- 离职交接 - 快速整理工作文档 + 准备离职沟通
- 项目移交 - 归档项目相关资料
- 岗位轮换 - 交接工作职责
- 定期备份 - 导出文档资产清单

---

## 使用方法

### 前置要求

1. 安装 **lark-cli**（飞书命令行工具）
2. 完成飞书授权

```bash
# 安装 lark-cli
pip install lark-cli

# 授权登录
lark-cli auth login --no-wait --domain all
# 按提示完成授权
```

### 快速使用

#### 功能一：生成交接文档

```bash
# 使用脚本一键生成并上传
python scripts/generate_handover.py --user 你的姓名

# 输出：生成本地文件 + 上传到飞书云文档
```

#### 功能二：生成离职话术

```bash
# 交互式使用（推荐）
python scripts/generate_resignation_speech.py --interactive

# 或查看离职理由选项
python scripts/generate_resignation_speech.py --list-reasons
```

交互式使用会引导你输入老板信息（MBTI、性格、年龄等），然后生成个性化话术。

### 高级用法

```bash
# 从 JSON 文件导入（离线模式）
python scripts/generate_handover.py --user 张三 --input docs.json

# 只生成本地文件，不上传
python scripts/generate_handover.py --user 张三 --no-upload

# 指定输出文件名
python scripts/generate_handover.py --user 张三 --output 我的交接清单.md

# 指定邮箱
python scripts/generate_handover.py --user 张三 --email zhangsan@example.com
```

---

## 文档结构

生成的交接文档包含以下章节：

### 1. 文档资产清单
- 我创建的云文档（表格形式，含链接）
- 我参与协作的文档

### 2. 文档分类汇总
- 按类型分类（云文档、知识库、表格等）
- 按主题分类（GEO、运营、项目、技术等）
- 按重要程度分类（⭐⭐⭐⭐ 到 ⭐）

### 3. 关键文档说明
- 核心文档详细说明
- 交接建议和后续负责人

### 4. 账号权限交接
- 文档所有权清单
- 建议权限变更

### 5. 待办事项
- 文档权限转移
- 知识传承事项

### 6. 文档备份建议
- 建议备份的文档清单
- 备份方法说明

### 7. 交接确认
- 交接清单确认表
- 三方签字栏

---

## 智能分类规则

### 文档类型识别

| 飞书类型 | 中文名 |
|---------|--------|
| DOC/DOCX | 云文档 |
| WIKI | 知识库 |
| SHEET | 电子表格 |
| BITABLE | 多维表格 |
| FILE | 文件 |

### 重要程度判断

| 级别 | 关键词 | 说明 |
|------|--------|------|
| ⭐⭐⭐⭐ | 核心、中枢、关键、重要、主 | 核心文档，必须重点交接 |
| ⭐⭐⭐ | GEO、AI、项目、手册、报告、设计 | 重要文档，建议详细说明 |
| ⭐⭐ | 调研、方案、预算、清单、playbook | 一般文档，简要交接 |
| ⭐ | 参考、备份、临时、草稿 | 参考文档，可备份后清理 |

### 主题分类

| 分类 | 关键词 |
|------|--------|
| GEO/AI | GEO、AI、技能、智能体、agent |
| 运营 | 运营、营销、market、operation |
| 项目 | 项目、project、心灵彩虹、omada |
| 技术 | 技术、工具、skill、代码、开发 |
| 调研 | 调研、调研报告、分析、research |
| 个人 | 个人、我的、私、个人知识库 |

---

## 配置文件

可通过配置文件自定义分类规则和重要度关键词。

### 配置文件示例 `config.json`

```json
{
  "doc_types": {
    "DOC": "云文档",
    "WIKI": "知识库",
    "SHEET": "电子表格"
  },
  "importance_keywords": {
    "⭐⭐⭐⭐": ["核心", "关键", "主"],
    "⭐⭐⭐": ["重要", "GEO", "AI"],
    "⭐⭐": ["调研", "方案"],
    "⭐": ["参考", "备份"]
  },
  "category_mapping": {
    "核心工作": ["核心", "主", "中枢"],
    "技术研究": ["GEO", "AI", "技术"],
    "项目管理": ["项目", "管理"]
  }
}
```

### 使用配置文件

```python
from skills.lark_handover import HandoverGenerator, Config

# 加载自定义配置
config = Config('config.json')

# 使用配置生成文档
generator = HandoverGenerator('张三')
# ... 后续操作
```

---

## Python API 使用

### 基础用法

```python
from skills.lark_handover import HandoverGenerator

# 创建生成器
generator = HandoverGenerator(
    user_name="张三",
    user_email="zhangsan@example.com"
)

# 添加文档数据
docs_data = [
    {
        "entity_type": "DOCX",
        "title_highlighted": "项目方案文档",
        "result_meta": {
            "url": "https://xxx.feishu.cn/docx/xxx",
            "create_time_iso": "2026-04-01",
            "owner_name": "张三"
        }
    },
    # ... 更多文档
]

generator.add_documents(docs_data)

# 生成 Markdown
generator.save_markdown("交接清单.md")

# 导出 JSON
json_data = generator.to_json()
```

### 获取分类统计

```python
# 按类型分类
type_stats = generator.categorize_by_type()
# {'云文档': [...], '知识库': [...]}

# 按主题分类
theme_stats = generator.categorize_by_theme()
# {'GEO/AI': [...], '运营': [...]}

# 按重要度分类
importance_stats = generator.categorize_by_importance()
# {'⭐⭐⭐⭐': [...], '⭐⭐⭐': [...]}
```

---

## 技术架构

```
lark-handover-skill/
├── skills/
│   └── lark-handover/
│       ├── __init__.py      # 模块入口
│       ├── handover.py      # 核心生成逻辑
│       ├── config.py        # 配置管理
│       └── cli.py           # 命令行接口
├── scripts/
│   └── generate_handover.py # 一键生成脚本
├── references/
│   └── usage.md            # 详细使用说明
├── config.json             # 默认配置文件
├── SKILL.md               # 本文件
├── README.md              # 项目说明
└── pyproject.toml         # Python 项目配置
```

### 核心类说明

| 类名 | 功能 |
|------|------|
| `HandoverGenerator` | 交接文档生成器，核心逻辑 |
| `Document` | 文档对象，封装单篇文档信息 |
| `Config` | 配置管理，支持自定义规则 |

---

## 与 Claude Code / Qwen Code 集成

### 作为 Skill 安装

```bash
# 复制到 skills 目录
cp -r lark-handover-skill ~/.qwen/skills/

# 重启 Claude Code / Qwen Code
```

### 在对话中使用

```
用户：帮我生成交接文档
Claude：我来帮你使用 Lark Handover Skill 生成交接文档。
      首先需要从飞书获取你的文档数据...
```

---

## 命令速查表

| 命令 | 说明 |
|------|------|
| `python scripts/generate_handover.py --user 张三` | 一键生成并上传 |
| `python -m lark_handover --user 张三 --input docs.json` | 从文件导入 |
| `python -m lark_handover --user 张三 --no-upload` | 只生成本地文件 |
| `lark-cli auth login --no-wait --domain all` | 飞书授权 |
| `lark-cli docs +search --query ""` | 搜索文档 |

---

## 常见问题

### Q1: 如何获取飞书文档数据？

A: 需要提前安装并授权 lark-cli：

```bash
pip install lark-cli
lark-cli auth login --no-wait --domain all
```

### Q2: 可以离线使用吗？

A: 可以。先用 `lark-cli` 导出文档数据为 JSON，然后离线生成：

```bash
# 导出数据
lark-cli docs +search --format json > docs.json

# 离线生成
python scripts/generate_handover.py --user 张三 --input docs.json --no-upload
```

### Q3: 如何自定义分类规则？

A: 创建 `config.json` 配置文件，修改 `importance_keywords` 和 `category_mapping`。

### Q4: 支持哪些飞书文档类型？

A: 支持云文档(DOC/DOCX)、知识库(WIKI)、电子表格(SHEET)、多维表格(BITABLE)、文件(FILE)。

### Q5: 生成的文档可以编辑吗？

A: 可以。生成的是标准 Markdown 格式，可以用任何文本编辑器修改。

---

## 离职话术生成详解

### 功能介绍

离职话术生成器根据老板的性格特征（MBTI、年龄、性别、沟通风格等）生成个性化的离职沟通话术。

### 支持的 MBTI 类型

| 类型 | 名称 | 沟通策略 |
|------|------|---------|
| ENTJ | 指挥官 | 开门见山，强调新机会成长性 |
| ENTP | 辩论家 | 以探讨方式，展现兴奋 |
| INTJ | 建筑师 | 用数据和逻辑说明职业规划 |
| INTP | 逻辑学家 | 坦诚分享思考过程 |
| ENFJ | 主人公 | 强调对团队的感激 |
| ENFP | 竞选者 | 分享对新机会的兴奋 |
| INFJ | 提倡者 | 真诚表达，说明成长思考 |
| INFP | 调停者 | 温和表达，追随内心 |
| ESTJ | 总经理 | 直接说明，强调交接计划 |
| ESFJ | 执政官 | 强调团队情谊 |
| ISTJ | 检查者 | 强调会妥善交接 |
| ISFJ | 守护者 | 表达感激，确保平稳过渡 |
| ESTP | 企业家 | 直接坦诚，展现兴奋 |
| ESFP | 表演者 | 热情分享新机会 |
| ISTP | 鉴赏家 | 简洁直接，说明技能发展 |
| ISFP | 探险家 | 温和真诚，追随价值 |

### 离职理由选项

#### 职业发展类
- `CAREER_GROWTH` - 个人职业发展规划
- `NEW_OPPORTUNITY` - 新的职业机会
- `STARTUP` - 创业
- `STUDY` - 继续深造/学习
- `INDUSTRY_CHANGE` - 行业转型

#### 个人原因类
- `FAMILY` - 家庭原因
- `HEALTH` - 健康原因
- `WORK_LIFE_BALANCE` - 工作生活平衡
- `BURNOUT` - 职业倦怠，需要休息
- `RELOCATION` - 搬家/relocate

#### 客观原因类
- `CONTRACT_END` - 合同到期
- `COMPANY_CHANGE` - 公司战略调整
- `PROJECT_END` - 项目结束

### 生成的话术版本

1. **正式版** - 适合邮件或正式场合
2. **轻松版** - 适合关系较好的老板
3. **简短版** - 紧急情况或老板时间有限
4. **微信/钉钉版** - 分段发送的消息格式

### 使用示例

```python
from skills.lark_handover import generate_resignation_speech

result = generate_resignation_speech(
    boss_name="张",
    boss_gender="男",
    boss_age="40-50",
    boss_mbti="ENTJ",
    reason_key="NEW_OPPORTUNITY",
    last_day="2026年4月30日",
    relationship="一般"
)

print(result["正式版"])
print(result["微信/钉钉版"])
print(result["_qa_guide"])  # 面谈 Q&A 指南
```

### 面谈 Q&A 指南

生成器会同时提供离职面谈常见问题的应对指南：
- "为什么突然要离职？"
- "是不是对公司/我有什么不满？"
- "有没有挽留的可能？"
- 针对不同 MBTI 老板的面谈技巧

---

## 贡献指南

欢迎提交 Issue 和 PR！

### 开发环境

```bash
# 克隆仓库
git clone https://github.com/yourname/lark-handover-skill.git
cd lark-handover-skill

# 安装依赖
pip install -e "."

# 运行测试
python -m pytest tests/
```

### 提交规范

- 使用语义化版本号
- 提交前运行代码格式化
- 更新 CHANGELOG.md

---

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 相关链接

- **GitHub**: https://github.com/yourname/lark-handover-skill
- **飞书开放平台**: https://open.feishu.cn/
- **lark-cli**: https://github.com/larksuite/lark-cli

---

> 💡 **提示**：首次使用前，请确保已完成飞书授权！
>
> 运行：`lark-cli auth login --no-wait --domain all`
