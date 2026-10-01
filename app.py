"""
中高考卷面提分项目 - 商业级全能 SaaS 运营工作台 v5.0 (Pro 旗舰版)
集成了：
1. 小红书防限流文案工厂 (含2025新规安全模式)
2. 微信私域转化与异议攻心专家 (切片化话术)
3. 学员卷面诊断与高客单报告书 (自动落盘入库)
4. 微信朋友圈高信任成交文案工厂
5. 🗄️ 云端学员档案库与历史复盘 (SQLite 数据库支持)
"""

import streamlit as st
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import database as db

# 1. 页面基本配置
st.set_page_config(
    page_title="中高考卷面提分 · 商业全能 SaaS 工作台",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化数据库表
db.init_db()

# 注入高质感 UI 样式
st.markdown("""
<style>
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .metric-title {
        color: #64748b;
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 4px;
    }
    .metric-value {
        color: #0f172a;
        font-size: 20px;
        font-weight: 700;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 18px;
        font-weight: 600;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

# 2. 状态持久化初始化
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "xhs_result" not in st.session_state:
    st.session_state.xhs_result = None
if "wechat_result" not in st.session_state:
    st.session_state.wechat_result = None
if "diagnose_result" not in st.session_state:
    st.session_state.diagnose_result = None
if "moments_result" not in st.session_state:
    st.session_state.moments_result = None

# 3. 授权验证与安全检查
AUTHORIZED_KEYS = ["exam2025", "vip888", "teacher999"]

# 优先从 Streamlit Secrets 读取，次选本地环境变量
api_key = st.secrets.get("DEEPSEEK_API_KEY") if hasattr(st, "secrets") and "DEEPSEEK_API_KEY" in st.secrets else None
if not api_key:
    load_dotenv()
    api_key = os.getenv("DEEPSEEK_API_KEY")

# 4. 侧边栏：安全授权与系统配置
with st.sidebar:
    st.title("⚙️ 系统中枢 & 权限")
    
    if not st.session_state.authenticated:
        access_pwd = st.text_input("🔑 请输入运营授权码：", type="password")
        if st.button("验证并进入系统", use_container_width=True):
            if access_pwd in AUTHORIZED_KEYS:
                st.session_state.authenticated = True
                st.success("✅ 授权成功，欢迎使用！")
                st.rerun()
            else:
                st.error("❌ 授权码错误，请联系管理员！")
                st.stop()
        else:
            st.info("💡 请先输入授权码以解锁所有商业模块。")
            st.stop()
    else:
        st.success("🟢 当前授权状态：VIP 机构运营版")
        if st.button("🔒 退出当前授权", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    st.markdown("---")
    st.subheader("🤖 AI 模型配置")
    
    # 动态支持手动填写 API Key（备用方案）
    if not api_key:
        api_key = st.text_input("DeepSeek API Key:", type="password", placeholder="sk-...")
        if not api_key:
            st.warning("⚠️ 未检测到 API Key，请在下方配置或设置 Secrets。")
            st.stop()

    model_option = st.selectbox(
        "选择推理模型：",
        ["deepseek-chat", "deepseek-reasoner"],
        index=0,
        help="deepseek-chat 速度极快，适合图文与朋友圈；deepseek-reasoner 具备深度逻辑链，适合私域深度攻心与复杂卷面诊断。"
    )
    
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    st.markdown("---")
    st.subheader("📊 商业闭环定位")
    st.caption("核心产品：**980元/6小时中高考卷面提分课**")
    st.caption("引流钩子：**《2025答题卡1:1速练字帖PDF》**")
    st.caption("数据库支持：**SQLite 本地持久化**")

# 5. 主工作台界面
st.title("🎯 中高考卷面提分 · 商业全能 SaaS 工作台 (Pro)")
st.markdown("覆盖 **公域引流 ➡️ 私域转化 ➡️ 卷面诊断 ➡️ 朋友圈发酵 ➡️ 学员档案库** 的全流程高客单变现引擎。")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📕 小红书防限流文案工厂", 
    "💬 微信私域转化专家", 
    "📝 卷面诊断与提分报告",
    "⭕ 朋友圈高信任成交工厂",
    "🗄️ 云端学员档案库 (Pro)"
])

# ==========================================
# TAB 1: 小红书防限流文案工厂
# ==========================================
with tab1:
    st.header("📕 小红书防限流文案生成器 (2025 平台新规适配)")
    st.info("💡 **合规安全模式**：文案全程摒弃生硬的「扣1免费领」，采用情境式触发与粉丝群官方合规引导，规避限流与违规判定。")
    
    col1, col2 = st.columns(2)
    with col1:
        grade_xhs = st.selectbox("学生学段：", ["初一", "初二", "初三 (中考)", "高一", "高二", "高三 (高考)"], key="xhs_grade")
        subject_xhs = st.selectbox("学科领域：", ["数学", "语文", "英语", "物理", "化学", "全科通用"], key="xhs_subject")
        target_score = st.text_input("预期卷面提分目标：", "5-15分 (稳拿卷面印象分)", key="xhs_score")
        
    with col2:
        pain_point_xhs = st.selectbox(
            "核心卷面痛点：",
            [
                "字迹潦草涂改多，阅卷老师直接按最低档给分",
                "答题不规范，解答题没有分步骤写步骤分全丢",
                "写字太慢导致最后压轴题没时间做",
                "答题卡超出边界被扫描仪裁切丢失",
                "中高考电脑阅卷双评误差导致的隐形扣分"
            ],
            key="xhs_pain"
        )
        style_xhs = st.selectbox("笔记风格包装：", ["一线阅卷老师内部视角 (权威避坑)", "学霸提分复盘 (逆袭干货)", "焦虑家长拯救指南 (痛点共鸣)"], key="xhs_style")

    if st.button("🚀 生成合规小红书文案", type="primary", use_container_width=True):
        prompt = f"""
        你是一位精通 2025 年小红书最新算法规则的中高考卷面提分资深名师。
        请为【980元/6小时中高考卷面规范提分课】撰写一篇爆款小红书图文文案。

        【参数信息】：
        - 学段：{grade_xhs}
        - 学科：{subject_xhs}
        - 提分目标：{target_score}
        - 核心痛点：{pain_point_xhs}
        - 风格定位：{style_xhs}

        【2025 平台防限流与高转化铁律】：
        1. 严禁出现「评论区扣1」、「私信我发你」、「免费领取」等强诱导互动词汇（会被系统判定为违规诱导）。
        2. 引流钩子软植入：在文末以自然口吻提及「针对这套规范，我把中高考答题卡1:1模版和提分细则整理到了自留的复习资料/粉丝群资料库里，需要的同学/家长直接到置顶群聊或按照平时习惯自取即可」。
        3. 格式要求：
           - 包含 3 个具有点击率的爆款标题（带 Emoji）；
           - 封面图设计建议（极度具体：画面左边放什么、右边放什么、打什么大字痛点标签）；
           - 结构清晰的正文（痛点直击 -> 阅卷内幕揭秘 -> 3个马上可用的改卷面技巧 -> 提分钩子植入 -> 标签）。
        """
        
        with st.spinner("AI 正在根据 2025 小红书最新算法生成防限流文案..."):
            response = client.chat.completions.create(
                model=model_option,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            st.session_state.xhs_result = response.choices[0].message.content

    if st.session_state.xhs_result:
        st.markdown("### 📋 生成结果")
        st.markdown(st.session_state.xhs_result)
        st.download_button(
            label="📥 下载本篇笔记 (Markdown 格式)",
            data=st.session_state.xhs_result,
            file_name=f"{grade_xhs}_{subject_xhs}_小红书文案.md",
            mime="text/markdown"
        )

# ==========================================
# TAB 2: 微信私域转化与异议攻心专家
# ==========================================
with tab2:
    st.header("💬 微信私域转化专家 (切片化高情商话术)")
    st.caption("针对进私域的家长/学员，生成符合真实微信聊天节奏的「短句切片」，一键复制即发。")
    
    col1, col2 = st.columns(2)
    with col1:
        stage = st.selectbox(
            "当前私域沟通阶段：",
            [
                "1. 刚通过好友 (首响破冰与资料交付)",
                "2. 试卷反馈后 (指出卷面硬伤与提分空间)",
                "3. 抛出 980元/6小时 提分课程",
                "4. 异议攻心 (嫌贵/没时间/想自己练)",
                "5. 未成交沉睡用户激活 (利用模考/倒计时)"
            ],
            key="wechat_stage"
        )
        parent_feedback = st.text_input("家长/学生说的那句话（或当前状态）：", "980块钱有点贵，孩子自己在字帖上描一描不行吗？", key="wechat_input")
        
    with col2:
        student_info_wx = st.text_input("学员背景（年级/科目/分数段）：", "初三/数学105分左右/字迹偏乱步骤经常挤在一起", key="wechat_bg")
        tone_wx = st.selectbox("老师沟通人设：", ["专业严谨且有温度的名师", "推心置腹、懂升学压力的学姐/助教", "直击要害、雷厉风行的阅卷组老师"], key="wechat_tone")

    if st.button("⚡ 生成微信对齐切片话术", type="primary", use_container_width=True):
        prompt = f"""
        你是一位拥有极高转化率的家庭教育咨询名师兼私域销售转化专家。
        现在需要针对微信聊天场景，生成一套能够直接复制发给家长的「切片化短句回复话术」。

        【背景参数】：
        - 沟通阶段：{stage}
        - 家长输入/异议：{parent_feedback}
        - 学员背景：{student_info_wx}
        - 老师人设：{tone_wx}
        - 最终成交目标：980元/6小时【中高考卷面规范提分定制课】

        【输出硬性要求】：
        1. 必须输出为【切片化短消息】格式（模拟微信打字，每条在 20-50 字左右），标明【第1条】、【第2条】、【第3条】、【第4条】。
        2. 严禁出现长篇大论的教科书式说教！必须符合真实微信聊天心理学（先共情 -> 破除误区/点出致命痛点 -> 给解决方案 -> 给出微行动指令）。
        3. 针对「嫌980贵」：必须算账（中高考1分压倒一千人，卷面5-15分只需980，平均1分不到100元，比补课几千块划算得多）。
        4. 针对「想自己练」：指出字帖练的是书法，考试要的是扫描仪识别度与答题区域布局，练错反而浪费冲刺时间。
        """
        
        with st.spinner("AI 正在推演家长心理防御并生成切片式攻心话术..."):
            response = client.chat.completions.create(
                model=model_option,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.65
            )
            st.session_state.wechat_result = response.choices[0].message.content

    if st.session_state.wechat_result:
        st.markdown("### 💬 建议复制以下切片短句直接发送：")
        st.markdown(st.session_state.wechat_result)

# ==========================================
# TAB 3: 学员卷面诊断与高客单报告书 (支持自动落盘入库)
# ==========================================
with tab3:
    st.header("📝 学员卷面深度诊断与提分规划书")
    st.caption("输入学员卷面特征，生成一份极具专业度、让家长愿意为 980 元买单的《卷面提分诊断报告书》，并自动存入学员档案库。")
    
    col1, col2 = st.columns(2)
    with col1:
        s_name = st.text_input("学员姓名/代号：", "张同学", key="diag_name")
        s_grade = st.selectbox("所在年级：", ["初二", "初三 (中考)", "高一", "高二", "高三 (高考)"], key="diag_grade")
        s_subject = st.selectbox("主要诊断学科：", ["语文 (作文与简答)", "数学 (大题步骤规范)", "英语 (作文书写与涂卡)", "理综/文综综合卷面"], key="diag_sub")
        
    with col2:
        s_score_gap = st.text_input("当前成绩与目标差距：", "当前102分，目标115分 (卷面预估丢分8-12分)", key="diag_score")
        s_issues = st.text_area(
            "卷面硬伤特征描述：", 
            "字迹倾斜且偏小，涂改处直接打黑团；解答题没有分步骤写“解/答/公式”，大题逻辑混乱，阅卷老师很难一眼抓到得分点；答题卡第21题有超出黑色边框现象。",
            key="diag_issues"
        )

    if st.button("📋 生成专业诊断书并自动归档", type="primary", use_container_width=True):
        prompt = f"""
        你是一位中高考命题阅卷组特聘卷面规范专家。
        请为学员【{s_name}】出具一份极具权威感、说服力且排版优美的《中高考卷面提分深度诊断与行动方案》。

        【学员档案】：
        - 姓名：{s_name}
        - 学段：{s_grade}
        - 学科：{s_subject}
        - 成绩与差距：{s_score_gap}
        - 卷面实测硬伤：{s_issues}

        【报告结构规范】：
        # 📑《中高考卷面规范与提分空间深度诊断报告书》
        ## 一、卷面综合定级与隐形丢分评估（定级：如 C级严重失分 / B级隐患较大 / A级良好需精进，并明确指出卷面预计损失的具体分值）
        ## 二、阅卷机视角三大致命硬伤剖析（从高分扫描仪成像、阅卷老师 5-8 秒扫视心理学深度解读）
        ## 三、6小时卷面重塑与提分定制路径（分为：书写结构矫正 2h -> 黄金答题排版规范 2h -> 压轴题抢分话术模版 2h）
        ## 四、专家建议与行动方案（顺理成章引出 980元/6小时 定制卷面提分课，说明预期提分效果与保分承诺）
        """
        
        with st.spinner("AI 正在构建专业医学级提分诊断报告并归档..."):
            response = client.chat.completions.create(
                model=model_option,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5
            )
            report_text = response.choices[0].message.content
            st.session_state.diagnose_result = report_text
            
            # 自动保存到 SQLite 数据库
            db.save_report(
                student_name=s_name,
                grade=s_grade,
                subject=s_subject,
                score_gap=s_score_gap,
                issue_desc=s_issues,
                report_content=report_text
            )
            st.toast(f"💾 学员【{s_name}】的诊断报告已自动永久归档至云端学员库！", icon="✅")

    if st.session_state.diagnose_result:
        st.markdown("### 📄 诊断报告书预览")
        st.markdown(st.session_state.diagnose_result)
        
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.download_button(
                label=f"📥 导出为学员专属诊断书 ({s_name}.md)",
                data=st.session_state.diagnose_result,
                file_name=f"{s_name}_{s_grade}_{s_subject}_卷面诊断提分报告.md",
                mime="text/markdown",
                use_container_width=True
            )
        with col_d2:
            st.download_button(
                label=f"📄 导出为纯文本 ({s_name}.txt)",
                data=st.session_state.diagnose_result,
                file_name=f"{s_name}_诊断报告.txt",
                mime="text/plain",
                use_container_width=True
            )

# ==========================================
# TAB 4: 朋友圈高信任成交文案工厂
# ==========================================
with tab4:
    st.header("⭕ 朋友圈高信任成交文案工厂")
    st.caption("打造不惹人烦、专业度拉满、持续唤醒家长的朋友圈内容矩阵。")
    
    col1, col2 = st.columns(2)
    with col1:
        moment_type = st.selectbox(
            "朋友圈内容模型：",
            [
                "1. 学员提分对比模型 (视觉冲击+成绩逆袭)",
                "2. 阅卷内幕/认知颠覆模型 (打破家长固有认知)",
                "3. 名额稀缺/交付日常模型 (展现火爆与负责态度)",
                "4. 家长走心好评/感谢模型 (第三方证言造势)"
            ],
            key="moment_type"
        )
        grade_moment = st.selectbox("针对学段：", ["初三 (中考冲刺)", "高三 (高考冲刺)", "初一初二/高一高二 (提前规避)"], key="moment_grade")
        
    with col2:
        subject_moment = st.selectbox("针对学科：", ["数学大题", "语文作文", "英语书写", "全科答题规范"], key="moment_sub")
        detail_moment = st.text_input("具体素材细节（如提了多少分/哪个学校学员/今天收到了什么反馈）：", "初三学生经过6小时规范训练，模拟考数学大题步骤分全拿，卷面多拿了9分！", key="moment_detail")

    if st.button("✨ 一键生成高转化朋友圈", type="primary", use_container_width=True):
        prompt = f"""
        你是一位深谙微信私域朋友圈成交逻辑的教育名师 IP 操盘手。
        请为【980元/6小时中高考卷面提分课】撰写一条极具吸引力、高信任度且不折叠的朋友圈文案。

        【模型参数】：
        - 内容模型：{moment_type}
        - 针对学段：{grade_moment}
        - 针对学科：{subject_moment}
        - 真实细节：{detail_moment}

        【朋友圈文案核心规则】：
        1. 【防折叠排版】：前两行必须是黄金吸睛钩子（不被“全文”折叠隐藏）；段落之间空行，适当使用 Emoji。
        2. 【配图建议】：给出极度具体的 1-3 张图片搭配方案（如：左图练前涂改卷，右图练后规范卷，中间放成绩单/家长聊天截图）。
        3. 【第一条评论 (自评套路)】：文末提供 1 条老师在朋友圈自评区置顶的话术（用于引导私聊或制造紧迫感，不污染正文格调）。
        """
        
        with st.spinner("AI 正在根据微信朋友圈传播算法生成高转化文案..."):
            response = client.chat.completions.create(
                model=model_option,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            st.session_state.moments_result = response.choices[0].message.content

    if st.session_state.moments_result:
        st.markdown("### 📱 朋友圈文案与配图方案")
        st.markdown(st.session_state.moments_result)

# ==========================================
# TAB 5: 云端学员档案库 (Pro)
# ==========================================
with tab5:
    st.header("🗄️ 云端学员档案库与历史复盘 (Pro)")
    st.caption("所有在【Tab 3】生成的学员诊断报告均在此永久保存，支持按姓名快速检索、回看与管理。")
    
    # 顶部搜索与数据概览
    search_col, stat_col = st.columns([2, 1])
    with search_col:
        search_kw = st.text_input("🔍 搜索学员姓名 / 年级 / 学科：", placeholder="输入如：张同学、初三、数学...", key="search_kw")
    
    # 获取数据库中的记录
    records = db.get_all_reports(search_query=search_kw.strip() if search_kw else None)
    
    with stat_col:
        st.metric("📁 已沉淀档案总数", f"{len(records)} 份")
        
    st.markdown("---")
    
    if not records:
        if search_kw:
            st.warning(f"🔍 未找到与「{search_kw}」相关的学员记录。")
        else:
            st.info("💡 暂无学员档案。请前往【Tab 3 卷面诊断与提分报告】生成第一份学员诊断书，系统将自动在此建立档案！")
    else:
        for item in records:
            with st.expander(f"👤 学员：{item['student_name']} | 🎓 {item['grade']} - {item['subject']} | ⏱️ {item['created_at']}"):
                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    st.write(f"**提分目标：** {item['score_gap']}")
                with col_info2:
                    st.write(f"**卷面硬伤特征：** {item['issue_desc']}")
                
                st.markdown("#### 📄 完整诊断报告书：")
                st.markdown(item['report_content'])
                
                btn_col1, btn_col2 = st.columns([1, 1])
                with btn_col1:
                    st.download_button(
                        label=f"📥 重新导出诊断书 ({item['student_name']}.md)",
                        data=item['report_content'],
                        file_name=f"{item['student_name']}_{item['grade']}_诊断报告.md",
                        mime="text/markdown",
                        key=f"dl_{item['id']}"
                    )
                with btn_col2:
                    if st.button(f"🗑️ 删除此档案", key=f"del_{item['id']}"):
                        db.delete_report(item['id'])
                        st.toast(f"已成功删除学员【{item['student_name']}】的档案！", icon="🗑️")
                        st.rerun()

# 6. 页脚说明
st.markdown("---")
st.caption("🔒 中高考卷面提分 SaaS Pro v5.0 | 数据安全本地持久化 | 仅供授权机构内部使用")
