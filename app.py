import streamlit as st
from openai import OpenAI
import os
from datetime import datetime
from dotenv import load_dotenv

# 加载本地环境变量
load_dotenv()

# --- 页面基本配置 ---
st.set_page_config(
    page_title="中高考卷面提分 AI 商业工作台",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义部分样式
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        font-size: 16px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# --- 密码门禁配置 ---
AUTHORIZED_KEYS = ["exam2025", "vip888", "teacher999"]

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def check_password():
    input_key = st.session_state.get("password_input", "").strip()
    if input_key in AUTHORIZED_KEYS:
        st.session_state.authenticated = True
        if "login_error" in st.session_state:
            del st.session_state["login_error"]
    else:
        st.session_state.login_error = "❌ 访问密钥无效，请联系管理员获取授权！"

# 未登录时展示登录界面
if not st.session_state.authenticated:
    st.markdown("<h2 style='text-align: center; margin-top: 50px;'>🔐 中高考卷面提分项目 · 内部商业工作台</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>请输入专属授权密钥以进入系统</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.text_input("授权密钥 (Access Key)", type="password", key="password_input", on_change=check_password)
        if st.button("🚀 验证并进入工作台", use_container_width=True):
            check_password()
            st.rerun()
        if "login_error" in st.session_state:
            st.error(st.session_state.login_error)
    st.stop()

# --- 获取 API Key 并初始化客户端 ---
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["DEEPSEEK_API_KEY"]
    except Exception:
        pass

if not api_key:
    st.error("⚠️ 未检测到 DEEPSEEK_API_KEY！请在 Streamlit Cloud Settings -> Secrets 或本地 .env 中配置。")
    st.stop()

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# --- 初始化状态持久化变量 ---
if "xhs_result" not in st.session_state:
    st.session_state.xhs_result = ""
if "diag_result" not in st.session_state:
    st.session_state.diag_result = ""

# --- 侧边栏配置 ---
with st.sidebar:
    st.title("⚙️ 工作台控制中心")
    st.markdown("---")
    
    st.subheader("🎯 模型与参数")
    selected_model = st.selectbox(
        "选择 AI 大模型：",
        ["deepseek-chat", "deepseek-reasoner"],
        index=0,
        help="deepseek-chat: 响应迅速，适合爆款文案；deepseek-reasoner: 深度思考，适合高难度诊断报告"
    )
    
    temperature = st.slider(
        "创意发散度 (Temperature)：",
        min_value=0.0,
        max_value=1.0,
        value=0.70,
        step=0.05,
        help="数值越高文案越生动有创意，数值越低分析越严谨聚焦"
    )
    
    st.markdown("---")
    st.markdown("📌 **中高考卷面提分项目组**")
    st.caption("💡 核心产品：980元/6小时 提分实操课")
    st.caption("🎁 引流钩子：《2025中高考答题卡1:1速练字帖》")
    
    st.markdown("---")
    if st.button("🚪 退出登录", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# --- 主界面标题 ---
st.title("🎯 中高考卷面提分 · 营销与转化工作台")
st.markdown("🎯 **一键生成小红书/视频号引流矩阵文案** ｜ **智能生成 980 元私域卷面诊断报告**")

tab1, tab2 = st.tabs(["📝 引流文案爆款工厂", "🔍 试卷深度诊断与转化报告"])

# ==================== Tab 1: 引流文案爆款工厂 ====================
with tab1:
    st.subheader("📝 小红书/视频号 爆款矩阵文案生成器")
    st.caption("基于 CRISPE 框架，专为中高考卷面提分课程定制爆款流量钩子")
    
    col1, col2 = st.columns(2)
    with col1:
        grade_subject = st.text_input("年级与学科：", value="初三/高三 英语、语文及文综", key="xhs_grade")
        magnet_name = st.text_input("引流资料名称（免费钩子）：", value="《2025中高考标准答题卡1:1速练电子字帖》PDF", key="xhs_magnet")
    
    with col2:
        pain_points = st.text_input("痛点关键词：", value="卷面潦草、踩分点被扣、客观题满分主观题扣冤枉分、写字慢答不完卷", key="xhs_pains")
        target_audience = st.text_input("目标受众群体：", value="初三/高三焦虑家长、提分遇到瓶颈的考生", key="xhs_target")
    
    if st.button("🚀 立即生成爆款引流文案", type="primary", use_container_width=True, key="btn_gen_xhs"):
        system_prompt = (
            "你是一位深谙小红书和视频号算法的教育赛道顶级内容操盘手，精通中高考卷面书写提分与私域转化技巧。\n"
            "请根据用户提供的学科痛点与引流资料，撰写一篇高点击率、强互动、极具说服力的小红书爆款图文文案。\n\n"
            "【输出结构必须包含】：\n"
            "1. 【3组高点击率爆款标题】（包含数字、痛点刺激、制造反差与紧迫感，带吸睛 Emoji）\n"
            "2. 【黄金前3秒吸睛正文】（直击家长痛点，指出答题卡扫描后丢分的残酷现实）\n"
            "3. 【深度痛点剖析与提分逻辑】（解释为什么6小时专项训练卷面能多拿10-15分）\n"
            "4. 【超强评论区引流钩子与行动指令 (CTA)】（引导评论区留言领资料，如'扣【字帖】领取'）\n"
            "5. 【5-8个高流量精准话题标签 (Tags)】"
        )
        user_prompt = f"年级学科：{grade_subject}\n引流资料：{magnet_name}\n核心痛点：{pain_points}\n目标受众：{target_audience}"
        
        with st.spinner("AI 正在深度构思爆款文案，请稍候..."):
            try:
                response = client.chat.completions.create(
                    model=selected_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=temperature
                )
                st.session_state.xhs_result = response.choices[0].message.content
                st.success("🎉 爆款文案生成成功！")
            except Exception as e:
                st.error(f"生成失败：{str(e)}")

    if st.session_state.xhs_result:
        st.markdown("### 📄 文案生成结果")
        st.markdown(st.session_state.xhs_result)
        
        st.markdown("---")
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.download_button(
                label="📥 下载文案为 Markdown (.md)",
                data=str(st.session_state.xhs_result),
                file_name=f"xhs_copy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        with col_d2:
            st.download_button(
                label="📥 下载文案为 文本文件 (.txt)",
                data=str(st.session_state.xhs_result),
                file_name=f"xhs_copy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )

# ==================== Tab 2: 试卷深度诊断与转化报告 ====================
with tab2:
    st.subheader("🔍 学员专属《卷面深度诊断与提分规划书》")
    st.caption("为私域家长量身定制专业诊断分析，自然推介 980元/6小时 提分课程")
    
    col_a, col_b = st.columns(2)
    with col_a:
        student_name = st.text_input("学员称谓/姓名：", value="张同学", key="diag_stu")
        teacher_name = st.text_input("诊断主考/指导老师：", value="卷面提分教研组", key="diag_teacher")
    
    with col_b:
        subject_score = st.text_input("诊断科目与目前分数：", value="初三中考英语（目前 92分/满分 120）", key="diag_score")
        target_score = st.text_input("期望目标分数：", value="105分以上（卷面挽回 8-12分）", key="diag_target")
    
    paper_issues = st.text_area(
        "试卷卷面典型问题描述（越详细报告越专业）：",
        value="1. 英语书写字母倾斜角度不一致，无四线三格基准意识；\n2. 答题区域涂改严重，作文段落间距拥挤；\n3. 电脑扫描后整体发灰发黑，阅卷老师极易漏看关键采分点词汇；\n4. 书写速度偏慢，考场后半段作文仓促收尾。",
        height=120,
        key="diag_issues"
    )
    
    if st.button("📑 一键生成学员专属诊断报告", type="primary", use_container_width=True, key="btn_gen_diag"):
        sys_prompt_diag = (
            "你是一位拥有15年中高考阅卷与提分经验的资深专家。\n"
            "请根据家长/学员提供的卷面书写问题，生成一份极具专业度、权威感和温度感的《卷面深度诊断与提分规划书》。\n\n"
            "【输出结构必须严格
