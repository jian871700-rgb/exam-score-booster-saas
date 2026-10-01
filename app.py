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

# 自定义样式
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; font-size: 16px; font-weight: 600; }
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

# 未登录时拦截
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
    st.error("⚠️ 未检测到 DEEPSEEK_API_KEY！请在 Streamlit Cloud Settings -> Secrets 中配置。")
    st.stop()

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# 保持结果持久化
if "xhs_result" not in st.session_state:
    st.session_state.xhs_result = ""
if "diag_result" not in st.session_state:
    st.session_state.diag_result = ""

# --- 侧边栏 ---
with st.sidebar:
    st.title("⚙️ 工作台控制中心")
    st.markdown("---")
    
    selected_model = st.selectbox(
        "选择 AI 大模型：",
        ["deepseek-chat", "deepseek-reasoner"],
        index=0,
        help="deepseek-chat 适合文案；deepseek-reasoner 适合复杂诊断分析"
    )
    
    temperature = st.slider(
        "创意发散度 (Temperature)：",
        min_value=0.0,
        max_value=1.0,
        value=0.70,
        step=0.05
    )
    
    st.markdown("---")
    st.markdown("📌 **中高考卷面提分项目组**")
    st.caption("💡 核心产品：980元/6小时 提分实操课")
    st.caption("🎁 引流钩子：《2025答题卡1:1速练字帖》")
    
    st.markdown("---")
    if st.button("🚪 退出登录", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# --- 主界面 ---
st.title("🎯 中高考卷面提分 · 营销与转化工作台")

tab1, tab2 = st.tabs(["📝 引流文案爆款工厂", "🔍 试卷深度诊断与转化报告"])

# ==================== Tab 1 ====================
with tab1:
    st.subheader("📝 小红书/视频号 爆款矩阵文案生成器")
    
    col1, col2 = st.columns(2)
    with col1:
        grade_subject = st.text_input("年级与学科：", value="初三/高三 英语、语文及文综", key="xhs_grade")
        magnet_name = st.text_input("引流资料名称：", value="《2025中高考标准答题卡1:1速练电子字帖》PDF", key="xhs_magnet")
    with col2:
        pain_points = st.text_input("痛点关键词：", value="卷面潦草、踩分点被扣、客观题满分主观题扣冤枉分、写字慢", key="xhs_pains")
        target_audience = st.text_input("目标受众群体：", value="初三/高三焦虑家长、提分遇到瓶颈的考生", key="xhs_target")
    
    if st.button("🚀 立即生成爆款引流文案", type="primary", use_container_width=True, key="btn_gen_xhs"):
        sys_p = "你是一位精通中高考卷面提分的内容操盘手。请写一篇小红书爆款文案，包含：1. 3组爆款标题；2. 黄金前3秒正文；3. 痛点剖析与提分逻辑；4. 评论区领资料钩子(CTA)；5. 5-8个精准标签。"
        user_p = f"年级学科：{grade_subject}\n引流资料：{magnet_name}\n核心痛点：{pain_points}\n目标受众：{target_audience}"
        
        with st.spinner("AI 正在深度构思爆款文案..."):
            try:
                res = client.chat.completions.create(
                    model=selected_model,
                    messages=[
                        {"role": "system", "content": sys_p},
                        {"role": "user", "content": user_p}
                    ],
                    temperature=temperature
                )
                st.session_state.xhs_result = res.choices[0].message.content
                st.success("🎉 爆款文案生成成功！")
            except Exception as e:
                st.error(f"生成失败：{str(e)}")

    if st.session_state.xhs_result:
        st.markdown("### 📄 文案生成结果")
        st.markdown(st.session_state.xhs_result)
        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.download_button(
                "📥 下载文案为 Markdown (.md)",
                st.session_state.xhs_result,
                file_name=f"xhs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        with c2:
            st.download_button(
                "📥 下载文案为 文本文件 (.txt)",
                st.session_state.xhs_result,
                file_name=f"xhs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )

# ==================== Tab 2 ====================
with tab2:
    st.subheader("🔍 学员专属《卷面深度诊断与提分规划书》")
    
    col_a, col_b = st.columns(2)
    with col_a:
        student_name = st.text_input("学员称谓/姓名：", value="张同学", key="diag_stu")
        teacher_name = st.text_input("诊断主考/指导老师：", value="卷面提分教研组", key="diag_teacher")
    with col_b:
        subject_score = st.text_input("诊断科目与目前分数：", value="初三中考英语（目前 92分/满分 120）", key="diag_score")
        target_score = st.text_input("期望目标分数：", value="105分以上（卷面挽回 8-12分）", key="diag_target")
    
    paper_issues = st.text_area(
        "试卷卷面典型问题描述：",
        value="1. 英语书写字母倾斜角度不一致；\n2. 答题区域涂改严重；\n3. 电脑扫描后整体发灰，阅卷老师易漏看采分点；\n4. 书写速度偏慢。",
        height=100,
        key="diag_issues"
    )
    
    if st.button("📑 一键生成学员专属诊断报告", type="primary", use_container_width=True, key="btn_gen_diag"):
        sys_diag = "你是一位中高考阅卷专家。请生成《卷面深度诊断与提分规划书》，严格包含四大模块：一、试卷扫描成像定性诊断；二、卷面隐形丢分精准测算；三、6小时卷面抢分通关方案；四、高情商推介980元/6小时课程的私域转化话术。"
        user_diag = f"学员：{student_name}\n老师：{teacher_name}\n科目与分数：{subject_score}\n目标：{target_score}\n卷面问题：{paper_issues}"
        
        with st.spinner("专家正在测算与编写诊断报告..."):
            try:
                res = client.chat.completions.create(
                    model=selected_model,
                    messages=[
                        {"role": "system", "content": sys_diag},
                        {"role": "user", "content": user_diag}
                    ],
                    temperature=0.3
                )
                st.session_state.diag_result = res.choices[0].message.content
