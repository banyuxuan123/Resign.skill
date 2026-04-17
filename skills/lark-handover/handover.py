"""核心交接文档生成逻辑"""

import os
import re
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from collections import defaultdict

from .config import config


class Document:
    """文档对象"""
    
    def __init__(self, data: Dict[str, Any]):
        self.entity_type = data.get("entity_type", "")
        self.title = data.get("title_highlighted", "")
        self.url = data.get("result_meta", {}).get("url", "")
        self.create_time = data.get("result_meta", {}).get("create_time_iso", "")
        self.update_time = data.get("result_meta", {}).get("update_time_iso", "")
        self.owner_name = data.get("result_meta", {}).get("owner_name", "")
        self.edit_user_name = data.get("result_meta", {}).get("edit_user_name", "")
        self.token = data.get("result_meta", {}).get("token", "")
        
        # 自动判断重要程度和分类
        self.importance = config.determine_importance(self.title)
        self.category = config.determine_category(self.title)
        self.doc_type = config.get_doc_type_name(self.entity_type)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "title": self.title,
            "type": self.doc_type,
            "entity_type": self.entity_type,
            "category": self.category,
            "importance": self.importance,
            "create_time": self.create_time,
            "update_time": self.update_time,
            "owner": self.owner_name,
            "editor": self.edit_user_name,
            "url": self.url,
            "token": self.token
        }


