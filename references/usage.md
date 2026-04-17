# 详细使用说明

## 目录

- [快速开始](#快速开始)
- [进阶配置](#进阶配置)
- [常见问题](#常见问题)
- [故障排除](#故障排除)

---

## 快速开始

### 1. 环境准备

确保你的系统满足以下要求：

- Python 3.8 或更高版本
- 飞书账号（有文档访问权限）
- 网络连接（用于飞书 API 调用）

### 2. 安装步骤

#### 安装 lark-cli

```bash
pip install lark-cli
```

验证安装：

```bash
lark-cli --version
```

#### 下载本 Skill

```bash
git clone https://github.com/yourname/lark-handover-skill.git
cd lark-handover-skill
```

或下载 ZIP 解压。

### 3. 飞书授权

这是最关键的一步！

```bash
lark-cli auth login --no-wait --domain all
```

执行后会显示：

```
{"device_code":"xxxxx","verification_url":"https://accounts.feishu.cn/...","user_code":"ABCD-EFGH"}
```

**操作步骤**：

1. 复制 `verification_url` 链接
2. 在浏览器中打开
3. 登录你的飞书账号
4. 输入 `user_code`（如 ABCD-EFGH）
5. 确认授权

### 4. 生成交接文档

```bash
python scripts/generate_handover.py --user 你的姓名
```

等待片刻，文档将自动生成并上传到飞书。

---

## 进阶配置

### 自定义重要度关键词

编辑 `config.json`：

```json
{
  "importance_keywords": {
    "⭐⭐⭐⭐": ["核心", "关键", "中枢", "主"],
    "⭐⭐⭐": ["重要", "GEO", "AI", "项目", "手册"],
    "⭐⭐": ["调研", "方案", "预算", "清单"],
    "⭐": ["参考", "备份", "临时", "草稿"]
  }
}
```

### 自定义主题分类

```json
{
  "category_mapping": {
    "核心工作": ["核心", "主", "中枢"],
    "技术研究": ["GEO", "AI", "技术", "算法"],
    "项目管理": ["项目", "管理", "计划"],
    "运营营销": ["运营", "营销", "推广", "市场"],
    "人力资源": ["人事", "招聘", "培训", "绩效"],
    "财务管理": ["财务", "预算", "报销", "发票"]
  }
}
```

### 使用自定义配置

```bash
python scripts/generate_handover.py --user 张三 --config my-config.json
```

---

## 常见问题

### Q1: 授权时提示 "device code expired"

**原因**：授权链接已过期（有效期2分钟）

**解决**：重新运行授权命令：

```bash
lark-cli auth login --no-wait --domain all
```

### Q2: 提示 "Permission denied" 或权限不足

**原因**：飞书应用没有足够权限

**解决**：
1. 确认你是文档的所有者或协作者
2. 联系飞书管理员开通相关权限
3. 确保授权时选择了正确的权限范围

### Q3: 生成的文档中文乱码

**原因**：编码问题

**解决**：确保使用 UTF-8 编码：

```python
# 在 Python 脚本开头添加
# -*- coding: utf-8 -*-
```

### Q4: 文档数量显示为 0

**原因**：
1. 未正确授权
2. 飞书账号下确实没有文档
3. API 调用失败

**排查步骤**：

```bash
# 检查授权状态
lark-cli auth status

# 手动搜索文档测试
lark-cli docs +search --query "" --page-size 10
```

### Q5: 如何导出所有文档（超过100篇）

**方法**：分页导出

```bash
# 第1页
lark-cli docs +search --query "" --page-size 100 --page-token "" > docs_page1.json

# 第2页（使用上一页的 page_token）
lark-cli docs +search --query "" --page-size 100 --page-token "xxx" > docs_page2.json

# 合并后再生成
python scripts/merge_json.py docs_page*.json > all_docs.json
python scripts/generate_handover.py --user 张三 --input all_docs.json
```

---

## 故障排除

### 问题：脚本运行报错 "ModuleNotFoundError"

**解决**：

```bash
# 确保在项目根目录
pip install -e "."

# 或使用 Python 路径
PYTHONPATH=. python scripts/generate_handover.py --user 张三
```

### 问题：上传到飞书失败

**解决**：

1. 检查网络连接
2. 确认授权未过期：`lark-cli auth status`
3. 使用 `--no-upload` 参数只生成本地文件
4. 手动上传到飞书

### 问题：生成的 Markdown 格式错乱

**解决**：

1. 检查文档标题是否包含特殊字符
2. 使用 `--output` 指定纯英文文件名
3. 在支持的 Markdown 编辑器中打开

---

## 最佳实践

### 1. 定期备份

建议每月运行一次，备份文档清单：

```bash
# 添加到 cron（Linux/Mac）
0 9 1 * * cd /path/to/lark-handover-skill && python scripts/generate_handover.py --user 张三 --no-upload --output 备份-$(date +%Y%m).md
```

### 2. 分类整理

在生成前，建议先整理飞书文档：
- 删除临时/无用文档
- 归档已完成的项目文档
- 确保重要文档命名规范

### 3. 交接前准备

离职前一周：

1. 运行脚本生成交接文档
2. 与接手人确认文档清单
3. 补充文档说明和交接备注
4. 安排知识传承会议

---

## 更多帮助

- 查看 [SKILL.md](../SKILL.md) 了解完整功能
- 提交 [Issue](https://github.com/yourname/lark-handover-skill/issues) 反馈问题
- 阅读 [README.md](../README.md) 获取项目概览
