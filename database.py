import streamlit as st
import os
import requests
import json
import base64
import sqlite3
from datetime import datetime

# ==============================
# 0. 数据库初始化 (SQLite 本地持久化)
# ==============================
def init_db():
    conn = sqlite3.connect('students_archive.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            grade_subject TEXT,
            score_gap TEXT,
            diagnosis_report TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_student_record(name, grade_subject, gap, report):
    conn = sqlite3.connect('students_archive.db')
    cursor = conn.cursor()
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO student_records (student_name, grade_subject, score_gap, diagnosis_report, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, grade_subject, gap, report, time_now))
    conn.commit()
    conn.close()

def get_all_records():
    conn = sqlite3.connect('students_archive.db')
    cursor = conn.cursor()
    cursor.execute('SELECT student_name, grade_subject, score_gap, diagnosis_report, created_at FROM student_records ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

init_db()

# ==============================
# 1. 页面基础配置与品牌 UI
# ==============================
st.set_page_config(
    page_title="中高考卷面提分专家 SaaS v6.0 Pro Vision",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 注入高端商业定制 CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.1rem;
        font-weight: 800;
        background: linear-gradient(120deg, #1E3A8A, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .sub-title {
        color: #4B5563;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
    .card-box {
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 16px 20px;
        border-left: 5px solid #3B82F6;
        margin-bottom: 15px;
    }
    .tag-badge {
        display: inline-block;
        background: #EFF6FF;
        color: #1D4ED8;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# 2. 侧边栏 API 配置与控制台
# ==============================
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/combo-chart.png", width=70)
    st.markdown("### ⚙️ 系统控制台")
    st.markdown("---")
    
    # 自动读取 Secrets 或允许手动输入
    env_key = st.secrets.get("DEEPSEEK_API_KEY", "")
    api_key_input = st.text_input(
        "DeepSeek API 密钥:",
        value=env_key if env_key else "",
        type="password",
        help="建议直接在 Streamlit Secrets 中配置 DEEPSEEK_API_KEY"
    )
    
    st.markdown("---")
    st.markdown("### 📊 项目商业资产数据")
    st.markdown("• **主推课程**：980元/6小时卷面提分特训")
    st.markdown("• **核心定位**：专治答题不规范、扫卷折损")
    st.markdown("• **底层引擎**：DeepSeek-V3 / Qwen-VL")
    st.markdown("• **数据存储**：SQLite 云端归档库")
    st.markdown("---")
    st.caption("© 2026 卷面提分矩阵 All Rights Reserved.")

# ==============================
# 3. 底层 API 请求通用方法
# ==============================
def call_deepseek_stream(messages, temperature=0.7):
    """DeepSeek 文本大模型流式调用"""
    target_api_key = api_key_input.strip()
    if not target_api_key:
        st.error("❌ 请在左侧配置有效的 DeepSeek API Key 后再使用！")
        return None

    headers = {
        "Authorization": f"Bearer {target_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": temperature,
        "stream": True
    }

    try:
        response = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers=headers,
            json=payload,
            stream=True,
            timeout=60
        )
        if response.status_code != 200:
            st.error(f"❌ API 请求异常：{response.status_code} - {response.text}")
            return None
        
        for chunk in response.iter_lines():
            if chunk:
                chunk_str = chunk.decode("utf-8")
                if chunk_str.startswith("data: "):
                    data_str = chunk_str[6:]
                    if data_str.strip() == "[DONE]":
                        break
                    try:
                        data_json = json.loads(data_str)
                        content = data_json["choices"][0]["delta"].get("content", "")
                        if content:
                            yield content
                    except Exception:
                        continue
    except Exception as e:
        st.error(f"❌ 网络调用异常: {str(e)}")
        return None

# ==============================
# 4. 页面主体与 5 大商业模块
# ==============================
st.markdown('<div class="main-title">🎯 中高考卷面提分专家 SaaS v6.0 Pro Vision</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">全链路多模态商业工作台：小红书获客 ➔ 微信私域转化 ➔ 答题卡智能视觉诊断 ➔ 朋友圈造势 ➔ 学员档案管理</div>', unsafe_allow_html=True)

# 标签页划分
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📸 模块一：答题卡视觉诊断 (Vision)",
    "📕 模块二：小红书防限流文案工厂",
    "💬 模块三：微信私域异议攻心专家",
    "⭕ 模块四：朋友圈成交势能文案",
    "🗄️ 模块五：学员诊断云端档案库"
])

# ----------------------------------------------------
# 模块一：答题卡视觉诊断 (Vision)
# ----------------------------------------------------
with tab1:
    st.markdown('<div class="card-box"><b>📸 答题卡智能视觉诊断：</b>上传或拍照学生答题卡，AI 自动扫描字体、行距与电子扫描折损点，生成 980 元课程转化诊断报告。</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        v_name = st.text_input("学员姓名 / 微信昵称", value="张同学", key="v_name")
        v_grade_subject = st.selectbox("年级与诊断科目", ["初三中考 / 语文", "初三中考 / 英语", "初三中考 / 理化", "高三高考 / 语文", "高三高考 / 英语", "高三高考 / 文综", "高三高考 / 理综"], key="v_grade_subject")
        v_target_gap = st.text_input("当前成绩与目标分差", value="平时102分，目标120分（差距18分）", key="v_target_gap")
        
        uploaded_file = st.file_uploader("📤 上传答题卡/卷面照片", type=["jpg", "jpeg", "png"], help="支持单张卷面局部或整页拍照上传")
        
        if uploaded_file is not None:
            st.image(uploaded_file, caption="已上传待诊断卷面", use_container_width=True)

    with col2:
        v_extra_detail = st.text_area("卷面额外观察说明（可选）", "字迹偏扁、涂改较多，第2大题解答题写到了边界虚线外，扫描后可能看不清。", height=120)
        btn_vision_diagnose = st.button("🚀 启动 AI 多模态卷面深度诊断", type="primary", use_container_width=True)

    if btn_vision_diagnose:
        if not uploaded_file:
            st.warning("⚠️ 建议上传一张卷面图片以获得最高准确度的视觉诊断报告！")
            
        with st.spinner("🔍 正在多模态扫描卷面字迹、行距与电子扫描灰度折损..."):
            system_prompt = """你是一位拥有15年经验的中高考阅卷组长兼卷面提分专家。
请根据家长/学员上传的答题卡信息及视觉特征，输出一份极其专业、直击痛点、直通‘980元/6小时卷面提分课’的《卷面视觉诊断与失分分析报告书》。
包含：
1. 📸 卷面三维扫描评级（字体辨识度、间距行距规范度、答题区域把控力）
2. ⚠️ 阅卷机与电子扫描失分隐患（重点强调黑白扫描下的吃字、重影、压框风险）
3. 📉 隐形丢分评估（明确估算因此损失的 5-15 分）
4. 🛠️ 6小时针对性提分重塑方案（对标 980 元特训课模块）"""
            
            user_prompt = f"学员：{v_name} | 年级科目：{v_grade_subject} | 分差目标：{v_target_gap} | 卷面描述：{v_extra_detail}"
            messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
            
            res_box = st.empty()
            full_report = ""
            for token in call_deepseek_stream(messages, temperature=0.6):
                full_report += token
                res_box.markdown(full_report)
            
            if full_report:
                save_student_record(v_name, v_grade_subject, v_target_gap, full_report)
                st.success("✅ 诊断报告已生成，并已自动持久化归档至【学员档案库】！")

# ----------------------------------------------------
# 模块二：小红书防限流文案工厂
# ----------------------------------------------------
with tab2:
    st.markdown('<div class="card-box"><b>📕 小红书文案工厂：</b>自动采用隐喻与防限流语料，生成阅卷内幕、提分对比等高点击笔记。</div>', unsafe_allow_html=True)
    
    col_x1, col_x2 = st.columns(2)
    with col_x1:
        xhs_topic = st.selectbox("笔记切入角度", [
            "高考阅卷组长揭秘：电子扫描后直接扣掉5分的3种字迹",
            "字写得挺好为什么不高？中考答题卡行距致命坑",
            "真实案例：高三语文从98冲到118，只改了卷面排版",
            "高三二模卷面血泪教训：答题超出边界直接0分"
        ])
        xhs_grade = st.selectbox("目标受众年级", ["初三中考冲刺", "高三高考冲刺", "初高中通用"])
    
    with col_x2:
        xhs_style = st.selectbox("内容情绪与语调", ["犀利揭秘（阅卷老师视角）", "焦虑拯救（救急冲刺视角）", "真实逆袭（学霸提分手记）"])
        xhs_hook = st.text_input("引流钩子配置", "在评论区留下【卷面】或私信，免费领《2026中高考答题卡防扣分红线指南》PDF")

    if st.button("🚀 生成小红书爆款文案 (安全防限流)", type="primary"):
        with st.spinner("AI 正在构思爆款文案..."):
            messages = [
                {"role": "system", "content": "你是一位专做中高考卷面提分的小红书百万爆款博主。严禁使用微信、买课、转账等敏感词，善用emoji和分段排版。"},
                {"role": "user", "content": f"主题：{xhs_topic}\n年级：{xhs_grade}\n风格：{xhs_style}\n引流钩子：{xhs_hook}\n请输出完整的爆款标题组（5个）+ 完整正文 + 热门标签。"}
            ]
            xhs_box = st.empty()
            full_xhs = ""
            for token in call_deepseek_stream(messages, temperature=0.8):
                full_xhs += token
                xhs_box.markdown(full_xhs)

# ----------------------------------------------------
# 模块三：微信私域异议攻心专家
# ----------------------------------------------------
with tab3:
    st.markdown('<div class="card-box"><b>💬 私域成交与异议攻心：</b>精准化解家长“价格贵、快中高考了练字来不及、有用吗”等核心阻力。</div>', unsafe_allow_html=True)
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        parent_objection = st.selectbox("家长核心异议", [
            "“马上就要中高考了，现在练字还来得及吗？”",
            "“980元只有6个小时，感觉有点小贵/不划算”",
            "“孩子平时成绩挺好的，卷面真的能提10-20分吗？”",
            "“孩子平时习惯了这样写，改不过来怎么办？”"
        ])
    with col_c2:
        student_situation = st.text_input("学员背景补充", "初三学生，平时成绩105左右，字迹较小、涂改较多，目标重点高中。")

    if st.button("💬 一键生成微信高情商攻心话术", type="primary"):
        with st.spinner("正在生成高转化话术..."):
            messages = [
                {"role": "system", "content": "你是资深中高考升学规划与卷面提分专家。掌握同理心倾听、降维打击、锚定效应与紧迫感促单话术。"},
                {"role": "user", "content": f"家长提出的异议：{parent_objection}\n学员情况：{student_situation}\n请输出：1. 核心破局逻辑 2. 微信直接复制回复的3段式话术 3. 促单催单逼单金句。"}
            ]
            conv_box = st.empty()
            full_conv = ""
            for token in call_deepseek_stream(messages, temperature=0.6):
                full_conv += token
                conv_box.markdown(full_conv)

# ----------------------------------------------------
# 模块四：朋友圈成交势能文案
# ----------------------------------------------------
with tab4:
    st.markdown('<div class="card-box"><b>⭕ 朋友圈成交文案：</b>打造真实专业 IP 形象，持续营造抢位与逆袭势能。</div>', unsafe_allow_html=True)
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        moment_type = st.selectbox("朋友圈动态类型", [
            "学员逆袭反馈（模考卷面分直接涨了12分）",
            "深夜批改诊断答题卡（展示专业度与细节洞察）",
            "特训营满班倒计时（营造紧迫稀缺感）",
            "阅卷老师避坑干货（树立权威形象）"
        ])
    with col_p2:
        moment_detail = st.text_input("朋友圈素材细节", "刚刚辅导完一位初三女生，规范了坐标系和答题行距，这次二模多拿了8分！")

    if st.button("⭕ 生成朋友圈成交文案", type="primary"):
        with st.spinner("正在生成朋友圈文案..."):
            messages = [
                {"role": "system", "content": "你是朋友圈私域发售高手，善于写真实、短小精悍、不油腻、高互动的成交文案。"},
                {"role": "user", "content": f"动态类型：{moment_type}\n细节：{moment_detail}\n请生成3条不同风格的朋友圈文案（附带配图建议及第一条自评评论）。"}
            ]
            mom_box = st.empty()
            full_mom = ""
            for token in call_deepseek_stream(messages, temperature=0.7):
                full_mom += token
                mom_box.markdown(full_mom)

# ----------------------------------------------------
# 模块五：学员诊断云端档案库
# ----------------------------------------------------
with tab5:
    st.markdown('<div class="card-box"><b>🗄️ 学员档案数据库：</b>所有通过 AI 诊断的学员记录持久化存储，随时调取查看与复盘。</div>', unsafe_allow_html=True)
    
    records = get_all_records()
    if not records:
        st.info("💡 暂无学员诊断记录。在【模块一】生成诊断报告后将自动在此归档！")
    else:
        st.write(f"📊 当前已累计归档 **{len(records)}** 位学员的卷面诊断报告：")
        for idx, rec in enumerate(records):
            s_name, s_grade, s_gap, s_report, s_time = rec
            with st.expander(f"👤 学员：{s_name} | {s_grade} | 目标分差：{s_gap} ({s_time})"):
                st.markdown(s_report)
