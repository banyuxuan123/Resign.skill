"""测试用例"""

import json
import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from skills.lark_handover.handover import HandoverGenerator, Document
from skills.lark_handover.config import Config


class TestConfig:
    """测试配置类"""
    
    def test_default_config(self):
        """测试默认配置"""
        config = Config()
        assert config.get("doc_types") is not None
        assert config.get("importance_keywords") is not None
        assert config.get("category_mapping") is not None
    
    def test_get_doc_type_name(self):
        """测试获取文档类型名"""
        config = Config()
        assert config.get_doc_type_name("DOC") == "云文档"
        assert config.get_doc_type_name("WIKI") == "知识库"
        assert config.get_doc_type_name("UNKNOWN") == "其他"
    
    def test_determine_importance(self):
        """测试重要度判断"""
        config = Config()
        assert config.determine_importance("核心项目文档") == "⭐⭐⭐⭐"
        assert config.determine_importance("GEO调研报告") == "⭐⭐⭐"
        assert config.determine_importance("参考备份") == "⭐"
        assert config.determine_importance("普通文档") == "⭐"
    
    def test_determine_category(self):
        """测试分类判断"""
        config = Config()
        assert config.determine_category("GEO技能设计") == "GEO/AI"
        assert config.determine_category("运营方案") == "运营营销"
        assert config.determine_category("个人笔记") == "个人管理"
        assert config.determine_category("普通文档") == "其他"


class TestDocument:
    """测试文档类"""
    
    def test_document_creation(self):
        """测试文档创建"""
        data = {
            "entity_type": "DOCX",
            "title_highlighted": "测试文档",
            "result_meta": {
                "url": "https://example.com/doc",
                "create_time_iso": "2026-04-01T10:00:00+08:00",
                "update_time_iso": "2026-04-02T10:00:00+08:00",
                "owner_name": "张三",
                "edit_user_name": "张三"
            }
        }
        
        doc = Document(data)
        assert doc.title == "测试文档"
        assert doc.entity_type == "DOCX"
        assert doc.doc_type == "云文档"
        assert doc.owner_name == "张三"
        assert doc.url == "https://example.com/doc"
    
    def test_document_to_dict(self):
        """测试文档转字典"""
        data = {
            "entity_type": "WIKI",
            "title_highlighted": "知识库文档",
            "result_meta": {
                "url": "https://example.com/wiki",
                "create_time_iso": "2026-04-01T10:00:00+08:00",
                "update_time_iso": "2026-04-02T10:00:00+08:00",
                "owner_name": "张三",
                "edit_user_name": "李四"
            }
        }
        
        doc = Document(data)
        doc_dict = doc.to_dict()
        
        assert doc_dict["title"] == "知识库文档"
        assert doc_dict["type"] == "知识库"
        assert "url" in doc_dict
        assert "importance" in doc_dict
        assert "category" in doc_dict


