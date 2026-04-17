#!/usr/bin/env python3
"""
飞书离职交接文档生成脚本

使用方法：
1. 确保已安装 lark-cli 并完成授权
2. 运行：python scripts/generate_handover.py --user 你的姓名
3. 文档将自动上传到飞书

或者从 JSON 文件导入：
  python scripts/generate_handover.py --user 你的姓名 --input docs.json
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

# 添加 skill 到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from skills.lark_handover.handover import HandoverGenerator


def fetch_docs_from_feishu(query: str = "", page_size: int = 100) -> list:
    """
    从飞书获取文档数据
    
    需要提前完成 lark-cli 授权：
    lark-cli auth login --no-wait --domain all
    """
    try:
        # 调用 lark-cli 搜索文档
        cmd = [
            "lark-cli", "docs", "+search",
            "--query", query,
            "--page-size", str(page_size),
            "--format", "json",
            "--as", "user"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ 获取文档失败：{result.stderr}")
            return []
        
        # 解析 JSON 输出
        output = json.loads(result.stdout)
        
        if output.get("ok"):
            return output.get("data", {}).get("results", [])
        else:
            print(f"❌ API 错误：{output.get('error')}")
            return []
            
    except Exception as e:
        print(f"❌ 执行失败：{e}")
        print("\n💡 请确保：")
        print("  1. 已安装 lark-cli")
        print("  2. 已完成授权：lark-cli auth login --no-wait --domain all")
        return []


def upload_to_feishu(file_path: str, title: str = None) -> str:
    """上传到飞书云文档"""
    try:
        cmd_title = title or Path(file_path).stem
        cmd = [
            "lark-cli", "docs", "+create",
            "--markdown", f"@{file_path}",
            "--title", cmd_title,
            "--as", "user"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            output = json.loads(result.stdout)
            if output.get("ok"):
                doc_url = output.get("data", {}).get("doc_url", "")
                print(f"✅ 已上传到飞书：{doc_url}")
                return doc_url
        
        print(f"⚠️ 上传失败：{result.stderr}")
        return ""
        
    except Exception as e:
        print(f"❌ 上传失败：{e}")
        return ""


def main():
    parser = argparse.ArgumentParser(
        description="生成飞书离职交接文档"
    )
    
    parser.add_argument(
        "--user", "-u",
        required=True,
        help="交接人姓名"
    )
    
    parser.add_argument(
        "--email", "-e",
        default="",
        help="交接人邮箱"
    )
    
    parser.add_argument(
        "--input", "-i",
        help="从 JSON 文件导入（可选，默认从飞书API获取）"
    )
    
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="输出文件路径（默认：{user}_交接清单.md）"
    )
    
    parser.add_argument(
        "--upload", "--feishu",
        action="store_true",
        default=True,
        help="上传到飞书云文档（默认开启）"
    )
    
    parser.add_argument(
        "--no-upload",
        action="store_true",
        help="不上传到飞书，仅生成本地文件"
    )
    
    args = parser.parse_args()
    
    # 确定是否上传
    should_upload = args.upload and not args.no_upload
    
    # 确定输出路径
    if args.output:
        output_path = args.output
    else:
        output_path = f"{args.user}_交接清单.md"
    
    print(f"🚀 开始生成交接文档...")
    print(f"   交接人：{args.user}")
    print(f"   输出文件：{output_path}")
    print()
    
    # 获取文档数据
    if args.input:
        print(f"📂 从文件导入：{args.input}")
        with open(args.input, 'r', encoding='utf-8') as f:
            docs_data = json.load(f)
    else:
        print("🔍 从飞书获取文档数据...")
        print("   提示：如未授权，请先运行：lark-cli auth login --no-wait --domain all")
        print()
        docs_data = fetch_docs_from_feishu()
    
    if not docs_data:
        print("❌ 未能获取文档数据，退出")
        return 1
    
    print(f"✅ 获取到 {len(docs_data)} 篇文档")
    print()
    
    # 创建生成器
    generator = HandoverGenerator(args.user, args.email)
    generator.add_documents(docs_data)
    
    # 生成本地文件
    generator.save_markdown(output_path)
    print(f"✅ Markdown 文档已生成：{output_path}")
    
    # 同时生成 JSON 备份
    json_path = output_path.replace('.md', '.json')
    json_content = generator.to_json()
    with open(json_path, 'w', encoding='utf-8') as f:
        f.write(json_content)
    print(f"✅ JSON 备份已生成：{json_path}")
    
    # 上传到飞书
    if should_upload:
        print()
        print("📤 正在上传到飞书云文档...")
        doc_url = upload_to_feishu(output_path, f"{args.user}-云文档交接清单")
        
        if doc_url:
            print(f"\n🔗 飞书文档链接：{doc_url}")
    
    # 打印统计
    print()
    print("=" * 50)
    print("📊 文档统计")
    print("=" * 50)
    print(f"  文档总数：{len(generator.documents)}")
    print(f"  创建文档：{len(generator.created_docs)}")
    print(f"  协作文档：{len(generator.collaborated_docs)}")
    print()
    
    # 按类型统计
    type_stats = generator.categorize_by_type()
    if type_stats:
        print("📁 按类型分布：")
        for doc_type, docs in sorted(type_stats.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"    - {doc_type}: {len(docs)} 篇")
    
    # 按分类统计
    theme_stats = generator.categorize_by_theme()
    if theme_stats:
        print()
        print("🏷️ 按主题分布：")
        for theme, docs in sorted(theme_stats.items(), key=lambda x: len(x[1]), reverse=True)[:5]:
            print(f"    - {theme}: {len(docs)} 篇")
    
    print()
    print("✨ 完成！")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
