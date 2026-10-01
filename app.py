import streamlit as st
from openai import OpenAI
import datetime

# 页面基础配置
st.set_page_config(
    page_title="中高考卷面提分 · 全链路商业增长中台",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 注入样式
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        border-left: 4px solid #ff4b4b;
        margin-bottom: 15px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        font-weight: 600;
        font-size: 15px;
    }
</style>
""", unsafe_allow_html=True)

# 授权密钥列表
AUTHORIZED_KEYS = ["exam2025", "vip888", "teacher999"]

# 初始化 Session State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "xhs_result" not in st.session_state:
    st.session_state.xhs_result = ""
if "diag_result" not in st.session_state:
    st.session_state.diag_result = ""
if "wechat_result" not in st.session_state:
    st.session_state.wechat_result = ""

# 登录验证函数
def check_password():
    if not st.session_state.authenticated:
        st.markdown("<h2 style='text-align: center;'>🔐 中高考卷面提分 · 数字化教研转化系统</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>请输入专属授权访问码以进入工作台</p>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            key_input = st.text_input("授权访问码 (Access Key)", type="password", placeholder="请输入密钥")
            if st.button("🚀 验证并进入工作台", use_container_width=True):
                if key_input.strip() in AUTHORIZED_KEYS:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("❌ 授权码无效或已过期，请联系管理员获取！")
        return False
    return True

if not check_password():
    st.stop()

# 获取 API Key
api_key = st.secrets.get("DEEPSEEK_API_KEY")
if not api_key:
    st.error("⚠️ 未检测到 DEEPSEEK_API_KEY，请在 Streamlit Secrets 中配置！")
    st.stop()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# 侧边栏配置
with st.sidebar:
    st.title("⚙️ 引擎与控制中心")
    st.markdown("---")
    model_choice = st.selectbox(
        "🧠 核心推理模型",
        ["deepseek-chat", "deepseek-reasoner"],
        index=0,
        help="deepseek-chat 适合爆款文案快速生成；deepseek-reasoner 适合复杂学情逻辑与私域攻心拆解。"
    )
    temp_choice = st.slider(
        "🎛️ 逻辑创造度 (Temperature)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.05,
        help="文案与私域建议 0.6~0.8，学术诊断建议 0.2~0.4。"
    )
    st.markdown("---")
    st.markdown("### 📌 转化全链路导航")
    st.caption("1️⃣ **公域引流**：小红书合规干货笔记")
    st.caption("2️⃣ **私域承接**：微信 1对1 攻心与异议化解")
    st.caption("3️⃣ **诊断交付**：试卷卷面失分风险报告书")
    st.caption("4️⃣ **高客单成交**：980元/6小时极速提分营")
    st.markdown("---")
    if st.button("🚪 退出登录", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# 页面主标题
st.title("✍️ 中高考卷面提分 · 全链路商业增长中台")
st.caption("三大中枢：公域爆款引流工厂 | 私域微信高情商成交中枢 | 学员深度诊断规划报告")

tab1, tab2, tab3 = st.tabs([
    "📝 公域引流文案工厂 (小红书防限流版)", 
    "💬 微信私域转化与异议攻心专家",
    "📑 学员卷面诊断与高客单转化报告"
])

# ----------------- TAB 1: 小红书文案工厂 -----------------
with tab1:
    st.markdown("#### 🎯 批量生成高权重、防限流的小红书爆款笔记")
    
    col1, col2 = st.columns(2)
    with col1:
        grade_subject = st.selectbox("📌 目标学段/学科", ["初三中考英语", "高三高考语文", "初中全科通用", "高中全科通用"])
        target_audience = st.selectbox("👥 核心目标受众", ["焦虑初三/高三家长", "字迹潦草/常被扣分的学生", "总分卡在提分瓶颈期的考生"])
    with col2:
        lead_magnet = st.text_input("🎁 嵌入的信任钩子 (资料名)", value="2025中考答题卡1:1速成字帖PDF")
        core_pain = st.text_input("⚡ 核心戳痛点", value="平时做题都会，一到大考因字迹潦草被扣掉8-15分冤枉分")

    if st.button("🔥 立即生成小红书合规爆款文案", use_container_width=True, type="primary"):
        with st.spinner("🤖 正在结合小红书最新合规算法创作文案..."):
            prompt = f"""
你是一位深谙小红书2025最新推荐算法与违规风控机制的顶级教育运营操盘手。
请针对以下中高考卷面提分需求，创作一篇【绝对合规、防限流、高互动、去AI感】的小红书爆款图文文案。

【核心背景】：
- 学科与阶段：{grade_subject}
- 核心受众：{target_audience}
- 核心痛点：{core_pain}
- 引流物料：{lead_magnet}

