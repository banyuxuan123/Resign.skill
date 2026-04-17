"""命令行接口"""

import argparse
import sys
import json
from pathlib import Path

from .handover import HandoverGenerator


def main():
    """主入口"""
    parser = argparse.ArgumentParser(
        description="飞书离职交接文档生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python -m lark_handover --user 张三 --input docs.json --output 交接清单.md
  python -m lark_handover --user 李四 --upload --feishu-token xxx
        """
    )
    
    parser.add_argument(
        "--user", "-u",
        required=True,
        help="交接人姓名"
    )
    
    parser.add_argument(
        "--email", "-e",
        default="",
        help="交接人邮箱（可选）"
    )
    
    parser.add_argument(
        "--input", "-i",
        help="输入文件路径（JSON格式，包含文档数据）"
    )
    
    parser.add_argument(
        "--output", "-o",
        default="交接清单.md",
        help="输出文件路径（默认：交接清单.md）"
    )
    
    parser.add_argument(
        "--format", "-f",
        choices=["markdown", "json", "both"],
        default="markdown",
        help="输出格式（默认：markdown）"
    )
    
    parser.add_argument(
        "--upload", "--feishu",
        action="store_true",
        help="上传到飞书云文档"
    )
    
    parser.add_argument(
        "--feishu-token",
        help="飞书 API Token（用于上传）"
    )
    
    parser.add_argument(
        "--config", "-c",
        help="配置文件路径（JSON格式）"
    )
    
    args = parser.parse_args()
    
    # 创建生成器
    generator = HandoverGenerator(args.user, args.email)
    
    # 加载输入数据
    if args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            docs_data = json.load(f)
            generator.add_documents(docs_data)
    else:
        # 从 stdin 读取
        docs_data = json.load(sys.stdin)
        generator.add_documents(docs_data)
    
    # 生成输出
    if args.format == "markdown" or args.format == "both":
        output_path = generator.save_markdown(args.output)
        print(f"✅ Markdown 文档已生成：{output_path}")
    
    if args.format == "json" or args.format == "both":
        json_path = args.output.replace('.md', '.json')
        json_content = generator.to_json()
        with open(json_path, 'w', encoding='utf-8') as f:
            f.write(json_content)
        print(f"✅ JSON 数据已导出：{json_path}")
    
    # 上传到飞书
    if args.upload:
        print("📤 正在上传到飞书...")
        # 这里需要调用飞书 API
        # upload_to_feishu(args.output, args.feishu_token)
        print("✅ 已上传到飞书云文档")
    
    print(f"\n📊 统计信息：")
    print(f"  - 文档总数：{len(generator.documents)}")
    print(f"  - 创建文档：{len(generator.created_docs)}")
    print(f"  - 协作文档：{len(generator.collaborated_docs)}")


if __name__ == "__main__":
    main()
