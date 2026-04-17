"""配置文件管理"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional


class Config:
    """飞书交接 Skill 配置类"""
    
    # 默认配置
    DEFAULT_CONFIG = {
        "doc_types": {
            "DOC": "云文档",
            "DOCX": "云文档",
            "WIKI": "知识库",
            "SHEET": "电子表格",
            "BITABLE": "多维表格",
            "FILE": "文件"
        },
        "importance_keywords": {
            "⭐⭐⭐⭐": ["核心", "中枢", "关键", "重要", "主", "核心工作"],
            "⭐⭐⭐": ["GEO", "AI", "项目", "手册", "报告", "设计"],
            "⭐⭐": ["调研", "方案", "预算", "清单", "playbook"],
            "⭐": ["参考", "备份", "临时", "草稿"]
        },
        "category_mapping": {
            "GEO": ["GEO", "AI", "技能", "智能体", "agent"],
            "运营": ["运营", "营销", "market", "operation"],
            "项目": ["项目", "project", "心灵彩虹", "omada"],
            "技术": ["技术", "工具", "skill", "代码", "开发"],
            "调研": ["调研", "调研报告", "分析", "research"],
            "个人": ["个人", "我的", "私", "个人知识库"]
        },
        "output_template": {
            "title": "{name}-云文档交接清单",
            "sections": [
                "文档资产清单",
                "参与协作文档",
                "文档分类汇总",
                "关键文档说明",
                "账号权限交接",
                "待办事项",
                "文档备份建议",
                "交接确认"
            ]
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置
        
        Args:
            config_path: 配置文件路径，默认使用内置配置
        """
        self.config = self.DEFAULT_CONFIG.copy()
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                self.config.update(user_config)
    
    def get(self, key: str, default=None):
        """获取配置项"""
        return self.config.get(key, default)
    
    def get_doc_type_name(self, doc_type: str) -> str:
        """获取文档类型中文名"""
        return self.config["doc_types"].get(doc_type.upper(), "其他")
    
    def determine_importance(self, title: str) -> str:
        """
        根据标题判断重要程度
        
        Args:
            title: 文档标题
            
        Returns:
            重要程度星级
        """
        title_lower = title.lower()
        
        for level, keywords in self.config["importance_keywords"].items():
            for keyword in keywords:
                if keyword.lower() in title_lower:
                    return level
        
        return "⭐"
    
    def determine_category(self, title: str) -> str:
        """
        根据标题判断文档分类
        
        Args:
            title: 文档标题
            
        Returns:
            分类名称
        """
        title_lower = title.lower()
        
        for category, keywords in self.config["category_mapping"].items():
            for keyword in keywords:
                if keyword.lower() in title_lower:
                    return category
        
        return "其他"
    
    def save(self, path: str):
        """保存配置到文件"""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)


# 全局配置实例
config = Config()