【小红书平台防限流硬性规则】：
1. 严禁出现诱导互动词：绝对禁止出现“评论区扣XX发你”、“免费送”、“无偿领取”、“加微信/私信我”等任何索要互动的表述！
2. 合规结尾：文末只能使用【自然场景植入】或【启发式提问】，如：“之前带的学生都是用我自己整理的【{lead_magnet}】纠正的，在标准格子里写两周效果就出来了。大家平时英语作文卷面最容易在哪个细节扣分？”
3. 语言风格：必须第一人称“带了多年中高考班的XX老师”，真诚、专业、多用短句与小红书表情，杜绝AI机械感。

【文案输出格式】：
1. 3个高点击率爆款封面标题（带情绪标签与数字对比）
2. 3秒黄金抓人痛点开场
3. 卷面提分干货正文（分点排版）
4. 合规互动结尾（启发讨论/自然植入资料名）
5. 5-8个精准高流量小红书标签
"""
            try:
                response = client.chat.completions.create(
                    model=model_choice,
                    temperature=temp_choice,
                    messages=[{"role": "user", "content": prompt}]
                )
                st.session_state.xhs_result = response.choices[0].message.content
                st.success("✅ 爆款合规文案生成成功！")
            except Exception as e:
                st.error(f"❌ 生成失败: {str(e)}")

    if st.session_state.xhs_result:
        st.markdown("---")
        st.subheader("📋 生成结果预览与导出")
        st.markdown(st.session_state.xhs_result)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.download_button(
                label="📥 下载文案为 Markdown (.md)",
                data=st.session_state.xhs_result,
                file_name=f"XHS_Copy_{grade_subject}_{timestamp}.md",
                mime="text/markdown",
                use_container_width=True
            )
        with col_d2:
            st.download_button(
                label="📥 下载文案为纯文本 (.txt)",
                data=st.session_state.xhs_result,
                file_name=f"XHS_Copy_{grade_subject}_{timestamp}.txt",
                mime="text/plain",
                use_container_width=True
            )

# ----------------- TAB 2: 微信私域转化专家 -----------------
with tab2:
    st.markdown("#### 🎯 微信私域 1对1 沟通、高情商推课与异议化解专家")
    
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        wechat_stage = st.selectbox(
            "📍 当前微信沟通阶段",
            [
                "1. 加微信首接打招呼与交付资料（顺便要试卷）",
                "2. 收到家长试卷图后的【定性反馈与痛点放大】",
                "3. 正式推荐【980元/6小时卷面抢分实战课】",
                "4. 核心异议攻心化解（针对家长各种抗拒与犹豫）",
                "5. 家长已读不回 / 沉默超过24小时的【无压力二次激活】"
            ]
        )
        objection_type = st.selectbox(
            "⚡ 针对的家长核心顾虑/抗拒点",
            [
                "无抗拒 / 正常推进流程",
                "嫌980元太贵 / 问能不能便宜点",
                "孩子时间紧没空练字",
                "字迹定型了改不过来",
                "要跟孩子或家人商量",
                "孩子自己不重视",
                "已读不回 / 沉默不语"
            ]
        )
    with col_w2:
        parent_info = st.text_input("👤 家长与孩子基本情况", value="初三男生家长，孩子英语模拟考90分左右，作文涂改严重")
        lead_magnet_used = st.text_input("🎁 刚才送出的资料", value="2025中考答题卡1:1速成字帖PDF")

    if st.button("💬 一键生成微信实战话术与心理攻心策略", use_container_width=True, type="primary"):
        with st.spinner("🤖 正在运用教育私域转化心理学生成切片话术..."):
            wechat_prompt = f"""
你是一位拥有近10年私域教育高客单成交经验的顶级金牌导师与沟通心理学专家。
请根据以下微信沟通场景，为一线老师生成一套【高情商、不卑不亢、专业利他、强信任感】的微信聊天话术。

【沟通背景】：
- 当前阶段：{wechat_stage}
- 家长抗拒/顾虑点：{objection_type}
- 家长/孩子画像：{parent_info}
- 钩子物料：{lead_magnet_used}
- 核心转化目标产品：980元/6小时中高考卷面极速提分课（主打：针对中高考答题卡扫描机制，6小时攻克排版、字距与阅卷老师得分盲区，避免丢掉8-15分冤枉分）。

