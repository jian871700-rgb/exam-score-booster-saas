import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import database as db

# 初始化本地/云端数据库
db.init_db()

# 加载本地 .env
load_dotenv()

# 获取 API Key (优先读取 Streamlit Secrets，其次读取本地 .env)
api_key = st.secrets.get("DEEPSEEK_API_KEY", os.getenv("DEEPSEEK_API_KEY", ""))

# 页面基础配置
st.set_page_config(
    page_title="中高考卷面提分项目 · 商业级全流程增长工作台 v5.0 Pro",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义 CSS 优化商业质感
st.markdown("""
<style>
    .metric-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre-wrap;
        background-color: #f1f5f9;
        border-radius: 6px 6px 0px 0px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563eb !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# 侧边栏配置与授权
with st.sidebar:
    st.title("🎓 卷面提分 SaaS Pro")
    st.caption("商业交付与私域转化一体化系统 v5.0")
    
    st.divider()
    auth_code = st.text_input("🔐 内部授权访问码", type="password", help="请输入授权码解锁系统")
    
    # 授权码校验
    AUTHORIZED_CODES = ["exam2025", "vip888", "teacher999"]
    if auth_code not in AUTHORIZED_CODES:
        st.warning("⚠️ 请输入有效授权码以解锁所有商业功能。")
        st.stop()
    else:
        st.success("✅ 已授权：商业专业版 (Pro)")
    
    st.divider()
    st.subheader("⚙️ 引擎配置")
    if not api_key:
        api_key = st.text_input("DeepSeek API 密钥", type="password")
        if not api_key:
            st.error("请配置有效的 DEEPSEEK_API_KEY")
            st.stop()
    else:
        st.success("🟢 API 接口连接就绪")

    model_choice = st.selectbox(
        "🧠 核心模型选择",
        ["deepseek-chat", "deepseek-reasoner"],
        index=0,
        help="deepseek-chat: 响应快，适合爆款文案与即时话术；deepseek-reasoner: 适合深度卷面病理推理诊断"
    )
    
    temperature = st.slider("创意/严谨度 (Temperature)", min_value=0.1, max_value=1.0, value=0.6, step=0.05)
    
    st.divider()
    st.markdown("### 📊 商业运营指标")
    st.markdown("""
    - **课程定位**: 980元 / 6小时卷面提分
    - **核心引流品**: 2025中高考答题卡1:1模考字帖
    - **转化闭环**: 诊断报告 ➔ 痛点放大 ➔ 锁定名额
    """)

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# 顶部主标题与状态栏
st.title("🎓 中高考卷面提分项目 · 全流程增长工作台 v5.0 Pro")
st.markdown("从**小红书低成本获客**到**微信私域高客单转化**、**个性化诊断报告自动归档**的全链路商业武器库。")

# 5大核心模块标签页
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📕 小红书防限流文案工厂",
    "💬 微信私域转化专家",
    "📝 卷面诊断与高客单报告",
    "朋友圈 朋友圈高信任文案",
    "🗂️ 学员云端档案库 (DB)"
])

# ==========================================
# 模块 1：小红书防限流爆款文案工厂
# ==========================================
with tab1:
    st.subheader("📕 2025小红书防限流文案生成器")
    st.caption("严格遵循 2025 平台最新合规规则：严禁评论区诱导互动，采用自然场景引流与资深名师人设。")
    
    col1, col2 = st.columns(2)
    with col1:
        grade = st.selectbox("🎯 目标年级", ["初三中考冲刺", "高三高考冲刺", "初一/初二", "高一/高二"], key="xhs_grade")
        subject = st.selectbox("📚 针对学科", ["语文 (作文/阅读/卷面)", "英语 (书面表达/衡水体)", "文综/理综综合卷面", "全科卷面规范"], key="xhs_subject")
        target_audience = st.selectbox("👥 受众群体", ["焦虑的中高考考生家长", "卷面扣分严重的考生本人", "提分遇到瓶颈的学生"], key="xhs_target")
        
    with col2:
        pain_point = st.selectbox(
            "⚠️ 核心视觉/分数痛点",
            [
                "字迹潦草涂改，被阅卷机严重降档扣5-15分",
                "写字慢导致答题卡做不完，临考心慌",
                "平底字/笔画挤压，扫描后成一团黑墨",
                "明明知识点写对了，因为排版不规范被阅卷老师误判扣分"
            ],
            key="xhs_pain"
        )
        content_angle = st.selectbox(
            "📐 选题切入角度",
            [
                "【阅卷官内幕曝光】答题卡扫描后的真实残忍现场",
                "【提分对比逆袭】中等生靠卷面规范多拿12分的真实案例",
                "【避坑避雷指南】90%考生都在犯的3个卷面致命扣分习惯",
                "【保姆级提分法】每天15分钟，考前1个月速成阅卷机最爱字体"
            ],
            key="xhs_angle"
        )
        lead_magnet = st.text_input("🎁 引流载体（自然植入）", value="2025中高考答题卡1:1速成训练字帖PDF版（群文件/主页自取）")

    if st.button("🚀 一键生成小红书爆款文案", type="primary", use_container_width=True):
        prompt = f"""你是一名拥有10年中高考阅卷经验的资深名师兼小红书百万爆款操盘手。
请为“中高考卷面提分项目”撰写一篇严格符合2025年小红书最新防限流规则的高互动爆款笔记。

【输入参数】
- 年级阶段：{grade}
- 提分学科：{subject}
- 核心受众：{target_audience}
- 核心痛点：{pain_point}
- 选题切口：{content_angle}
- 引流资料：{lead_magnet}

【核心撰写规范】
1. 严禁出现“私信我发你”、“评论区扣1”等违规诱导字眼！引流方式必须采用“自然场景分享”（例如：字帖已整理好放在主页粉丝群/群文件，需要的同学自取）。
2. 结构清晰：
   - 【爆款标题库】：提供 3 个极具点击欲望的标题（涵盖痛点型、内幕型、反常识型，含精准Emoji）。
   - 【封面视觉脚本】：给出 2 张极具视觉冲击力的封面实拍建议（前后卷面对比/扫描放大细节）。
   - 【笔记正文】：第一人称名师口吻，痛点场景扎心 ➔ 阅卷底层逻辑拆解 ➔ 提分实操方案 ➔ 自然植入引流品。
   - 【精准标签库】：5-8个高权重、高垂直度的话题标签（带 # 号）。
"""
        with st.spinner("🤖 正在为您生成防限流高转化文案..."):
            try:
                response = client.chat.completions.create(
                    model=model_choice,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    stream=True
                )
                st.markdown("### 📝 生成结果：")
                st.write_stream(response)
            except Exception as e:
                st.error(f"生成失败：{str(e)}")

# ==========================================
# 模块 2：微信私域转化与异议攻心专家
# ==========================================
with tab2:
    st.subheader("💬 微信私域 5 阶段切片式转化话术")
    st.caption("针对加微信后的每一个关键节点，精准输出攻心话术，把引流流量转化为 980 元高客单付费学员。")
    
    stage = st.selectbox(
        "📍 当前用户处于的私域转化阶段",
        [
            "阶段 1：好友刚通过（打招呼 + 赠送字帖 + 顺畅索要试卷卷面照片）",
            "阶段 2：收到卷面照片（即时抛出 3 个致命扣分点 + 制造紧迫感）",
            "阶段 3：抛出【980元/6小时中高考卷面提分课】（高价值方案介绍 + 锁定名额）",
            "阶段 4：处理异议 -【价格嫌贵 / 考虑一下】（投资回报比 + 1分甩掉千人理念）",
            "阶段 5：处理异议 -【孩子没时间练字 / 临考来不及】（不是练书法，是考场答题战术）",
            "阶段 6：未成交沉默唤醒（发布同类学员模考逆袭喜报 + 最后一席名额逼单）"
        ]
    )
    
    col_a, col_b = st.columns(2)
    with col_a:
        parent_type = st.selectbox("家长画像", ["极度焦虑型（成绩中等想冲重点）", "理性对比型（关心具体怎么提分）", "时间紧迫型（马上中高考）"])
    with col_b:
        student_current_score = st.text_input("学员目前平时卷面大致扣分/总分", value="平时卷面大致扣8-12分，语文总分95分左右")
        
    custom_objection = st.text_area("家长具体提出的顾虑/原话（选填）", placeholder="例如：老师，现在离中考就剩两个月了，真能提高吗？会不会耽误复习时间？")

    if st.button("⚡ 生成私域切片攻心话术", type="primary", use_container_width=True):
        prompt = f"""你是一名拥有极高成单率的高端教育私域成交导师。
请为【980元/6小时中高考卷面提分课】撰写针对微信私域当前阶段的销售实战切片话术。

【当前场景】
- 所处阶段：{stage}
- 家长画像：{parent_type}
- 学员分数现状：{student_current_score}
- 家长原话/顾虑：{custom_objection if custom_objection else "按阶段标准常见异议处理"}

【输出要求】
1. **微信发送切片（核心）**：拆分成 3~4 条适合直接微信复制发送的短句（每条50-100字，口吻真实自然、专业温暖，绝不带机器翻译感）。
2. **心理学底层逻辑解析**：指出这几句话为什么能击穿家长防御心理、建立专业信任。
3. **下一步行动指令（CTA）**：引导家长立即回复的关键提问。
"""
        with st.spinner("🤖 正在为您定制私域成交话术..."):
            try:
                response = client.chat.completions.create(
                    model=model_choice,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    stream=True
                )
                st.markdown("### 💬 实战微信复制话术：")
                st.write_stream(response)
            except Exception as e:
                st.error(f"生成失败：{str(e)}")

# ==========================================
# 模块 3：卷面诊断与高客单报告书 (自动落库)
# ==========================================
with tab3:
    st.subheader("📝 学员卷面深度病理诊断报告与提分方案")
    st.caption("生成权威的《中高考阅卷官卷面诊断书》，并自动归档至云端学员数据库。")
    
    col_x, col_y = st.columns(2)
    with col_x:
        s_name = st.text_input("👤 学员姓名/昵称", value="张同学", key="diag_name")
        s_grade = st.selectbox("🎓 目标考段", ["初三 (中考目标重高)", "高三 (高考冲刺特控线)", "初二", "高二"], key="diag_grade")
        s_subject = st.selectbox("📖 诊断科目", ["语文作文及全卷", "英语书面表达", "文综/理综答题卡综合"], key="diag_subject")
        s_gap = st.text_input("📉 估算潜在卷面丢分", value="8 - 14 分", key="diag_gap")

    with col_y:
        s_desc = st.text_area(
            "🔍 卷面具体问题描述（可根据家长发来的答题卡照片输入）",
            value="1. 字体大小不均，字距过紧，扫描后行距几乎贴在一起；\n2. 涂改频繁，使用涂改液痕迹或大面积黑块涂抹；\n3. 答题超出扫描红色边框线，导致阅卷机边缘吃字漏判。",
            height=130,
            key="diag_desc"
        )

    if st.button("📋 一键生成深度诊断报告并入库", type="primary", use_container_width=True):
        prompt = f"""你是一名资深中高考主观题阅卷组组长。请根据以下学员的卷面问题，输出一份极具权威性、让家长看了立刻意识到严重性并愿意购买980元提分课的《中高考阅卷官卷面深度诊断与提分报告书》。

【学员基本档案】
- 学员姓名：{s_name}
- 报考阶段：{s_grade}
- 诊断学科：{s_subject}
- 预估卷面失分：{s_gap}
- 卷面特征描述：{s_desc}

【报告输出格式规范】
# 🎓【中高考阅卷组】学员卷面病理深度诊断书
**学员档案**：{s_name} | {s_grade} | {s_subject} | 潜在提升空间：{s_gap}

## 一、 阅卷机扫描与阅卷官视觉分析
（针对描述中的问题，用高清扫描仪还原真实阅卷场景，指出阅卷老师在7-10秒内看到该卷面的真实心理打分倾向）

## 二、 核心卷面失分三大致命病灶
（分点深入剖析：如字距行距压迫感、答题超框风险、涂改黑洞效应）

## 三、 专属卷面提分处方（6小时提分法）
（给出可落地的战术训练路线，证明无需练书法，只需掌握答题卡空间排版学即可提分）

## 四、 专家综合评估与保分建议
（明确指出距离考前的抢分窗口期，并推荐配套【980元/6小时中高考卷面提分课】）
"""
        with st.spinner("🤖 阅卷专家正在出具报告并保存至数据库..."):
            try:
                # 获取完整文本输出
                resp = client.chat.completions.create(
                    model=model_choice,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5
                )
                report_content = resp.choices[0].message.content
                
                # 自动保存入库
                db.save_report(
                    student_name=s_name,
                    grade=s_grade,
                    subject=s_subject,
                    score_gap=s_gap,
                    issue_desc=s_desc,
                    report_content=report_content
                )
                
                st.success(f"🎉 诊断报告已成功生成，并已持久化归档至学员数据库！")
                st.markdown(report_content)
                
            except Exception as e:
                st.error(f"生成或入库失败：{str(e)}")

# ==========================================
# 模块 4：朋友圈高信任成交文案工厂
# ==========================================
with tab4:
    st.subheader("朋友圈 朋友圈高信任成交文案工厂")
    st.caption("打造名师 IP 真实感朋友圈，针对中高考家长痛点持续种草、建立极高专业信任。")
    
    m_type = st.selectbox(
        "📱 朋友圈内容类型",
        [
            "【学员逆袭喜报】刚辅导完6小时学员模考卷面提升8分",
            "【阅卷现场内幕】分享一张中考/高考阅卷扫描现场真实对比图心得",
            "【专业干货避坑】告诉家长为什么临考切忌让孩子练庞中华/楷书",
            "【限时名额锁定】周末6小时卷面提分集训营仅剩最后2个名额"
        ]
    )
    m_detail = st.text_input("💡 亮点细节/学员背景（选填）", value="高三理科生李同学，平时理综答题卡全黑，经过2次课调整网格间距，模考多拿了11分")

    if st.button("✨ 生成朋友圈高信任文案", type="primary", use_container_width=True):
        prompt = f"""你是一名中高考卷面提分名师IP操盘手。请写一条符合微信朋友圈阅读习惯的真实、高信任、强转化的文案。

【文案类型】：{m_type}
【背景细节】：{m_detail}

【撰写要求】：
1. 语言极其真实自然，像一位负责任、专业度极高的老师在发生活和工作日常，严禁浓厚微商感或AI感。
2. 采用短段落换行，保证在朋友圈不被“折叠全文”。
3. 评论区“第一条神评论（SOP）”：给出老师自己在评论区置顶引导互动或转化的第一条话术。
4. 附带【配图建议】：说明这条朋友圈应该配什么样的真实图片（如聊天记录截图/字迹对比/答题卡局部）。
"""
        with st.spinner("🤖 正在为您生成朋友圈爆款文案..."):
            try:
                response = client.chat.completions.create(
                    model=model_choice,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    stream=True
                )
                st.markdown("### 📱 朋友圈实战发布方案：")
                st.write_stream(response)
            except Exception as e:
                st.error(f"生成失败：{str(e)}")

# ==========================================
# 模块 5：学员云端档案与数据中心
# ==========================================
with tab5:
    st.subheader("🗂️ 学员卷面诊断档案与历史数据库")
    st.caption("基于 SQLite 本地/云端持久化存储，支持按姓名快速检索、历史诊断书回溯与导出。")
    
    search_keyword = st.text_input("🔍 按学员姓名快速检索档案", placeholder="输入学员姓名，留空显示全部...")
    
    records = db.get_all_reports(search_keyword)
    
    col_count, col_action = st.columns([3, 1])
    with col_count:
        st.info(f"📊 当前数据库已归档诊断报告：**{len(records)}** 份")
        
    if records:
        for rec in records:
            # rec 结构: (id, student_name, grade, subject, score_gap, issue_desc, report_content, created_at)
            rec_id = rec[0]
            rec_name = rec[1]
            rec_grade = rec[2]
            rec_subject = rec[3]
            rec_gap = rec[4]
            rec_time = rec[7]
            rec_content = rec[6]
            
            with st.expander(f"📁 【{rec_name}】{rec_grade} - {rec_subject}（潜在提分：{rec_gap}）- {rec_time}"):
                st.markdown(rec_content)
                st.download_button(
                    label=f"📥 导出【{rec_name}】诊断报告书 (Markdown)",
                    data=rec_content,
                    file_name=f"{rec_name}_卷面诊断报告_{rec_subject}.md",
                    mime="text/markdown",
                    key=f"dl_{rec_id}"
                )
    else:
        st.write("📭 暂无相关诊断档案记录。在【模块 3】生成报告后将自动归档在此。")
