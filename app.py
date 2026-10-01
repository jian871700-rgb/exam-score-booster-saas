import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
import datetime

# 加载本地 .env 文件（如果在云端，则优先从 st.secrets 读取）
load_dotenv()

# ==================== 页面全局配置 ====================
st.set_page_config(
    page_title="中高考卷面提分·AI 商业获客与诊断工作台 v2.0",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 授权密码保护机制 ====================
# 支持多组授权码（方便给不同老师或自己使用）
AUTHORIZED_KEYS = ["exam2025", "vip888", "teacher999"]

def check_password():
    """验证用户输入的授权码"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.title("🎓 中高考卷面提分 · 智能工作台 v2.0")
        st.markdown("##### 🔒 本系统为内部商业交付系统，请输入专属授权码进入")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            pwd = st.text_input("请输入授权码：", type="password", key="password_input")
        with col2:
            st.write("")
            st.write("")
            btn = st.button("🔑 验证进入", use_container_width=True)
            
        if btn:
            if pwd in AUTHORIZED_KEYS:
                st.session_state.authenticated = True
                st.success("✅ 验证成功，正在加载系统...")
                st.rerun()
            else:
                st.error("❌ 授权码无效，请联系管理员获取！")
        return False
    return True

if not check_password():
    st.stop()

# ==================== 初始化 API 客户端 ====================
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key and "DEEPSEEK_API_KEY" in st.secrets:
    api_key = st.secrets["DEEPSEEK_API_KEY"]

if not api_key:
    st.error("⚠️ 未检测到 DEEPSEEK_API_KEY，请检查环境变量或云端 Secrets 配置。")
    st.stop()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# 初始化 Session State 缓存生成结果
if "xhs_result" not in st.session_state:
    st.session_state.xhs_result = ""
if "diagnosis_result" not in st.session_state:
    st.session_state.diagnosis_result = ""

# ==================== 侧边栏：系统控制中心 ====================
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/education.png", width=120)
    st.title("⚙️ 工作台控制中心")
    st.markdown("---")
    
    st.subheader("🤖 模型与参数")
    model_choice = st.selectbox(
        "选择 AI 大模型：",
        ["deepseek-chat", "deepseek-reasoner"],
        index=0,
        help="deepseek-chat 适合爆款文案快速生成；deepseek-reasoner (R1) 适合深度试卷逻辑诊断"
    )
    
    temperature = st.slider(
        "创意发散度 (Temperature)：",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.05,
        help="文案建议 0.7~0.85，精准诊断建议 0.2~0.4"
    )
    
    st.markdown("---")
    st.caption("📌 **中高考卷面提分项目组**")
    st.caption("💡 核心产品：980元/6小时 提分实操课")
    
    if st.button("🚪 退出登录"):
        st.session_state.authenticated = False
        st.session_state.xhs_result = ""
        st.session_state.diagnosis_result = ""
        st.rerun()

# ==================== 核心主操作界面 ====================
st.title("🎓 中高考卷面提分 · AI 商业工作台 v2.0")
st.markdown("🎯 **一键生成小红书/视频号引流矩阵文案 ｜ 智能生成 980 元私域卷面诊断报告**")

tab1, tab2 = st.tabs(["📝 引流文案爆款工厂", "🔍 试卷深度诊断与转化报告"])

# ----------------- Tab 1: 小红书引流文案 -----------------
with tab1:
    st.subheader("📌 小红书/视频号 爆款获客文案生成器")
    
    c1, c2 = st.columns(2)
    with c1:
        grade_subject = st.text_input("📚 年级与学科", value="初三英语", placeholder="例如：高二语文、初三数学")
        lead_magnet = st.text_input("🎁 引流钩子（免费资料）", value="《中考英语答题卡 1:1 规范字帖 PDF》", placeholder="例如：阅卷避坑清单")
    with c2:
        pain_point = st.text_input("💥 卷面核心痛点", value="字迹潦草重叠、作文涂改严重被判卷老师扣冤枉分", placeholder="例如：解答题步骤挤在一起")
        target_audience = st.selectbox("🎯 目标受众画像", ["初三/高三 焦虑家长", "平时成绩不错但卷面扣分的学生", "临考冲刺冲刺重点中学的家庭"])
    
    if st.button("🚀 一键生成爆款引流文案", type="primary", use_container_width=True):
        prompt = f"""
你是一位深谙小红书与教育私域转化的千万级操盘手，专门为“980元/6小时中高考卷面提分课”撰写引流文案。
请根据以下信息，生成一篇符合小红书爆款逻辑的文案：

【基本信息】
- 年级学科：{grade_subject}
- 核心痛点：{pain_point}
- 引流钩子：{lead_magnet}
- 目标受众：{target_audience}

【文案结构要求】
1. 3个具有强烈点击欲的爆款标题（痛点型、反常识型、结果呈现型，带 Emoji）。
2. 黄金 3 秒痛点 Hook 开头（还原阅卷现场的残酷扣分细节）。
3. 正文内容：用真实阅卷老师视角，分析卷面潦草为什么在电子阅卷中会被“系统降级”，并给出 2 个立竿见影的卷面急救技巧。
4. 强引导留资钩子（CTA）：引导家长在评论区回复关键词领取【{lead_magnet}】。
5. 包含 5-8 个热门标签话题（带#）。
"""
        with st.spinner("AI 正在深度构思爆款文案..."):
            response = client.chat.completions.create(
                model=model_choice,
                messages=[
                    {"role": "system", "content": "你是一位顶级教育爆款文案专家与私域流量操盘手。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                stream=False
            )
            st.session_state.xhs_result = response.choices[0].message.content

    # 展示与导出区域
    if st.session_state.xhs_result:
        st.markdown("### 📄 生成结果展示：")
        st.markdown(st.session_state.xhs_result)
        
        st.markdown("---")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            st.download_button(
                label="📥 下载文案为 Markdown (.md)",
                data=st.session_state.xhs_result,
                file_name=f"小红书文案_{grade_subject}_{datetime.datetime.now().strftime('%m%d_%H%M')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        with col_btn2:
            st.download_button(
                label="📥 下载文案为 文本文件 (.txt)",
                data=st.session_state.xhs_result,
                file_name=f"小红书文案_{grade_subject}_{datetime.datetime.now().strftime('%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True
            )

# ----------------- Tab 2: 卷面诊断与转化报告 -----------------
with tab2:
    st.subheader("🔍 学员专属《卷面深度诊断与提分规划书》")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        student_name = st.text_input("👤 学员称谓/姓名", value="张同学", placeholder="如：李同学、初三王家长")
        teacher_name = st.text_input("👨‍🏫 诊断主考/指导老师", value="卷面提分教研组", placeholder="如：王老师")
    with col_t2:
        subject_info = st.text_input("📝 诊断科目与目前分数", value="初三中考英语（目前 92 分/满分 120）")
        target_score = st.text_input("🎯 期望目标分数", value="105 分以上（卷面挽回 8-12 分）")
    
    student_issues = st.text_area(
        "⚠️ 学员卷面具体扣分与现状描述",
        value="英语作文涂改严重，字母大小不一，斜度不一致。阅读理解答题卡填涂过轻，经常被扫描仪识别为模糊。主观题答题区域超出边框。",
        rows=3
    )

    if st.button("📊 一键生成专属诊断报告与 980 元转化话术", type="primary", use_container_width=True):
        diag_prompt = f"""
你是一位拥有15年中高考阅卷组长经验的卷面提分专家。请根据以下学员情况，生成一份极具专业度和说服力的【卷面深度诊断与提分规划书】：

【学员信息】
- 学员姓名：{student_name}
- 诊断指导：{teacher_name}
- 科目与现状：{subject_info}
- 目标分数：{target_score}
- 卷面问题：{student_issues}

【报告输出格式规范】
# 🎓【中高考卷面提分专题】学员专属卷面诊断与提分规划书
**学员档案**：{student_name} | **诊断科目**：{subject_info} | **诊断专家**：{teacher_name} | **生成日期**：{datetime.date.today()}

---
### 一、 电子阅卷光学扫描定性诊断（扣分真相剖析）
（从扫描仪成像、阅卷老师 3-5 秒定档评分心理学角度，精准定性 3 项致命卷面扣分点）

### 二、 隐形扣分量化评估表
（列出当前卷面在“客观题填涂规范”、“主观题版面布局”、“字迹工整度”三个维度的具体流失分数预估，总计流失分数值）

### 三、 专属提分改善方案（三阶抢分法）
- **第一阶段（1-2天）**：修正运笔角度与字间距，建立基准线意识。
- **第二阶段（3-4天）**：专攻答题卡边框边界控制与答题黄金排版法。
- **第三阶段（5-6天）**：高频答题模板肌肉记忆实操，实现快速书写不走样。

### 四、 私域专家高情商转化沟通话术（直接微信发给家长）
（撰写一段既体现权威关怀、不引起焦虑，又自然承接【980元/6小时中高考卷面提分实操课】的高转化微信沟通话术）
"""
        with st.spinner("专家教研模型正在深度分析卷面病灶..."):
            diag_response = client.chat.completions.create(
                model=model_choice,
                messages=[
                    {"role": "system", "content": "你是一位兼具严谨中高考阅卷经验与家庭教育深度沟通能力的专家。"},
                    {"role": "user", "content": diag_prompt}
                ],
                temperature=0.3,
                stream=False
            )
            st.session_state.diagnosis_result = diag_response.choices[0].message.content

    # 展示与导出区域
    if st.session_state.diagnosis_result:
        st.markdown("### 📋 专属报告预览：")
        st.markdown(st.session_state.diagnosis_result)
        
        st.markdown("---")
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.download_button(
                label=f"📥 导出为《{student_name}_卷面诊断报告.md》",
                data=st.session_state.diagnosis_result,
                file_name=f"{student_name}_卷面深度诊断报告_{datetime.datetime.now().strftime('%m%d')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        with col_d2:
            st.download_button(
                label=f"📥 导出为《{student_name}_卷面诊断报告.txt》",
                data=st.session_state.diagnosis_result,
                file_name=f"{student_name}_卷面深度诊断报告_{datetime.datetime.now().strftime('%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