class TestHandoverGenerator:
    """测试生成器类"""
    
    @pytest.fixture
    def sample_docs(self):
        """示例文档数据"""
        return [
            {
                "entity_type": "DOCX",
                "title_highlighted": "核心项目文档",
                "result_meta": {
                    "url": "https://example.com/1",
                    "create_time_iso": "2026-04-01T10:00:00+08:00",
                    "owner_name": "张三",
                    "edit_user_name": "张三"
                }
            },
            {
                "entity_type": "WIKI",
                "title_highlighted": "GEO调研报告",
                "result_meta": {
                    "url": "https://example.com/2",
                    "create_time_iso": "2026-04-02T10:00:00+08:00",
                    "owner_name": "张三",
                    "edit_user_name": "张三"
                }
            },
            {
                "entity_type": "BITABLE",
                "title_highlighted": "协作表格",
                "result_meta": {
                    "url": "https://example.com/3",
                    "create_time_iso": "2026-04-03T10:00:00+08:00",
                    "owner_name": "李四",
                    "edit_user_name": "张三"
                }
            }
        ]
    
    def test_generator_creation(self):
        """测试生成器创建"""
        generator = HandoverGenerator("张三", "zhangsan@example.com")
        assert generator.user_name == "张三"
        assert generator.user_email == "zhangsan@example.com"
        assert len(generator.documents) == 0
    
    def test_add_documents(self, sample_docs):
        """测试添加文档"""
        generator = HandoverGenerator("张三")
        generator.add_documents(sample_docs)
        
        assert len(generator.documents) == 3
        assert len(generator.created_docs) == 2  # 张三创建的
        assert len(generator.collaborated_docs) == 1  # 张三协作的
    
    def test_categorize_by_type(self, sample_docs):
        """测试按类型分类"""
        generator = HandoverGenerator("张三")
        generator.add_documents(sample_docs)
        
        type_stats = generator.categorize_by_type()
        assert "云文档" in type_stats
        assert "知识库" in type_stats
        assert len(type_stats["云文档"]) == 1
        assert len(type_stats["知识库"]) == 1
    
    def test_categorize_by_theme(self, sample_docs):
        """测试按主题分类"""
        generator = HandoverGenerator("张三")
        generator.add_documents(sample_docs)
        
        theme_stats = generator.categorize_by_theme()
        assert "GEO/AI" in theme_stats
        assert len(theme_stats["GEO/AI"]) == 1
    
    def test_generate_markdown(self, sample_docs, tmp_path):
        """测试生成 Markdown"""
        generator = HandoverGenerator("张三")
        generator.add_documents(sample_docs)
        
        md_content = generator.generate_markdown()
        
        assert "张三 - 飞书云文档交接清单" in md_content
        assert "核心项目文档" in md_content
        assert "GEO调研报告" in md_content
        assert "文档资产清单" in md_content
        assert "| 序号 |" in md_content  # 表格格式
    
    def test_save_markdown(self, sample_docs, tmp_path):
        """测试保存 Markdown"""
        generator = HandoverGenerator("张三")
        generator.add_documents(sample_docs)
        
        output_path = tmp_path / "test_output.md"
        generator.save_markdown(str(output_path))
        
        assert output_path.exists()
        content = output_path.read_text(encoding='utf-8')
        assert "张三" in content
    
    def test_to_json(self, sample_docs):
        """测试导出 JSON"""
        generator = HandoverGenerator("张三", "zhangsan@example.com")
        generator.add_documents(sample_docs)
        
        json_str = generator.to_json()
        data = json.loads(json_str)
        
        assert data["user_name"] == "张三"
        assert data["user_email"] == "zhangsan@example.com"
        assert data["statistics"]["total_docs"] == 3
        assert len(data["documents"]) == 3


class TestIntegration:
    """集成测试"""
    
    def test_full_workflow(self, tmp_path):
        """测试完整工作流"""
        # 1. 加载示例数据
        sample_file = Path(__file__).parent / "sample_docs.json"
        with open(sample_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 2. 创建生成器
        generator = HandoverGenerator("张三", "zhangsan@example.com")
        
        # 3. 添加文档
        generator.add_documents(data["data"]["results"])
        
        # 4. 验证统计
        assert len(generator.documents) == 5
        assert len(generator.created_docs) == 3
        assert len(generator.collaborated_docs) == 2
        
        # 5. 生成分类
        type_stats = generator.categorize_by_type()
        theme_stats = generator.categorize_by_theme()
        importance_stats = generator.categorize_by_importance()
        
        assert len(type_stats) > 0
        assert len(theme_stats) > 0
        assert len(importance_stats) > 0
        
        # 6. 生成文档
        md_content = generator.generate_markdown()
        assert "🚀 EvoLeap 运营作战中枢" in md_content
        assert "GEO智能体/Skill体系设计" in md_content
        
        # 7. 保存文件
        output_md = tmp_path / "交接清单.md"
        generator.save_markdown(str(output_md))
        assert output_md.exists()
        
        # 8. 导出 JSON
        json_str = generator.to_json()
        json_data = json.loads(json_str)
        assert json_data["user_name"] == "张三"
        assert json_data["statistics"]["total_docs"] == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
