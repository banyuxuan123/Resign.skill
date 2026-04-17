"""离职话术生成器

根据老板的性格特征、MBTI类型、偏好等生成个性化的离职话术
"""

import random
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class ResignationReason(Enum):
    """离职原因选项"""
    # 职业发展类
    CAREER_GROWTH = "个人职业发展规划"
    NEW_OPPORTUNITY = "新的职业机会"
    STARTUP = "创业"
    STUDY = "继续深造/学习"
    INDUSTRY_CHANGE = "行业转型"
    
    # 个人原因类
    FAMILY = "家庭原因"
    HEALTH = "健康原因"
    RELOCATION = " relocating/搬家"
    WORK_LIFE_BALANCE = "工作生活平衡"
    BURNOUT = "职业倦怠，需要休息调整"
    
    # 客观原因类
    CONTRACT_END = "合同到期"
    COMPANY_CHANGE = "公司战略调整/部门变动"
    PROJECT_END = "项目结束"
    
    # 其他
    OTHER = "其他个人原因"


@dataclass
class BossProfile:
    """老板画像"""
    name: str  # 老板姓名/称呼
    gender: str  # 性别: "男" | "女" | "未知"
    age_range: str  # 年龄段: "30以下" | "30-40" | "40-50" | "50+"
    mbti: str  # MBTI类型，如 "ENTJ", "ISFJ" 等
    personality_traits: List[str]  # 性格特征，如 ["理性", "直接", "注重细节"]
    communication_style: str  # 沟通风格: "直接" | "委婉" | "正式" | "随意"
    values: List[str]  # 看重什么: ["效率", "忠诚", "创新", "稳定"]
    relationship: str  # 关系亲疏: "亲近" | "一般" | "疏远"
    
    def __post_init__(self):
        """验证和标准化"""
        self.mbti = self.mbti.upper() if self.mbti else "未知"
        self.gender = self.gender if self.gender in ["男", "女"] else "未知"


