"""
Lark Handover Skill - 飞书离职交接文档生成器

自动抓取飞书文档，分类整理，生成专业的离职交接清单。
同时提供离职话术生成功能。
"""

__version__ = "1.1.0"
__author__ = "Your Name"
__description__ = "飞书离职交接文档自动生成 Skill"

from .handover import HandoverGenerator
from .config import Config
from .resignation_speech import (
    ResignationSpeechGenerator,
    BossProfile,
    ResignationReason,
    generate_resignation_speech
)

__all__ = [
    'HandoverGenerator', 
    'Config',
    'ResignationSpeechGenerator',
    'BossProfile',
    'ResignationReason',
    'generate_resignation_speech'
]
