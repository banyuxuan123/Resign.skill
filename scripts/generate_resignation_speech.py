#!/usr/bin/env python3
"""
离职话术生成脚本

根据老板的性格特征生成个性化的离职话术

使用方法:
    # 交互式使用
    python scripts/generate_resignation_speech.py --interactive
    
    # 命令行参数
    python scripts/generate_resignation_speech.py \
        --name 张 \
        --gender 男 \
        --age 40-50 \
        --mbti ENTJ \
        --reason NEW_OPPORTUNITY \
        --last-day "2026年4月30日"
"""

import argparse
import json
import sys
from pathlib import Path

# 添加 skill 到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from skills.lark_handover.resignation_speech import (
    ResignationSpeechGenerator,
    BossProfile,
    ResignationReason,
    generate_resignation_speech
)


def print_reason_options():
    """打印离职理由选项"""
    generator = ResignationSpeechGenerator()
    options = generator.get_reason_options()
    
    print("\n" + "=" * 60)
    print("📋 离职理由选项")
    print("=" * 60)
    
    for category in options:
        print(f"\n【{category['category']}】")
        for reason in category['reasons']:
            print(f"  {reason['key']:20} - {reason['label']:<15} ({reason['description']})")
    
    print("\n" + "=" * 60)


def print_mbti_guide():
    """打印 MBTI 指南"""
    print("\n" + "=" * 60)
    print("🧠 MBTI 类型参考")
    print("=" * 60)
    
    mbti_types = {
        "分析家 (NT)": ["INTJ", "INTP", "ENTJ", "ENTP"],
        "外交官 (NF)": ["INFJ", "INFP", "ENFJ", "ENFP"],
        "守护者 (SJ)": ["ISTJ", "ISFJ", "ESTJ", "ESFJ"],
        "探险家 (SP)": ["ISTP", "ISFP", "ESTP", "ESFP"]
    }
    
    for category, types in mbti_types.items():
        print(f"\n{category}:")
        for t in types:
            print(f"  - {t}")
    
    print("\n提示：如果不知道老板 MBTI，可以选 '未知'")
    print("=" * 60 + "\n")