class ResignationSpeechGenerator:
    """离职话术生成器"""
    
    # MBTI 特征映射
    MBTI_TRAITS = {
        # 分析家 (NT)
        "INTJ": {
            "traits": ["战略性", "独立", "理性", "完美主义"],
            "style": "逻辑清晰，重视长远规划",
            "keywords": ["规划", "战略", "目标", "效率"],
            "approach": "用数据和逻辑说明，强调职业规划"
        },
        "INTP": {
            "traits": ["分析型", "好奇", "客观", "灵活"],
            "style": "喜欢深入探讨原因",
            "keywords": ["探索", "分析", "理解", "可能性"],
            "approach": "坦诚分享思考过程，给足思考空间"
        },
        "ENTJ": {
            "traits": ["果断", "领导力", "效率", "目标导向"],
            "style": "直接高效，注重结果",
            "keywords": ["目标", "效率", "成果", "挑战"],
            "approach": "开门见山，强调新机会的成长性"
        },
        "ENTP": {
            "traits": ["创新", "机智", "辩论", "灵活"],
            "style": "喜欢讨论和新想法",
            "keywords": ["创新", "可能性", "挑战", "成长"],
            "approach": "以探讨的方式，展现对新机会的兴奋"
        },
        # 外交官 (NF)
        "INFJ": {
            "traits": ["理想主义", "洞察", "同理心", "深度"],
            "style": "重视意义和价值观",
            "keywords": ["意义", "成长", "价值", "理解"],
            "approach": "真诚表达感激，说明对个人成长的思考"
        },
        "INFP": {
            "traits": ["理想主义", "创意", "共情", "灵活"],
            "style": "温和敏感，重视真诚",
            "keywords": ["热情", "意义", "成长", "可能性"],
            "approach": "表达真挚情感，强调追随内心的决定"
        },
        "ENFJ": {
            "traits": [" charismatic", "激励", "同理心", "组织"],
            "style": "关注他人感受，善于沟通",
            "keywords": ["成长", "团队", "贡献", "发展"],
            "approach": "强调对团队的感激，说明是艰难但必要的决定"
        },
        "ENFP": {
            "traits": ["热情", "创意", "社交", "灵活"],
            "style": "热情开朗，喜欢新可能",
            "keywords": ["兴奋", "可能性", "成长", "新挑战"],
            "approach": "分享对新机会的兴奋，保持积极和热情"
        },
        # 守护者 (SJ)
        "ISTJ": {
            "traits": ["务实", "可靠", "注重细节", "传统"],
            "style": "重视责任和稳定",
            "keywords": ["责任", "稳定", "计划", "交接"],
            "approach": "强调会妥善交接，展现对责任的重视"
        },
        "ISFJ": {
            "traits": ["温暖", "尽责", "细致", "保护"],
            "style": "关心他人，重视和谐",
            "keywords": ["感激", "责任", "团队", "支持"],
            "approach": "表达感激之情，强调会确保平稳过渡"
        },
        "ESTJ": {
            "traits": ["务实", "果断", "组织", "直接"],
            "style": "高效直接，注重结果",
            "keywords": ["效率", "计划", "成果", "责任"],
            "approach": "直接说明，强调交接计划和最后工作日"
        },
        "ESFJ": {
            "traits": ["热心", "合作", "负责", "传统"],
            "style": "关注关系和谐",
            "keywords": ["感激", "团队", "支持", "关系"],
            "approach": "强调团队情谊，表达不舍但尊重个人发展"
        },
        # 探险家 (SP)
        "ISTP": {
            "traits": ["实用", "灵活", "分析", "独立"],
            "style": "务实低调",
            "keywords": ["实用", "灵活", "机会", "技能"],
            "approach": "简洁直接，说明新机会对技能发展的帮助"
        },
        "ISFP": {
            "traits": ["温和", "艺术", "敏感", "当下"],
            "style": "重视个人价值和感受",
            "keywords": ["热情", "价值", "成长", "可能性"],
            "approach": "温和真诚，表达追随内心选择的必要性"
        },
        "ESTP": {
            "traits": ["活力", "务实", "冒险", "直接"],
            "style": "喜欢行动和挑战",
            "keywords": ["挑战", "机会", "行动", "成长"],
            "approach": "直接坦诚，展现对新挑战的兴奋"
        },
        "ESFP": {
            "traits": ["热情", "社交", "自发", "享乐"],
            "style": "热情友好，活在当下",
            "keywords": ["兴奋", "机会", "体验", "热情"],
            "approach": "热情分享新机会，强调难得的机遇"
        },
        "未知": {
            "traits": ["综合型"],
            "style": "平衡稳重",
            "keywords": ["发展", "规划", "感激", "成长"],
            "approach": "真诚表达，强调职业发展规划"
        }
    }
    
    # 年龄段特征
    AGE_STYLES = {
        "30以下": {
            "style": "轻松平等，可以理解年轻人跳槽",
            "tone": "casual",
            "expectation": "理解职业探索期"
        },
        "30-40": {
            "style": "专业理性，重视职业发展逻辑",
            "tone": "professional",
            "expectation": "看重成长性和职业规划"
        },
        "40-50": {
            "style": "尊重经验，重视稳定性",
            "tone": "respectful",
            "expectation": "重视忠诚度和长期价值"
        },
        "50+": {
            "style": "尊敬传统，强调感恩",
            "tone": "formal_respectful",
            "expectation": "看重人品和责任感"
        }
    }
    
    # 性别称谓映射
    TITLES = {
        "男": {
            "formal": "X总",
            "casual": "X哥",
            "respectful": "X总/老师",
            "friendly": "老大"
        },
        "女": {
            "formal": "X总",
            "casual": "X姐",
            "respectful": "X总/老师",
            "friendly": "老大"
        },
        "未知": {
            "formal": "领导",
            "casual": "老大",
            "respectful": "领导/老师",
            "friendly": "老大"
        }
    }
    
    # 离职理由话术模板
    REASON_TEMPLATES = {
        ResignationReason.CAREER_GROWTH: {
            "general": "经过深思熟虑，我决定接受一个新的职业机会，这将有助于我的长期职业发展。",
            "ambitious": "我希望在职业生涯的这个阶段，挑战更大的责任和更广阔的发展空间。",
            "learning": "我希望能接触新的领域和技能，拓宽自己的职业视野。"
        },
        ResignationReason.NEW_OPPORTUNITY: {
            "general": "我收到了一个非常难得的机会，经过慎重考虑，决定接受这个挑战。",
            "exciting": "这个机会与我长期的职业目标高度契合，我希望能尝试一下。",
            "unexpected": "这个机会出现得比较突然，但我觉得值得去尝试。"
        },
        ResignationReason.STARTUP: {
            "general": "我决定尝试创业，这是我长期以来的一个想法。",
            "dream": "我有一个创业的想法想付诸实践，想趁年轻闯一闯。",
            "side_project": "我的副业发展得不错，我想全职投入试试。"
        },
        ResignationReason.FAMILY: {
            "general": "由于家庭原因，我需要调整工作地点/时间。",
            "caregiving": "家里有些情况需要我投入更多精力，我需要重新平衡工作和家庭。",
            "relocation": "家庭计划 relocating 到另一个城市，所以我不得不离职。"
        },
        ResignationReason.HEALTH: {
            "general": "最近身体有些状况，需要一段时间好好休息和调整。",
            "burnout": "我感觉最近有些透支，需要停下来调整一下节奏。",
            "stress": "工作压力对我的健康有些影响，我想暂时放慢脚步。"
        },
        ResignationReason.WORK_LIFE_BALANCE: {
            "general": "我希望找到更好的工作生活平衡。",
            "flexibility": "我希望能有更多灵活的时间安排。",
            "priority": "我现在想把更多精力放在生活上。"
        },
        ResignationReason.STUDY: {
            "general": "我计划继续深造/学习新的技能。",
            "degree": "我打算去读一个学位/证书。",
            "skill": "我想全职学习一些新的专业技能。"
        }
    }
    
    def __init__(self):
        self.boss_profile: Optional[BossProfile] = None
    
    def set_profile(self, profile: BossProfile):
        """设置老板画像"""
        self.boss_profile = profile
    
    def generate_speech(
        self,
        reason: ResignationReason,
        last_day: str = "30天后",
        additional_context: str = "",
        tone: str = "真诚专业"
    ) -> Dict[str, str]:
        """
        生成离职话术
        
        Args:
            reason: 离职原因
            last_day: 最后工作日
            additional_context: 额外上下文信息
            tone: 语气风格
            
        Returns:
            包含不同版本话术的字典
        """
        if not self.boss_profile:
            raise ValueError("请先设置老板画像 (set_profile)")
        
        mbti_info = self.MBTI_TRAITS.get(
            self.boss_profile.mbti, 
            self.MBTI_TRAITS["未知"]
        )
        
        age_info = self.AGE_STYLES.get(
            self.boss_profile.age_range,
            self.AGE_STYLES["30-40"]
        )
        
        # 确定称谓
        title = self._get_title(age_info["tone"])
        
        # 生成不同版本
        versions = {
            "正式版": self._generate_formal_version(
                title, reason, mbti_info, age_info, last_day, additional_context
            ),
            "轻松版": self._generate_casual_version(
                title, reason, mbti_info, age_info, last_day, additional_context
            ),
            "简短版": self._generate_short_version(
                title, reason, mbti_info, last_day
            ),
            "微信/钉钉版": self._generate_chat_version(
                title, reason, mbti_info, last_day
            )
        }
        
        return versions
    
    def _get_title(self, tone: str) -> str:
        """获取合适的称谓"""
        gender = self.boss_profile.gender
        
        if tone == "formal":
            return self.TITLES[gender]["formal"].replace("X", self.boss_profile.name[0])
        elif tone == "casual":
            return self.TITLES[gender]["casual"].replace("X", self.boss_profile.name[0])
        elif tone == "respectful":
            return self.TITLES[gender]["respectful"].replace("X", self.boss_profile.name[0])
        else:
            return self.TITLES[gender]["friendly"]
    
    def _generate_formal_version(
        self,
        title: str,
        reason: ResignationReason,
        mbti_info: Dict,
        age_info: Dict,
        last_day: str,
        context: str
    ) -> str:
        """生成正式版本"""
        
        # 开场
        opening = self._generate_opening(title, "formal")
        
        # 原因阐述
        reason_text = self._generate_reason_text(reason, mbti_info)
        
        # 感激部分
        gratitude = self._generate_gratitude(title, mbti_info)
        
        # 交接承诺
        handover = self._generate_handover_commitment(mbti_info)
        
        # 结尾
        closing = self._generate_closing(title, last_day, "formal")
        
        speech = f"""{opening}

{reason_text}

{gratitude}

{handover}

{closing}"""
        
        return speech
    
    def _generate_casual_version(
        self,
        title: str,
        reason: ResignationReason,
        mbti_info: Dict,
        age_info: Dict,
        last_day: str,
        context: str
    ) -> str:
        """生成轻松版本"""
        
        opening = f"{title}，想跟您聊个事儿~"
        
        reason_text = self._generate_reason_text(reason, mbti_info, tone="casual")
        
        gratitude = f"跟您干这两年真的学到特别多，特别感谢您一直以来的提携和信任。"
        
        closing = f"我会做好交接，{last_day}正式离开。以后咱们常联系！"
        
        speech = f"""{opening}

{reason_text}

{gratitude}

{closing}"""
        
        return speech
    
    def _generate_short_version(
        self,
        title: str,
        reason: ResignationReason,
        mbti_info: Dict,
        last_day: str
    ) -> str:
        """生成简短版本（适合紧急情况）"""
        
        reason_brief = self._get_reason_brief(reason)
        
        speech = f"""{title}，我决定离职了。

原因：{reason_brief}
最后工作日：{last_day}

感谢您一直以来的指导，我会认真做好交接。"""
        
        return speech
    
    def _generate_chat_version(
        self,
        title: str,
        reason: ResignationReason,
        mbti_info: Dict,
        last_day: str
    ) -> str:
        """生成微信/钉钉版本（分段发送）"""
        
        messages = [
            f"{title}，有个事儿想跟您说一下。",
            "我打算离职了。",
            self._get_reason_brief(reason),
            f"计划{last_day}离开。",
            "感谢您一直以来的指导和信任！我会认真做好交接。",
            "您看什么时候方便，我想当面跟您详细聊聊。"
        ]
        
        return "\n\n".join([f"【消息{i+1}】{msg}" for i, msg in enumerate(messages)])
    
    def _generate_opening(self, title: str, style: str) -> str:
        """生成开场白"""
        openings = {
            "formal": [
                f"{title}，您好。",
                f"{title}，打扰了。",
                f"{title}，想占用您一点时间。"
            ],
            "casual": [
                f"{title}，有空吗？想跟您聊聊。",
                f"{title}，有个事儿想跟您说。"
            ]
        }
        return random.choice(openings.get(style, openings["formal"]))
    
    def _generate_reason_text(
        self, 
        reason: ResignationReason, 
        mbti_info: Dict,
        tone: str = "formal"
    ) -> str:
        """生成原因阐述"""
        
        templates = self.REASON_TEMPLATES.get(reason, self.REASON_TEMPLATES[ResignationReason.CAREER_GROWTH])
        
        if tone == "casual":
            return templates.get("general", "")
        
        # 根据 MBTI 特点调整表述
        mbti_style = mbti_info.get("approach", "")
        
        if "逻辑" in mbti_style or "数据" in mbti_style:
            return f"经过深思熟虑和理性分析，{templates.get('general', '')}"
        elif "真诚" in mbti_style or "情感" in mbti_style:
            return f"这是一个艰难的决定，{templates.get('general', '')}"
        elif "直接" in mbti_style:
            return templates.get("general", "")
        else:
            return templates.get("general", "")
    
    def _generate_gratitude(self, title: str, mbti_info: Dict) -> str:
        """生成感激部分"""
        
        # 根据关系亲疏调整
        relationship = self.boss_profile.relationship
        
        if relationship == "亲近":
            gratitudes = [
                f"跟着您这段时间，真的学到了很多，不只是工作上的，还有做人做事的道理。",
                f"特别感谢您一直以来的信任和支持，这段时间的成长离不开您的指导。",
                f"很感激能有这样的机会跟着您学习，这段经历对我职业生涯影响很深。"
            ]
        elif relationship == "疏远":
            gratitudes = [
                f"感谢您提供的工作机会和学习平台。",
                f"感谢公司和团队给予的成长机会。"
            ]
        else:  # 一般
            gratitudes = [
                f"非常感谢您一直以来的指导和支持，这段时间的工作经历让我受益匪浅。",
                f"感谢您给予的机会和信任，在这里学到了很多宝贵的经验。",
                f"很感激能在这个团队工作，您的专业态度和领导力给了我很大启发。"
            ]
        
        return random.choice(gratitudes)
    
    def _generate_handover_commitment(self, mbti_info: Dict) -> str:
        """生成交接承诺"""
        
        # 根据 MBTI 看重的点来调整
        values = self.boss_profile.values
        
        commitments = [
            "我会认真做好工作交接，确保不影响团队运转。",
            "我会整理好所有文档和资料，做好详细的交接清单。",
            "在离职前，我会把手上的工作都处理完，做好交接准备。",
            "如果需要，我也可以协助培养接手人，确保平稳过渡。"
        ]
        
        # 如果老板看重效率
        if "效率" in values or "结果" in values:
            return "我会高效完成交接，确保不影响团队进度，所有文档都会整理清楚。"
        
        # 如果老板看重忠诚
        if "忠诚" in values or "稳定" in values:
            return "虽然要离开，但我对公司的感情不会变，会认真做好最后阶段的工作，确保平稳过渡。"
        
        return random.choice(commitments)
    
    def _generate_closing(self, title: str, last_day: str, style: str) -> str:
        """生成结尾"""
        
        closings = {
            "formal": [
                f"希望您能理解我的决定。我计划 {last_day} 正式离职，在这之前会全力做好交接工作。再次感谢您的理解和支持。",
                f"非常抱歉给您和团队带来不便。我会以 {last_day} 为最后工作日，在此之前确保所有工作顺利交接。",
                f"感谢您抽出时间阅读这封信。期待您的理解，我会确保 {last_day} 之前的交接工作顺利完成。"
            ],
            "casual": [
                f"{title}，希望您能理解。我计划{last_day}离开，会认真做好交接的。",
                f"您看这样可以吗？我会做到{last_day}，把交接都做好的。"
            ]
        }
        
        return random.choice(closings.get(style, closings["formal"]))
    
    def _get_reason_brief(self, reason: ResignationReason) -> str:
        """获取离职原因简述"""
        briefs = {
            ResignationReason.CAREER_GROWTH: "个人职业发展",
            ResignationReason.NEW_OPPORTUNITY: "新的职业机会",
            ResignationReason.STARTUP: "创业",
            ResignationReason.FAMILY: "家庭原因",
            ResignationReason.HEALTH: "健康原因",
            ResignationReason.WORK_LIFE_BALANCE: "工作生活平衡",
            ResignationReason.STUDY: "继续深造",
            ResignationReason.BURNOUT: "需要休息调整",
            ResignationReason.RELOCATION: "搬家/relocate",
            ResignationReason.INDUSTRY_CHANGE: "行业转型",
            ResignationReason.CONTRACT_END: "合同到期",
            ResignationReason.COMPANY_CHANGE: "公司调整",
            ResignationReason.PROJECT_END: "项目结束",
            ResignationReason.OTHER: "个人原因"
        }
        return briefs.get(reason, "个人原因")
    
    def generate_qa_guide(self) -> str:
        """生成离职面谈 Q&A 指南"""
        
        if not self.boss_profile:
            raise ValueError("请先设置老板画像")
        
        mbti_info = self.MBTI_TRAITS.get(
            self.boss_profile.mbti,
            self.MBTI_TRAITS["未知"]
        )
        
        qa_guide = f"""# 离职面谈 Q&A 准备指南

## 老板画像分析
- **MBTI**: {self.boss_profile.mbti}
- **性格特征**: {', '.join(mbti_info['traits'])}
- **沟通风格**: {mbti_info['style']}
- **应对策略**: {mbti_info['approach']}

## 可能的问题及建议回答

### 1. "为什么突然要离职？"
**建议回答**: 
"不是突然的决定，我思考了一段时间。主要是 [{self._get_reason_brief(ResignationReason.CAREER_GROWTH)}]，我觉得现在是个合适的时机。"

### 2. "是不是对公司/我有什么不满？"
**建议回答**:
"绝对不是。我非常感激在这里的经历，离职纯粹是个人发展考虑，和公司、您都没有关系。"

### 3. "有没有挽留的可能？"
**建议回答**:
（根据自己的真实想法回答）
- 如果确定要走："这个决定已经深思熟虑，希望您能理解。"
- 如果有条件留下："如果能在XX方面有所改善，我会重新考虑。"

### 4. "下一站去哪里？"
**建议回答**:
"是一家做XX的公司/我准备创业/我计划休息一段时间。"（根据自己的情况，可以说具体也可以说模糊）

### 5. "对公司和团队有什么建议？"
**建议回答**:
"整体来说都很好，如果一定要说，我觉得可以在XX方面加强...（说一个建设性但不伤人的点）"

## 面谈技巧

### 针对 {self.boss_profile.mbti} 型老板
"""
        
        # 添加针对 MBTI 的技巧
        if self.boss_profile.mbti in ["ENTJ", "ESTJ"]:
            qa_guide += """
- 准备充分，用数据和事实说话
- 直接表达，不要绕弯子
- 强调交接计划，展现责任感
- 准备好最后工作日和交接安排
"""
        elif self.boss_profile.mbti in ["INFJ", "INFP", "ENFJ"]:
            qa_guide += """
- 真诚表达感激之情
- 说明这是艰难的决定
- 强调对团队的情感
- 保持情感连接，表达希望以后保持联系
"""
        elif self.boss_profile.mbti in ["ISTJ", "ISFJ", "ESTJ", "ESFJ"]:
            qa_guide += """
- 详细说明交接计划
- 强调会完成所有承诺的工作
- 展现对责任的重视
- 提供具体的交接时间表
"""
        else:
            qa_guide += """
- 坦诚但专业地表达
- 准备多个理由备选
- 保持积极正面的态度
- 强调未来合作的可能性
"""
        
        qa_guide += """
### 通用技巧
- 保持冷静和自信
- 不要抱怨或批评
- 强调积极的原因（追求新机会，而非逃避现状）
- 准备好书面交接清单
- 表达愿意协助平稳过渡

## 禁忌
- ❌ 不要说公司/同事的坏话
- ❌ 不要表现得过于兴奋（显得迫不及待要走）
- ❌ 不要撒谎（容易被识破）
- ❌ 不要情绪化或对抗
- ❌ 不要透露新公司的敏感信息

## 最后提醒
- 提前准备好书面离职申请
- 想好最后工作日（通常提前30天）
- 整理好交接清单
- 保持职业素养，好聚好散
"""
        
        return qa_guide
    
    def get_reason_options(self) -> List[Dict]:
        """获取离职理由选项列表"""
        
        options = [
            {
                "category": "职业发展",
                "reasons": [
                    {"key": "CAREER_GROWTH", "label": "个人职业发展规划", "description": "寻求更大的发展空间"},
                    {"key": "NEW_OPPORTUNITY", "label": "新的职业机会", "description": "收到了更好的offer"},
                    {"key": "STARTUP", "label": "创业", "description": "想自己创业试试"},
                    {"key": "INDUSTRY_CHANGE", "label": "行业转型", "description": "想换个行业发展"},
                    {"key": "STUDY", "label": "继续深造", "description": "读书/考证/学习新技能"},
                ]
            },
            {
                "category": "个人原因",
                "reasons": [
                    {"key": "FAMILY", "label": "家庭原因", "description": "需要照顾家人/家庭计划"},
                    {"key": "HEALTH", "label": "健康原因", "description": "身体不适，需要休养"},
                    {"key": "BURNOUT", "label": "职业倦怠", "description": "需要休息调整"},
                    {"key": "WORK_LIFE_BALANCE", "label": "工作生活平衡", "description": "想要更多个人时间"},
                    {"key": "RELOCATION", "label": "搬家/relocate", "description": "搬到其他城市"},
                ]
            },
            {
                "category": "客观原因",
                "reasons": [
                    {"key": "CONTRACT_END", "label": "合同到期", "description": "合同到期不续签"},
                    {"key": "COMPANY_CHANGE", "label": "公司调整", "description": "部门变动/裁员等"},
                    {"key": "PROJECT_END", "label": "项目结束", "description": "项目完结"},
                ]
            },
            {
                "category": "其他",
                "reasons": [
                    {"key": "OTHER", "label": "其他个人原因", "description": "不想细说的原因"},
                ]
            }
        ]
        
        return options