【话术输出要求】：
1. 【微信单条发送切片（核心重点）】：直接生成 3-5 条适合在微信里一条一条发出去的短文本（每条控制在2-3句话内，带真实教师口吻，语气亲切真诚且专业）。
2. 【攻心逻辑拆解】：简要说明为什么这几句话能击中家长心理、化解防备。
3. 【下一步动作引导】：提示老师发完这段话后，下一步该引导家长做什么（如：引导发作文照片、支付定金、锁定名额等）。
"""
            try:
                wechat_resp = client.chat.completions.create(
                    model=model_choice,
                    temperature=temp_choice,
                    messages=[{"role": "user", "content": wechat_prompt}]
                )
                st.session_state.wechat_result = wechat_resp.choices[0].message.content
                st.success("✅ 微信私域转化话术生成成功！")
            except Exception as e:
                st.error(f"❌ 生成失败: {str(e)}")

    if st.session_state.wechat_result:
        st.markdown("---")
        st.subheader("📋 微信实战聊天话术预览与复制")
        st.markdown(st.session_state.wechat_result)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        col_dw1, col_dw2 = st.columns(2)
        with col_dw1:
            st.download_button(
                label="📥 下载话术为 Markdown (.md)",
                data=st.session_state.wechat_result,
                file_name=f"WeChat_SOP_{timestamp}.md",
                mime="text/markdown",
                use_container_width=True
            )
        with col_dw2:
            st.download_button(
                label="📥 下载话术为纯文本 (.txt)",
                data=st.session_state.wechat_result,
                file_name=f"WeChat_SOP_{timestamp}.txt",
                mime="text/plain",
                use_container_width=True
            )

# ----------------- TAB 3: 诊断与报告 -----------------
with tab3:
    st.markdown("#### 🎯 生成 1对1 权威卷面诊断书与 980元 课程转化方案")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        student_name = st.text_input("👤 学员称呼", value="张同学 (初三)")
        teacher_name = st.text_input("👨‍🏫 诊断规划师/老师", value="林老师")
    with col2:
        subject_info = st.text_input("📚 科目与当前分数", value="中考英语 92分 / 满分120分")
        target_score = st.text_input("🎯 目标分数", value="105分以上")
    with col3:
        issues = st.text_area("🔍 试卷卷面典型问题描述", value="主观题作文涂改严重、字母倾斜度不一致、大小写不分、答题超出答题卡扫描红线边框")

    if st.button("📑 一键生成学员专属诊断报告与高情商转化方案", use_container_width=True, type="primary"):
        with st.spinner("🤖 正在深度分析卷面失分风险并制定抢分方案..."):
            diag_prompt = f"""
你是一位资深中高考卷面教研专家兼高客单私域转化操盘手。
请根据以下学员的卷面具体情况，生成一份极具专业度、权威感且能自然促进成交的《1对1中高考卷面深度诊断与提分规划书》。

【学员基本档案】：
- 学员称呼：{student_name}
- 诊断规划师：{teacher_name}
- 科目与现状：{subject_info}
- 冲刺目标：{target_score}
- 试卷卷面典型问题：{issues}

【核心商业目的】：
客观指出痛点，测算隐形丢分，给出科学抢分路径，并自然过渡推荐【980元/6小时中高考卷面极速提分实战营】。

【诊断规划书标准输出结构】：
一、【试卷卷面定性诊断】：从电子阅卷扫描成像与阅卷老师心理角度，指出三大致命失分硬伤。
二、【卷面隐形丢分精准测算】：测算出主观题、作文、书写规范方面预计被扣掉的“冤枉分”（给出具体分值区间）。
三、【6小时卷面通关专属抢分方案】：
    - 第1-2小时：笔画重构与字距标准化（杜绝扫描模糊）
    - 第3-4小时：答题卡空间布局与防出框控制（确保扫描完整）
    - 第5-6小时：高频失分题型实战临摹与阅卷给分点仿真训练
四、【老师高情商私域成交转化话术】：写一段发给家长的微信语音/文字转化话术，语气真诚、不生硬推销、体现极强专业性与紧迫感，自然引入980元课程。
"""
            try:
                diag_response = client.chat.completions.create(
                    model=model_choice,
                    temperature=min(temp_choice, 0.4),
                    messages=[{"role": "user", "content": diag_prompt}]
                )
                st.session_state.diag_result = diag_response.choices[0].message.content
                st.success("✅ 诊断报告生成成功！")
            except Exception as e:
                st.error(f"❌ 诊断生成失败: {str(e)}")

    if st.session_state.diag_result:
        st.markdown("---")
        st.subheader("📋 学员诊断报告预览与导出")
        st.markdown(st.session_state.diag_result)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.download_button(
                label=f"📥 下载【{student_name}】诊断书 (.md)",
                data=st.session_state.diag_result,
                file_name=f"Diagnosis_{student_name}_{timestamp}.md",
                mime="text/markdown",
                use_container_width=True
            )
        with col_d2:
            st.download_button(
                label=f"📥 下载【{student_name}】诊断书 (.txt)",
                data=st.session_state.diag_result,
                file_name=f"Diagnosis_{student_name}_{timestamp}.txt",
                mime="text/plain",
                use_container_width=True
            )