def interactive_mode():
    """交互式模式"""
    
    print("\n" + "=" * 60)
    print("🎯 离职话术生成器 - 交互模式")
    print("=" * 60 + "\n")
    
    # 收集老板信息
    print("【老板信息】\n")
    
    name = input("1. 老板姓氏（如：张）: ").strip()
    
    gender = input("\n2. 性别（男/女/未知）: ").strip()
    while gender not in ["男", "女", "未知"]:
        gender = input("   请输入 男/女/未知: ").strip()
    
    print("\n3. 年龄段:")
    print("   - 30以下")
    print("   - 30-40")
    print("   - 40-50")
    print("   - 50+")
    age = input("   请选择: ").strip()
    
    print_mbti_guide()
    mbti = input("4. 老板 MBTI（不知道输'未知'）: ").strip().upper()
    
    print("\n5. 性格特征（选填，多个用逗号分隔）:")
    print("   例如：理性,直接,注重细节,温和,果断,敏感")
    traits_input = input("   请输入: ").strip()
    traits = [t.strip() for t in traits_input.split(",") if t.strip()]
    
    print("\n6. 沟通风格:")
    print("   - 直接（喜欢开门见山）")
    print("   - 委婉（需要铺垫）")
    print("   - 正式（注重礼仪）")
    print("   - 随意（比较轻松）")
    style = input("   请选择: ").strip()
    
    print("\n7. 关系亲疏:")
    print("   - 亲近（关系很好，常聊天）")
    print("   - 一般（正常工作关系）")
    print("   - 疏远（接触不多）")
    relationship = input("   请选择: ").strip()
    
    # 选择离职理由
    print_reason_options()
    
    reason_key = input("\n8. 请选择离职理由（输入 KEY，如 NEW_OPPORTUNITY）: ").strip().upper()
    
    last_day = input("\n9. 计划最后工作日（如：2026年4月30日/30天后）: ").strip()
    
    # 生成话术
    print("\n" + "=" * 60)
    print("⏳ 正在生成话术...")
    print("=" * 60 + "\n")
    
    try:
        result = generate_resignation_speech(
            boss_name=name,
            boss_gender=gender,
            boss_age=age,
            boss_mbti=mbti,
            reason_key=reason_key,
            last_day=last_day,
            personality_traits=traits,
            communication_style=style,
            relationship=relationship
        )
        
        # 显示结果
        print("\n" + "=" * 60)
        print("✅ 生成完成！")
        print("=" * 60)
        
        for version, speech in result.items():
            if version.startswith("_"):
                continue
            
            print(f"\n{'=' * 60}")
            print(f"📌 {version}")
            print(f"{'=' * 60}\n")
            print(speech)
        
        # 显示 Q&A 指南
        print(f"\n{'=' * 60}")
        print("📚 离职面谈 Q&A 指南")
        print(f"{'=' * 60}\n")
        print(result.get("_qa_guide", ""))
        
        # 询问是否保存
        save = input("\n\n是否保存到文件？(y/n): ").strip().lower()
        if save == "y":
            filename = input("文件名（默认：离职话术.txt）: ").strip() or "离职话术.txt"
            
            with open(filename, "w", encoding="utf-8") as f:
                for version, speech in result.items():
                    if version.startswith("_"):
                        continue
                    f.write(f"{'=' * 60}\n")
                    f.write(f"{version}\n")
                    f.write(f"{'=' * 60}\n\n")
                    f.write(speech)
                    f.write("\n\n")
                
                f.write(f"{'=' * 60}\n")
                f.write("离职面谈 Q&A 指南\n")
                f.write(f"{'=' * 60}\n\n")
                f.write(result.get("_qa_guide", ""))
            
            print(f"\n✅ 已保存到: {filename}")
        
    except Exception as e:
        print(f"\n❌ 生成失败: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="离职话术生成器 - 根据老板性格生成个性化离职话术",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 交互式模式（推荐）
  python scripts/generate_resignation_speech.py --interactive
  
  # 查看离职理由选项
  python scripts/generate_resignation_speech.py --list-reasons
  
  # 命令行模式
  python scripts/generate_resignation_speech.py \\
      --name 张 \\
      --gender 男 \\
      --age 40-50 \\
      --mbti ENTJ \\
      --reason NEW_OPPORTUNITY \\
      --last-day "2026年4月30日"
        """
    )
    
    # 主要参数
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="交互式模式（推荐）"
    )
    
    parser.add_argument(
        "--name",
        help="老板姓氏（如：张）"
    )
    
    parser.add_argument(
        "--gender",
        choices=["男", "女", "未知"],
        help="老板性别"
    )
    
    parser.add_argument(
        "--age",
        choices=["30以下", "30-40", "40-50", "50+"],
        help="老板年龄段"
    )
    
    parser.add_argument(
        "--mbti",
        help="老板 MBTI 类型（如：ENTJ）"
    )
    
    parser.add_argument(
        "--reason",
        help="离职理由 KEY（见 --list-reasons）"
    )
    
    parser.add_argument(
        "--last-day",
        default="30天后",
        help="最后工作日（默认：30天后）"
    )
    
    parser.add_argument(
        "--traits",
        help="性格特征，逗号分隔（如：理性,直接,果断）"
    )
    
    parser.add_argument(
        "--style",
        choices=["直接", "委婉", "正式", "随意"],
        default="直接",
        help="沟通风格"
    )
    
    parser.add_argument(
        "--relationship",
        choices=["亲近", "一般", "疏远"],
        default="一般",
        help="关系亲疏"
    )
    
    parser.add_argument(
        "--list-reasons",
        action="store_true",
        help="列出所有离职理由选项"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="输出文件路径"
    )
    
    args = parser.parse_args()
    
    # 列出席项
    if args.list_reasons:
        print_reason_options()
        return 0
    
    # 交互模式
    if args.interactive or (not args.name and not args.reason):
        interactive_mode()
        return 0
    
    # 命令行模式
    if not all([args.name, args.gender, args.age, args.mbti, args.reason]):
        print("❌ 缺少必要参数")
        print("\n请使用 --interactive 进入交互模式，或提供以下参数：")
        print("  --name, --gender, --age, --mbti, --reason")
        print("\n查看帮助：python scripts/generate_resignation_speech.py --help")
        return 1
    
    # 生成话术
    try:
        result = generate_resignation_speech(
            boss_name=args.name,
            boss_gender=args.gender,
            boss_age=args.age,
            boss_mbti=args.mbti,
            reason_key=args.reason,
            last_day=args.last_day,
            personality_traits=args.traits.split(",") if args.traits else [],
            communication_style=args.style,
            relationship=args.relationship
        )
        
        # 输出
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                for version, speech in result.items():
                    if version.startswith("_"):
                        continue
                    f.write(f"{'=' * 60}\n")
                    f.write(f"{version}\n")
                    f.write(f"{'=' * 60}\n\n")
                    f.write(speech)
                    f.write("\n\n")
            
            print(f"✅ 已保存到: {args.output}")
        else:
            for version, speech in result.items():
                if version.startswith("_"):
                    continue
                
                print(f"\n{'=' * 60}")
                print(f"📌 {version}")
                print(f"{'=' * 60}\n")
                print(speech)
        
        return 0
        
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