def generate_resignation_speech(
    boss_name: str,
    boss_gender: str,
    boss_age: str,
    boss_mbti: str,
    reason_key: str,
    last_day: str = "30天后",
    **kwargs
) -> Dict[str, str]:
    """
    便捷的离职话术生成函数
    
    使用示例:
    ```python
    result = generate_resignation_speech(
        boss_name="王",
        boss_gender="男",
        boss_age="40-50",
        boss_mbti="ENTJ",
        reason_key="NEW_OPPORTUNITY",
        last_day="4月30日"
    )
    ```
    """
    
    # 创建老板画像
    profile = BossProfile(
        name=boss_name,
        gender=boss_gender,
        age_range=boss_age,
        mbti=boss_mbti,
        personality_traits=kwargs.get("personality_traits", []),
        communication_style=kwargs.get("communication_style", "直接"),
        values=kwargs.get("values", ["效率", "结果"]),
        relationship=kwargs.get("relationship", "一般")
    )
    
    # 解析 reason_key
    try:
        reason = ResignationReason[reason_key]
    except KeyError:
        reason = ResignationReason.CAREER_GROWTH
    
    # 生成话术
    generator = ResignationSpeechGenerator()
    generator.set_profile(profile)
    
    speeches = generator.generate_speech(reason, last_day)
    
    # 添加 Q&A 指南
    speeches["_qa_guide"] = generator.generate_qa_guide()
    speeches["_reason_options"] = generator.get_reason_options()
    
    return speeches


if __name__ == "__main__":
    # 示例用法
    result = generate_resignation_speech(
        boss_name="张",
        boss_gender="男",
        boss_age="40-50",
        boss_mbti="ENTJ",
        reason_key="NEW_OPPORTUNITY",
        last_day="2026年4月30日",
        relationship="一般"
    )
    
    print("=== 正式版 ===")
    print(result["正式版"])
    print("\n=== 微信版 ===")
    print(result["微信/钉钉版"])