class HandoverGenerator:
    """离职交接文档生成器"""
    
    def __init__(self, user_name: str, user_email: str = ""):
        """
        初始化生成器
        
        Args:
            user_name: 交接人姓名
            user_email: 交接人邮箱
        """
        self.user_name = user_name
        self.user_email = user_email
        self.documents: List[Document] = []
        self.created_docs: List[Document] = []
        self.collaborated_docs: List[Document] = []
        
    def add_documents(self, docs_data: List[Dict[str, Any]]):
        """
        添加文档数据
        
        Args:
            docs_data: 原始文档数据列表
        """
        for doc_data in docs_data:
            doc = Document(doc_data)
            self.documents.append(doc)
            
            # 分类：我创建的 vs 我协作的
            if doc.owner_name == self.user_name:
                self.created_docs.append(doc)
            elif doc.edit_user_name == self.user_name:
                self.collaborated_docs.append(doc)
    
    def categorize_by_type(self) -> Dict[str, List[Document]]:
        """按类型分类"""
        categories = defaultdict(list)
        for doc in self.created_docs:
            categories[doc.doc_type].append(doc)
        return dict(categories)
    
    def categorize_by_theme(self) -> Dict[str, List[Document]]:
        """按主题分类"""
        themes = defaultdict(list)
        for doc in self.created_docs:
            themes[doc.category].append(doc)
        return dict(themes)
    
    def categorize_by_importance(self) -> Dict[str, List[Document]]:
        """按重要程度分类"""
        levels = defaultdict(list)
        for doc in self.created_docs:
            levels[doc.importance].append(doc)
        return dict(levels)
    
    def generate_markdown(self) -> str:
        """生成 Markdown 格式的交接文档"""
        
        # 统计信息
        type_stats = self.categorize_by_type()
        theme_stats = self.categorize_by_theme()
        importance_stats = self.categorize_by_importance()
        
        md = f"""# {self.user_name} - 飞书云文档交接清单

> **交接人**：{self.user_name}  
> **邮箱**：{self.user_email}  
> **文档总数**：{len(self.documents)} 篇  
> **创建文档**：{len(self.created_docs)} 篇  
> **协作文档**：{len(self.collaborated_docs)} 篇  
> **生成日期**：{datetime.now().strftime('%Y年%m月%d日')}  

---

## 一、文档资产清单

### 1.1 我创建的云文档（{len(self.created_docs)} 篇）

| 序号 | 文档名称 | 类型 | 分类 | 重要度 | 创建时间 | 文档链接 |
|------|---------|------|------|--------|---------|---------|
"""
        
        for i, doc in enumerate(self.created_docs, 1):
            create_date = doc.create_time[:10] if doc.create_time else "未知"
            md += f"| {i} | {doc.title} | {doc.doc_type} | {doc.category} | {doc.importance} | {create_date} | [查看]({doc.url}) |\n"
        
        md += f"""

### 1.2 我参与协作的文档（{len(self.collaborated_docs)} 篇）

| 序号 | 文档名称 | 类型 | 所有者 | 我的角色 | 文档链接 |
|------|---------|------|--------|---------|---------|
"""
        
        for i, doc in enumerate(self.collaborated_docs, 1):
            role = "编辑者" if doc.edit_user_name == self.user_name else "协作者"
            md += f"| {i} | {doc.title} | {doc.doc_type} | {doc.owner_name} | {role} | [查看]({doc.url}) |\n"
        
        md += """

---

## 二、文档分类汇总

### 2.1 按类型分类

| 类型 | 数量 | 占比 |
|------|------|------|
"""
        
        for doc_type, docs in sorted(type_stats.items(), key=lambda x: len(x[1]), reverse=True):
            percentage = len(docs) / len(self.created_docs) * 100 if self.created_docs else 0
            md += f"| {doc_type} | {len(docs)} | {percentage:.1f}% |\n"
        
        md += """

### 2.2 按主题分类

| 主题 | 数量 | 说明 |
|------|------|------|
"""
        
        for theme, docs in sorted(theme_stats.items(), key=lambda x: len(x[1]), reverse=True):
            md += f"| {theme} | {len(docs)} | 包含相关主题文档 |\n"
        
        md += """

### 2.3 按重要程度分类

| 级别 | 数量 | 说明 |
|------|------|------|
"""
        
        importance_order = ["⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐", "⭐"]
        for level in importance_order:
            docs = importance_stats.get(level, [])
            if level == "⭐⭐⭐⭐":
                desc = "核心文档，必须重点交接"
            elif level == "⭐⭐⭐":
                desc = "重要文档，建议详细说明"
            elif level == "⭐⭐":
                desc = "一般文档，简要交接"
            else:
                desc = "参考文档，可备份后清理"
            md += f"| {level} | {len(docs)} | {desc} |\n"
        
        md += """

---

## 三、关键文档说明

"""
        
        # 为核心文档添加详细说明
        for level in ["⭐⭐⭐⭐", "⭐⭐⭐"]:
            docs = importance_stats.get(level, [])
            if docs:
                md += f"### {level} 级别文档\n\n"
                for doc in docs[:5]:  # 每级别最多显示5个
                    md += f"""**{doc.title}**
- 类型：{doc.doc_type}
- 分类：{doc.category}
- 链接：[查看]({doc.url})
- 交接说明：___________________________

"""
        
        md += """---

## 四、账号权限交接

### 4.1 文档所有权

| 权限类型 | 数量 | 说明 |
|---------|------|------|
| 文档创建者 | """ + str(len(self.created_docs)) + """ | 拥有完全控制权限 |
| 协作文档 | """ + str(len(self.collaborated_docs)) + """ | 拥有编辑权限 |

### 4.2 建议权限变更

| 文档/知识库 | 当前权限 | 建议操作 |
|------------|---------|---------|
"""
        
        for doc in self.created_docs[:10]:  # 显示前10个
            md += f"| {doc.title} | 所有者 | 转移给接手人 |\n"
        
        md += """

---

## 五、待办事项

### 5.1 文档权限转移（离职前完成）

| 序号 | 事项 | 优先级 | 状态 |
|------|------|--------|------|
| 1 | 转移核心文档所有权 | P0 | ☐ 待完成 |
| 2 | 备份个人知识库 | P0 | ☐ 待完成 |
| 3 | 移交重要项目文档 | P1 | ☐ 待完成 |
| 4 | 清理个人无关文档 | P2 | ☐ 待完成 |

### 5.2 知识传承

| 序号 | 事项 | 说明 | 优先级 |
|------|------|------|--------|
| 1 | 核心文档讲解 | 向接手人说明核心文档内容和使用方法 | P0 |
| 2 | 项目背景交接 | 说明项目历史和当前状态 | P1 |
| 3 | 工具使用培训 | 讲解相关工具和系统使用方法 | P1 |

---

## 六、文档备份建议

### 6.1 建议备份的文档

以下文档建议导出本地备份：

"""
        
        for doc in self.created_docs[:15]:
            md += f"- [ ] **{doc.title}** - {doc.doc_type}\n"
        
        md += """

### 6.2 备份方法

```
飞书文档 → 更多 → 导出为 Markdown/PDF
```

---

## 七、交接确认

| 类别 | 项目 | 是否已交接 | 备注 |
|------|------|-----------|------|
| 文档资产 | 云文档 | ☐ 是 ☐ 否 | |
| 文档资产 | 知识库 | ☐ 是 ☐ 否 | |
| 权限账号 | 文档所有权 | ☐ 是 ☐ 否 | |
| 工作事项 | 核心文档说明 | ☐ 是 ☐ 否 | |
| 工作事项 | 项目知识库 | ☐ 是 ☐ 否 | |

### 三方签字确认

| 角色 | 姓名 | 签字 | 日期 |
|------|------|------|------|
| 交接人 | """ + self.user_name + """ | | |
| 接手人 | | | |
| 直属上级 | | | |

---

> 📅 文档生成时间：""" + datetime.now().strftime('%Y年%m月%d日 %H:%M') + """  
> 🤖 生成工具：Lark Handover Skill  
> 👤 交接人：""" + self.user_name + """
"""
        
        return md
    
    def save_markdown(self, output_path: str):
        """保存 Markdown 文件"""
        md_content = self.generate_markdown()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        return output_path
    
    def to_json(self) -> str:
        """导出为 JSON 格式"""
        data = {
            "user_name": self.user_name,
            "user_email": self.user_email,
            "generated_at": datetime.now().isoformat(),
            "statistics": {
                "total_docs": len(self.documents),
                "created_docs": len(self.created_docs),
                "collaborated_docs": len(self.collaborated_docs),
                "by_type": {k: len(v) for k, v in self.categorize_by_type().items()},
                "by_theme": {k: len(v) for k, v in self.categorize_by_theme().items()},
                "by_importance": {k: len(v) for k, v in self.categorize_by_importance().items()}
            },
            "documents": [doc.to_dict() for doc in self.documents]
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
