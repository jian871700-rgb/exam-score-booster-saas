import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# ==================== 1. 页面基础配置 ====================
st.set_page_config(
    page_title="中高考卷面提分 | AI 商业交付工作台",
    page_icon="📝",
    layout="wide"
)

# ==================== 2. 安全访问门禁 ====================
def check_password():
    """密码验证逻辑"""
    def password_entered():
        if st.session_state["password_input"] == "exam2025":
            st.session_state["password_correct"] = True
            del st.session_state["password_input"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.write("")
        st.write("")
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            st.markdown("<h2 style='text-align: center;'>🔒 内部系统访问授权</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: gray;'>中高考卷面提分项目 · 内部自动化交付与运营工作台</p>", unsafe_allow_html=True)
            st.text_input("请输入访问授权码：", type="password", on_change=password_entered, key="password_input")
        return False
    elif not st.session_state["password_correct"]:
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            st.markdown("<h2 style='text-align: center;'>🔒 内部系统访问授权</h2>", unsafe_allow_html=True)
            st.text_input("请输入访问授权码：", type="password", on_change=password_entered, key="password_input")
            st.error("❌ 授权码错误，请联系项目负责人获取权限")
        return False
    else:
        return True

# 拦截未登录用户
if not check_password():
    st.stop()

# ==================== 3. 登录成功后的主工作台 ====================

# 初始化 DeepSeek 客户端
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    st.error("⚠️ 未检测到 DEEPSEEK_API_KEY 环境变量，请在 .env 文件中配置！")
    st.stop()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# ==================== 4. 侧边栏配置 ====================
with st.sidebar:
    st.title("⚙️ 控制面板")
    
    st.subheader("🤖 模型配置")
    selected_model = st.selectbox(
        "选择推理模型",
        options=["deepseek-chat", "deepseek-reasoner"],
        index=0,
        help="deepseek-chat 适合文案生成与快速问答；deepseek-reasoner 适合深度逻辑推理。"
    )
    
    temperature = st.slider(
        "创意度 (Temperature)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.05
    )
    
    st.markdown("---")
    st.subheader("🎯 商业交付链路备忘")
    st.markdown("""
    - **前端引流**：小红书/视频号矩阵内容
    - **引流钩子**：《2025中高考答题卡1:1速练字帖PDF》
    - **私域转化**：试卷卷面阅卷官视角诊断
    - **成交产品**：980元/6小时卷面提分特训课
    """)
    
    st.markdown("---")
    if st.button("🚪 退出登录"):
        st.session_state["password_correct"] = False
        st.rerun()

# ==================== 5. 主工作区 ====================
st.title("📝 中高考卷面提分 | AI 自动化运营与转化工作台")
st.markdown("为中高考卷面提分项目定制的全流程商业交付系统：支持**小红书爆款文案生产**与**私域试卷诊断转化话术**。")

tab1, tab2 = st.tabs(["🔥 小红书爆款文案生成", "🔍 试卷卷面诊断与私域转化"])

# ----------------- Tab 1: 小红书文案 -----------------
with tab1:
    st.header("小红书爆款提分笔记生成器")
    
    col_a, col_b = st.columns(2)
    with col_a:
        grade_subject = st.text_input("年级与学科", value="初三/高三 语文与文综", key="xhs_grade")
        lead_magnet = st.text_input("引流钩子（资料名称）", value="《2025中高考答题卡1:1速练字帖PDF》", key="xhs_hook")
    with col_b:
        pain_points = st.text_area(
            "核心痛点描述", 
            value="字迹潦草被扣冤枉分、文综答题超出格子被扫描切边、行间距太挤老师看不清给起评分", 
            height=100, 
            key="xhs_pain"
        )
    
    if st.button("🚀 一键生成小红书爆款文案", type="primary", key="btn_xhs"):
        xhs_prompt = f"""
你是一名专注于小红书教育赛道（中高考提分/书写规范）的百万博主与转化文案大师。
请基于以下信息，写一篇能引发家长和初高中生强烈共鸣、具备高互动与强引流属性的小红书爆款笔记。

【输入信息】：
- 年级与学科：{grade_subject}
- 核心痛点：{pain_points}
- 免费钩子资料：{lead_magnet}

【输出格式与结构规范】：
1. 爆款标题库（提供3个不同维度的标题：痛点悬念型、阅卷内幕型、直观提分型，必须带合适Emoji）
2. 笔记正文：
   - 黄金前3秒抓人开场（还原阅卷现场/打破认知）
   - 痛点场景还原（字迹差、超格、扫描模糊导致的隐形失分）
   - 核心提分认知（阅卷老师的心理与给分习惯、标准化卷面排版3大原则）
   - 互动与评论区埋雷（引导家长在评论区留言）
3. 私域引流钩子话术（自然引导私信领取资料）
4. 推荐热门标签（#高考冲刺 #中考提分 #卷面书写规范 等）
"""
        st.markdown("### 📝 生成结果：")
        output_placeholder = st.empty()
        
        try:
            stream_kwargs = {
                "model": selected_model,
                "messages": [{"role": "user", "content": xhs_prompt}],
                "stream": True
            }
            if selected_model != "deepseek-reasoner":
                stream_kwargs["temperature"] = temperature
                
            response = client.chat.completions.create(**stream_kwargs)
            
            def stream_generator():
                for chunk in response:
                    content = chunk.choices[0].delta.content
                    if content:
                        yield content
            
            output_placeholder.write_stream(stream_generator())
            st.success("✅ 文案生成完毕！")
        except Exception as e:
            st.error(f"❌ 生成失败，错误信息: {e}")

# ----------------- Tab 2: 诊断与转化话术 -----------------
with tab2:
    st.header("私域阅卷官视角卷面诊断与 980 元课程转化话术")
    
    col_c, col_d = st.columns(2)
    with col_c:
        student_issues = st.text_area(
            "学生试卷卷面问题描述",
            value="高三文综大题字迹偏小且歪斜，主观题答题未分点，答案紧贴边框导致扫描后边缘字迹模糊，估算扣分在8-12分。",
            height=120,
            key="diag_issues"
        )
    with col_d:
        target_score = st.text_input("目标提升分数 / 冲刺目标", value="高考文综主观题挽回 10-15 分卷面分", key="diag_target")
        course_name = st.text_input("转化课程名称与价格", value="《980元/6小时中高考卷面提分特训课》", key="diag_course")
        
    if st.button("📊 一键生成阅卷官诊断报告与转化话术", type="primary", key="btn_diag"):
        diag_prompt = f"""
你是一名有10年中高考阅卷经验的高级阅卷组长，同时精通私域高客单价教育课程转化心理学。
请针对以下学生的卷面问题，生成一份专业、客观、击中痛点的【卷面诊断报告】以及配套的【微信私域一对一高情商转化话术】。

【学员情况】：
- 卷面问题：{student_issues}
- 提分目标：{target_score}
- 推荐课程：{course_name}

【请按以下4个模块严格输出】：
### 模块一：【阅卷官视角的卷面定性诊断】
（用阅卷老师第一视角的严谨语气，列出2-3个致命失分习惯）

### 模块二：【隐形失分账单测算】
（客观测算因为卷面印象分、扫描模糊、关键踩分点被淹没导致的隐形丢分，量化到具体分值）

### 模块三：【针对性抢救方案（3步走）】
（给出标准化书写与排版矫正的具体落地步骤）

### 模块四：【私域高情商转化与推课话术（微信直接发送给家长）】
（语气真诚、不强买强卖、站在帮孩子守住分数线的角度，自然引出 980 元/6小时特训课的必要性与紧迫性）
"""
        st.markdown("### 📋 诊断报告与转化话术：")
        output_placeholder2 = st.empty()
        
        try:
            stream_kwargs = {
                "model": selected_model,
                "messages": [{"role": "user", "content": diag_prompt}],
                "stream": True
            }
            if selected_model != "deepseek-reasoner":
                stream_kwargs["temperature"] = temperature
                
            response = client.chat.completions.create(**stream_kwargs)
            
            def stream_generator2():
                for chunk in response:
                    content = chunk.choices[0].delta.content
                    if content:
                        yield content
            
            output_placeholder2.write_stream(stream_generator2())
            st.success("✅ 诊断报告与转化话术已生成完毕！")
        except Exception as e:
            st.error(f"❌ 生成失败，错误信息: {e}")
