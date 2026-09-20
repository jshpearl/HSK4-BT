import streamlit as st
import requests
import json
import os

# --- CẤU HÌNH TRANG WEB & UI/UX ---
st.set_page_config(
    page_title="HỆ THỐNG BÀI TẬP HSK4",
    page_icon="📚",
    layout="wide"
)

# --- CSS CAO CẤP: PHỐI MÀU PASTEL XINH ĐẸP, FORCE LIGHT MODE & DÀN HÀNG NGANG BÀI HỌC ---
st.markdown("""
<style>
    /* 1. Nền trang xanh pastel dịu nhẹ lai trắng tinh tế */
    .stApp {
        background-color: #F3F7F4 !important;
    }
    
    /* 2. Ép toàn bộ phông chữ sang màu đen xám / xám đậm sắc nét, chống tàng hình chữ khi bật Dark Mode */
    html, body, p, span:not([aria-hidden="true"]):not([data-testid="stIcon"]), label, li, h1, h2, h3, h4, h5, h6, 
    .stMarkdown, .stWidgetLabel, .stMarkdownContainer p,
    div[data-testid="stMarkdownContainer"] p,
    div[role="radiogroup"] label, div[role="radiogroup"] p,
    div[data-testid="stNotification"] p, div[data-testid="stNotification"] div,
    .st-emotion-cache-1dp5vir, .st-emotion-cache-ue694m,
    .st-emotion-cache-zt5g90, .st-emotion-cache-1kyx60b, .st-emotion-cache-1629630 {
        color: #1A2E22 !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
        font-weight: 600 !important;
        text-shadow: 0.5px 0.5px 1px rgba(0, 0, 0, 0.04) !important;
    }
    
    /* 3. Tiêu đề chính lớn nổi bật */
    h1 {
        color: #1C4430 !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        text-align: center !important;
        margin-bottom: 6px !important;
    }
    
    /* Lời chào dưới tiêu đề */
    .subtitle {
        text-align: center !important;
        font-size: 17px !important;
        color: #386641 !important;
        font-weight: 600 !important;
        margin-bottom: 22px !important;
    }

    /* Khung hiển thị câu hỏi màu nhạt, bo tròn mềm mại, nổi nhẹ */
    .question-card {
        background-color: #FFFFFF !important;
        padding: 22px !important;
        border-radius: 16px !important;
        border: 1.5px solid #D5E4DC !important;
        margin-bottom: 18px !important;
        box-shadow: 0 4px 14px rgba(28, 68, 48, 0.04) !important;
    }

    /* 4. Force Light Mode cho các Form Widgets */
    
    /* Ô lựa chọn (Selectbox / Dropdown) */
    div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #D5E4DC !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #1F2937 !important;
    }
    div[data-baseweb="select"] span {
        color: #1F2937 !important;
        font-weight: 600 !important;
    }
    
    /* Danh sách tùy chọn khi mở Dropdown */
    ul[role="listbox"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #D5E4DC !important;
        border-radius: 10px !important;
    }
    ul[role="listbox"] li {
        background-color: #FFFFFF !important;
        color: #1F2937 !important;
    }
    ul[role="listbox"] li:hover {
        background-color: #EEF5F1 !important;
        color: #1C4430 !important;
    }

    /* Ô nhập văn bản (Text Input & Text Area) */
    div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea {
        background-color: #FFFFFF !important;
        color: #1F2937 !important;
        border: 1.5px solid #D5E4DC !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
    }

    /* Khung code chứa từ vựng gợi ý ở trên đầu bài đọc */
    div[data-testid="stCodeBlock"], code, pre {
        background-color: #FFFFFF !important;
        border: 1.5px solid #D5E4DC !important;
        border-radius: 10px !important;
    }
    div[data-testid="stCodeBlock"] pre {
        background-color: #FFFFFF !important;
        border: none !important;
        padding: 12px !important;
        margin: 0 !important;
    }
    div[data-testid="stCodeBlock"] code, code, pre {
        background-color: #FFFFFF !important;
        color: #1F2937 !important;
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 16px !important;
        font-weight: 700 !important;
    }

    /* Restore Streamlit Icon Fonts to prevent _arrow_right text overlapping */
    [data-testid="stIcon"],
    [data-testid="stExpanderToggleIcon"],
    .material-symbols-outlined,
    .material-symbols-rounded,
    .material-symbols-sharp,
    .material-icons,
    div[data-testid="stExpander"] details summary span[aria-hidden="true"],
    div[data-testid="stExpander"] details summary svg,
    div[data-testid="stExpander"] details summary i {
        font-family: 'Material Symbols Outlined', 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
        font-weight: normal !important;
        text-shadow: none !important;
    }

    /* 5. Khung xổ ra (st.expander) nền trắng chữ đen tuyền rõ nét */
    div[data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #D5E4DC !important;
        border-radius: 14px !important;
        box-shadow: 0 3px 8px rgba(28, 68, 48, 0.03) !important;
    }
    div[data-testid="stExpander"] details summary {
        background-color: #FFFFFF !important;
        color: #1C4430 !important;
        font-weight: 700 !important;
        padding: 12px 16px !important;
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
    }
    div[data-testid="stExpander"] details > div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border-top: 1px solid #EEF5F1 !important;
        padding: 16px !important;
    }
    div[data-testid="stExpander"] details > div p, 
    div[data-testid="stExpander"] details > div span, 
    div[data-testid="stExpander"] details > div strong,
    div[data-testid="stExpander"] details > div div {
        color: #000000 !important;
        font-weight: 600 !important;
    }

    /* 6. CHỌN BÀI HỌC (Pills / SegmentedControl / Radio / Tabs) */

    /* Khung chứa các nút chọn bài */
    div[data-testid="stPills"],
    div[data-testid="stSegmentedControl"],
    div[data-testid="stRadio"] div[role="radiogroup"] {
        gap: 10px !important;
        background-color: transparent !important;
        padding: 4px 0px !important;
        border: none !important;
        display: flex !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
    }

    /* --- NÚT BÀI CHƯA CHỌN (UNSELECTED TABS / PILLS) --- */
    /* Nền tab màu nhạt dịu mát, KHÔNG viền, chữ xám xanh đậm rõ nét */
    div[data-testid="stPills"] button,
    div[data-testid="stSegmentedControl"] button,
    button[data-testid="stBaseButton-pills"],
    button[data-testid="stBaseButton-segmented_control"],
    div[data-testid="stPills"] [role="option"],
    div[data-testid="stPills"] button[aria-selected="false"],
    div[data-testid="stPills"] button[aria-pressed="false"],
    div[data-testid="stSegmentedControl"] button[aria-selected="false"],
    div[data-testid="stRadio"] div[role="radiogroup"] label {
        background-color: #E4EFEA !important;
        color: #234731 !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 9px 20px !important;
        box-shadow: none !important;
        outline: none !important;
        transition: all 0.2s ease !important;
    }

    /* Hover nút chưa chọn */
    div[data-testid="stPills"] button:hover,
    div[data-testid="stSegmentedControl"] button:hover,
    button[data-testid="stBaseButton-pills"]:hover,
    div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
        background-color: #D6E7E0 !important;
        color: #173824 !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* --- NÚT BÀI ĐÃ CHỌN (SELECTED TAB / PILL) --- */
    /* Nền xanh lục bảo sang trọng, chữ trắng nổi bật, KHÔNG viền đỏ/đen */
    div[data-testid="stPills"] button[aria-selected="true"],
    div[data-testid="stPills"] button[aria-pressed="true"],
    div[data-testid="stSegmentedControl"] button[aria-selected="true"],
    div[data-testid="stPills"] [aria-selected="true"],
    button[data-testid="stBaseButton-pills"][aria-selected="true"],
    button[data-testid="stBaseButton-pills"][aria-pressed="true"] {
        background-color: #275338 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 20px !important;
        box-shadow: 0 4px 12px rgba(39, 83, 56, 0.22) !important;
    }

    /* Ép chữ bên trong nút ĐÃ CHỌN sang màu trắng tinh */
    div[data-testid="stPills"] button[aria-selected="true"] p,
    div[data-testid="stPills"] button[aria-selected="true"] span,
    div[data-testid="stPills"] button[aria-pressed="true"] p,
    div[data-testid="stPills"] button[aria-pressed="true"] span,
    button[data-testid="stBaseButton-pills"][aria-selected="true"] p,
    button[data-testid="stBaseButton-pills"][aria-selected="true"] span,
    button[data-testid="stBaseButton-pills"][aria-pressed="true"] p,
    button[data-testid="stBaseButton-pills"][aria-pressed="true"] span {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* Ép chữ bên trong nút CHƯA CHỌN sang màu xám xanh đậm rõ nét */
    div[data-testid="stPills"] button[aria-selected="false"] p,
    div[data-testid="stPills"] button[aria-selected="false"] span,
    div[data-testid="stPills"] button[aria-pressed="false"] p,
    div[data-testid="stPills"] button[aria-pressed="false"] span,
    button[data-testid="stBaseButton-pills"][aria-selected="false"] p,
    button[data-testid="stBaseButton-pills"][aria-selected="false"] span,
    button[data-testid="stBaseButton-pills"][aria-pressed="false"] p,
    button[data-testid="stBaseButton-pills"][aria-pressed="false"] span {
        color: #234731 !important;
        font-weight: 600 !important;
    }

    /* 7. PHẦN TAB PHÂN MÔN (Nghe, Đọc, Viết) */
    div[data-baseweb="tab-list"] {
        gap: 8px !important;
        background-color: #EBF3ED !important;
        padding: 6px !important;
        border-radius: 14px !important;
        border: 1px solid #D0E2D5 !important;
    }
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        color: #386641 !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 8px 20px !important;
        font-size: 15px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #386641 !important;
        color: #FFFFFF !important;
        box-shadow: 0 3px 8px rgba(56, 102, 65, 0.2) !important;
    }

    /* Nút nộp bài thiết kế mượt mà nổi bật */
    div.stButton > button {
        background-color: #275338 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        border-radius: 12px !important;
        padding: 12px 30px !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(39, 83, 56, 0.2) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        background-color: #1C4430 !important;
        box-shadow: 0 6px 16px rgba(28, 68, 48, 0.3) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Ẩn hoàn toàn các ký hiệu, menu và nút Deploy góc trên bên phải */
    header { visibility: hidden !important; height: 0px !important; }
    [data-testid="stHeader"] { display: none !important; }
    .stAppDeployButton { display: none !important; }
    div[data-testid="stDecoration"] { display: none !important; }
    div[data-testid="stStatusWidget"] { display: none !important; }

    /* Định dạng chân trang */
    .footer {
        text-align: center;
        padding: 30px 10px 10px 10px;
        font-size: 16px;
        color: #386641 !important;
        font-weight: bold;
        border-top: 1.5px solid #D5E4DC;
        margin-top: 50px;
    }
</style>
""", unsafe_allow_html=True)

# --- KHỞI TẠO STATE HỌC SINH ---
if 'student_name' not in st.session_state:
    st.session_state.student_name = ""
GSHEET_URL = "https://script.google.com/macros/s/AKfycbwcT6NbCmuSV9BHuj4Ev1GPLHKdG7FJxIa1PkiG63jDVSYEU0W1e0zq-TUi0aID5xfVuQ/exec"

def send_results_to_gsheet(student_name, lesson_title, section_name, score_str):
    payload = {
        "name": student_name,          # Bột: Tên học sinh
        "student_name": student_name,  # Dự phòng
        "lesson": lesson_title,        # Cột: Bài học (e.g. "Bài 16", "Bài 17")
        "lesson_title": lesson_title,  # Dự phòng
        "section": section_name,       # Cột: Phần làm bài (e.g. "PHẦN NGHE")
        "score": score_str             # Cột: Điểm số
    }
    try:
        requests.post(GSHEET_URL, json=payload)
    except:
        pass

# --- HÀM TÌM KIẾM ĐỆ QUY FILE AUDIO TRÊN GITHUB (CHỐNG SẬP TRANG) ---
def find_audio_file(filename_patt):
    # 1. Tìm các folder phổ biến và ghép thử trực tiếp
    for folder in ["audio", "Audio", "AUDIO", "assets", "sound", "sounds", ""]:
        for ext in [".mp3", ".MP3", ".wav", ".WAV", ".m4a", ".M4A"]:
            p = os.path.join(folder, filename_patt + ext) if folder else filename_patt + ext
            if os.path.exists(p):
                return p
                
    # 2. Tìm kiếm đệ quy toàn bộ thư mục dự án
    for root, dirs, files in os.walk("."):
        if any(x in root for x in [".git", ".venv", "__pycache__", ".streamlit"]):
            continue
        for f in files:
            name, ext = os.path.splitext(f)
            if filename_patt.lower() in f.lower() and ext.lower() in [".mp3", ".wav", ".m4a"]:
                return os.path.join(root, f)
    return None

def play_audio(filename_patt):
    found_path = find_audio_file(filename_patt)
    if found_path:
        try:
            with open(found_path, "rb") as f:
                st.audio(f.read(), format="audio/mp3")
        except Exception as e:
            st.error(f"⚠️ Lỗi giải mã tệp âm thanh '{found_path}': {str(e)}")
    else:
        st.warning(f"🎧 Trình phát: Chưa tìm thấy tệp âm thanh chứa kí hiệu '{filename_patt}' trong thư mục dự án của bạn trên GitHub.")
        st.markdown("Vui lòng tải thư mục `audio/` chứa các tệp âm thanh tương ứng lên GitHub của bạn nhé!")

# ==============================================================================
# HÀM HIỂN THỊ CHI TIẾT BÀI 16
# ==============================================================================
def show_lesson_16(student_name):
    # Khởi tạo state riêng cho Bài 16
    if 'l16_l_sub' not in st.session_state: st.session_state.l16_l_sub = False
    if 'l16_r_sub' not in st.session_state: st.session_state.l16_r_sub = False
    if 'l16_w_sub' not in st.session_state: st.session_state.l16_w_sub = False

    t_lis, t_read, t_write = st.tabs(["PHẦN NGHE", "PHẦN ĐỌC", "PHẦN VIẾT"])

    # ------------------ PHẦN NGHE BÀI 16 ------------------
    with t_lis:
        st.markdown("### 一、听力 (Phần nghe)")
        st.markdown("#### **第一部分 (Phần 1) - 判断对错**")
        play_audio("16-1")
        
        q1_5_text = [
            "1. ★ 他知道怎么办签证。",
            "2. ★ 护士工作前要通过考试。",
            "3. ★ 他第一次见女朋友时很放松。",
            "4. ★ 那篇文章写得很精彩。",
            "5. ★ 做得不好时别失望。"
        ]
        q1_5_ans = ["✘", "✔", "✘", "✘", "✔"]
        user_q1_5 = []
        col1, col2 = st.columns(2)
        for i, q_text in enumerate(q1_5_text):
            target_col = col1 if i < 3 else col2
            with target_col:
                st.markdown(f"<div class='question-card'><strong>{q_text}</strong>", unsafe_allow_html=True)
                ans = st.radio(f"Chọn câu {i+1}:", ["Chưa chọn", "✔ (Đúng)", "✘ (Sai)"], key=f"l16_lis_p1_{i}")
                user_q1_5.append(ans)
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### **第二部分 (Phần 2) - 单项选择**")
        play_audio("16-2")
        
        q6_12_options = [
            ["A. 杂志", "B. 成绩单", "C. 报名表", "D. 传真"],
            ["A. 害怕失败", "B. 弹得不好", "C. 没有报名", "D. 没有时间"],
            ["A. 睡不着", "B. 还有工作", "C. 在等人", "D. 在看小说"],
            ["A. 来宾馆", "B. 填表格", "C. 说很满意", "D. 写总结"],
            ["A. 商店", "B. 学校", "C. 公司", "D. 饭馆"],
            ["A. 经历丰富", "B. 非常可怜", "C. 更会打扮", "D. 都很聪明"],
            ["A. 力气很大", "B. 爱看小说", "C. 现在是记者", "D. 去过很多地方"]
        ]
        q6_12_ans = ["B", "C", "D", "B", "C", "A", "D"]
        user_q6_12 = []
        col1, col2 = st.columns(2)
        for i in range(7):
            target_col = col1 if i < 4 else col2
            with target_col:
                st.markdown(f"<div class='question-card'><strong>Câu {i+6}:</strong>", unsafe_allow_html=True)
                ans = st.selectbox(f"Đáp án câu {i+6}:", ["Chưa chọn"] + q6_12_options[i], key=f"l16_lis_p2_{i}")
                user_q6_12.append(ans[0] if ans != "Chưa chọn" else "Chưa chọn")
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### **第三部分 (Phần 3) - 单项选择**")
        play_audio("16-3")
        
        q13_22_options = [
            ["A. 正在排队", "B. 忘了号码", "C. 没有带笔", "D. 要填表格"],
            ["A. 办公室", "B. 书房", "C. 厨房", "D. 门上"],
            ["A. 坐地铁", "B. 坐出租车", "C. 自己开车", "D. 坐公共汽车"],
            ["A. 裤子脏了", "B. 手机坏了", "C. 比赛输了", "D. 足球丢了"],
            ["A. 包", "B. 钥匙", "C. 塑料袋", "D. 书"],
            ["A. 语言学", "B. 经济学", "C. 国际关系", "D. 环境科学"],
            ["A. 冰箱质量", "B. 买洗衣机", "C. 修理汽车", "D. 选择丈夫"],
            ["A. 非常担心", "B. 爱修东西", "C. 不爱逛街", "D. 性格很好"],
            ["A. 上五年级", "B. 不爱学习", "C. 成绩很好", "D. 在写作业"],
            ["A. 很怀疑", "B. 太吵了", "C. 被骗了", "D. 明白了"]
        ]
        q13_22_ans = ["D", "B", "A", "C", "B", "B", "D", "B", "B", "A"]
        user_q13_22 = []
        col1, col2 = st.columns(2)
        for i in range(10):
            target_col = col1 if i < 5 else col2
            with target_col:
                st.markdown(f"<div class='question-card'><strong>Câu {i+13}:</strong>", unsafe_allow_html=True)
                ans = st.selectbox(f"Đáp án câu {i+13}:", ["Chưa chọn"] + q13_22_options[i], key=f"l16_lis_p3_{i}")
                user_q13_22.append(ans[0] if ans != "Chưa chọn" else "Chưa chọn")
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 NỘP BÀI PHẦN NGHE", key="l16_btn_sub_lis"):
            if not student_name.strip():
                st.error("⚠️ Bạn hãy điền Họ và tên học sinh ở đầu trang trước khi nộp nhé!")
            else:
                correct_cnt = 0
                for i in range(5):
                    u_v = "✔" if "✔" in user_q1_5[i] else "✘" if "✘" in user_q1_5[i] else "Chưa chọn"
                    if u_v == q1_5_ans[i]: correct_cnt += 1
                for i in range(7):
                    if user_q6_12[i] == q6_12_ans[i]: correct_cnt += 1
                for i in range(10):
                    if user_q13_22[i] == q13_22_ans[i]: correct_cnt += 1
                st.session_state.l16_l_sub = True
                st.session_state.l16_l_score = f"{correct_cnt}/22"
                st.success(f"Chúc mừng bạn đã làm xong bài tập nha. Điểm số của bạn là: {st.session_state.l16_l_score}.")
                send_results_to_gsheet(student_name, "Bài 16", "PHẦN NGHE", st.session_state.l16_l_score)

        if st.session_state.l16_l_sub:
            st.markdown("### 🔍 CHI TIẾT CÂU SAI & ĐÁP ÁN ĐÚNG:")
            # Phần 1 giải thích sai
            for i in range(5):
                u_v = "✔" if "✔" in user_q1_5[i] else "✘" if "✘" in user_q1_5[i] else "Chưa chọn"
                if u_v != q1_5_ans[i]:
                    st.markdown(f"<span style='color:#D32F2F;'>❌ Câu {i+1} sai:</span> {q1_5_text[i]}", unsafe_allow_html=True)
                    st.markdown(f"👉 Đáp án đúng: **{q1_5_ans[i]}**")
                    with st.expander(f"📖 Xem Lời thoại (Script) Câu {i+1}"):
                        scripts = [
                            "办签证需要准备哪些材料，我也不太清楚，不过我有大使馆的电话号码，我可以帮你问一下。\n(Tôi cũng không rõ cần chuẩn bị giấy tờ gì để làm visa, nhưng tôi có số điện thoại của Đại sứ quán, để tôi hỏi giúp bạn.)",
                            "只有通过了考试，完全符合要求后，护士才能正式开始工作。医院对护士这一职业的要求是：专业、负责、尊重生命。\n(Chỉ sau khi vượt qua kỳ thi và hoàn toàn đáp ứng yêu cầu, y tá mới có thể chính thức bắt đầu làm việc.)",
                            "第一次跟女朋友见面的时候，他紧张极了，脸和耳朵都红了，几乎不敢看女朋友的眼睛。\n(Lần đầu gặp bạn gái, anh ấy vô cùng căng thẳng, mặt và tai đều đỏ bừng, hầu như không dám nhìn vào mắt cô ấy.)",
                            "这篇文章你还得拿回去好好改改，主要是内容有点儿乱，重点不够清楚，另外，有几个句子还有语法问题。\n(Bài viết này bạn phải mang về sửa lại thật kỹ, chủ yếu là nội dung hơi lộn xộn, trọng tâm chưa rõ ràng, ngoài ra một số câu còn gặp vấn đề ngữ pháp.)",
                            "受到批评时，也别伤心失望，谁都有做错事或者做得不够好的时候。只要不放弃努力，你就仍然有希望。\n(Khi bị phê bình thì cũng đừng đau lòng thất vọng, ai cũng có lúc làm sai hoặc làm chưa đủ tốt. Chỉ cần không từ bỏ nỗ lực, bạn vẫn luôn có hy vọng.)"
                        ]
                        st.markdown(scripts[i])

    # ------------------ PHẦN ĐỌC BÀI 16 ------------------
    with t_read:
        st.markdown("### 二、阅读 (Phần đọc)")
        st.markdown("#### **第一部分 (Phần 1) - 选词填空**")
        st.markdown("**第 23-26 题：**")
        st.code("A 冷静    B 尊重    C 敢    D 坚持    E 呀")
        
        q23_26_texts = [
            "23. 哥，你快来看，这是什么植物（ ）？\n叶子怎么这么宽？",
            "24. 做事情不要一开始就考虑太多，害怕失败，\n什么都不（ ）做怎么可能成功？",
            "25. 邀请别人吃饭，至少要提前一天联系。\n首先，这是对被邀请人表示（ ）；\n其次，也方便别人做好安排。",
            "26. 当事情没有按照原来的计划进行时，不要太着急、太担心，\n而应该使自己（ ）下来，态度积极地去想解决问题的办法。"
        ]
        q23_26_ans = ["E", "C", "B", "A"]
        user_q23_26 = []
        col1, col2 = st.columns(2)
        for i, q_text in enumerate(q23_26_texts):
            target_col = col1 if i < 2 else col2
            with target_col:
                st.markdown(f"<div class='question-card'><strong>{q_text}</strong>", unsafe_allow_html=True)
                ans = st.selectbox(f"Từ điền câu {i+23}:", ["Chưa chọn", "A. 冷静", "B. 尊重", "C. 敢", "D. 坚持", "E. 呀"], key=f"l16_read_p1_1_{i}")
                user_q23_26.append(ans[0] if ans != "Chưa chọn" else "Chưa chọn")
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("**第 27-30 题：**")
        st.code("A 激动    B 挂    C 温度    D 报名    E 郊区")
        q27_30_texts = [
            "27. A：我那件红衬衫呢？你放哪儿了？\nB：洗了，在外边（ ）着，还没干呢。你穿这件就很好，很精神。",
            "28. A：去植物园玩儿的同事一共是十二位，现在还有人要（ ）吗？\nB：我也想去。明天我们大概去多长时间？几点能回来呢？",
            "29. A：外面雪下得这么大，那些小伙子们怎么都跑外边去了？\nB：他们都是南方人，南方冬天很少下雪，更不用说这么大的雪，所以他们肯定特别（      ）。",
            "30. A：现在城市里越来越多的人喜欢到（ ）过周末了。\nB：是啊，那里空气新鲜、环境安静，可以让人好好放松一下。"
        ]
        q27_30_ans = ["B", "D", "A", "E"]
        user_q27_30 = []
        for i, q_text in enumerate(q27_30_texts):
            target_col = col1 if i < 2 else col2
            with target_col:
                st.markdown(f"<div class='question-card'><strong>{q_text}</strong>", unsafe_allow_html=True)
                ans = st.selectbox(f"Từ điền câu {i+27}:", ["Chưa chọn", "A. 激动", "B. 挂", "C. 温度", "D. 报名", "E. 郊区"], key=f"l16_read_p1_2_{i}")
                user_q27_30.append(ans[0] if ans != "Chưa chọn" else "Chưa chọn")
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### **第二部分 (Phần 2) - 排列顺序**")
        q31_34_texts = [
            "31.\n\nA. 因此，预习是学习的第一步\n\nB. 上课的时候，学习效果才会更好\n\nC. 提前对要学的内容有个大概的了解",
            "32.\n\nA. 结果眼睛越来越不好\n\nB. 所以现在我不敢再躺着看书了\n\nC. 拿我来说，小时候我总喜欢躺在床上看书",
            "33.\n\nA. 我们还是把它推到里面去吧\n\nB. 沙发太大了，放这儿容易堵着门，进出不方便\n\nC. 把这个地方空出来",
            "34.\n\nA. 也许你会发现， 这些事情其实用不着烦恼\n\nB. 每次发脾气前，请先给自己几分钟\n\nC. 冷静地想一想，是不是值得为此生气"
        ]
        q31_34_ans = ["CBA", "CAB", "BAC", "BCA"]
        user_q31_34 = []
        for i, q_text in enumerate(q31_34_texts):
            st.markdown(f"<div class='question-card'>{q_text}", unsafe_allow_html=True)
            ans = st.text_input(f"Thứ tự câu {i+31} (Ví dụ: ABC):", key=f"l16_read_p2_{i}").strip().upper()
            user_q31_34.append(ans)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### **第三部分 (Phần 3) - 阅读理解**")
        q35_43_questions = [
            "35. 每年有成千上万的高中毕业生报名参加电影学院的艺术考试，\n\n他们中很多人都抱着成为著名演员的理想，\n\n但其实大部分考生并不清楚表演到底是什么。\n\n★ 根据这段话，很多考生：",
            "36. 举办这次活动，主要是为了向大家介绍我们公司推出的最新手机，\n\n希望通过这次活动引起大家的兴趣，\n\n让大家更了解我们。\n\n★ 举办这次活动是为了：",
            "37. 在别人伤心难过的时候，我们总会对他/她表示同情。\n\n同情是最美好的情感之一，然而同情并不是高高在上的关心，\n\n它应该是对别人的理解、尊重和支持。\n\n★ 这段话认为，同情别人：",
            "38. 现在的输或者赢都只是暂时的，没有人会永远输，\n\n也没有人会一直赢。\n\n生活的关键就是：只要你敢想、敢做、积极努力了，\n\n那么无论是输还是赢，生活都一样精彩。\n\n★ 根据这段话，可以知道：",
            "39. 耳朵每天都帮助我们听到各种各样的声音，\n\n但我们可不像重视眼睛、鼻子那样重视它。\n\n很多时候人们常常感觉不到它，甚至忘记了它。\n\n其实我们都错了，有研究发现，通过耳朵可以看出一个人是不是健康，\n\n甚至是什么样的性格。\n\n★ 这段话主要讲：",
            "[40-41] “我找林医生，我有急事！”一位妈妈非常着急地给林医生打电话，\n\n林医生的妻子接的电话。\n\n“他刚出去了，您有什么事吗？”\n\n“天哪，我的小儿子刚才把我的手表吃到肚子里了，林医生什么时候能回来？”\n\n“两个小时左右。”医生的妻子回答。\n\n“两个小时！这段时间我该怎么办呀？”\n\n“我很抱歉，您恐怕只能先用另一块儿手表了。”\n\n40. ★ 孩子怎么了？",
            "41. ★ 关于林医生，可以知道什么？",
            "[42-43] 父母是孩子第一位老师，也是最重要的老师。\n\n父母不仅要帮助孩子认识世界，教会他们知识，\n\n还应该帮助孩子养成好的生活习惯，比如睡前刷牙、节约用水。\n\n另外，还要教会他们懂礼貌、对人诚实。\n\n这些都需要父母的耐心教育。\n\n孩子习惯的养成会受到父母的影响，\n\n所以做父母的平时一定要注意自己的言行。\n\n42. ★ 根据这段话，父母有什么责任？",
            "43. ★ 根据这段话，孩子习惯的养成："
        ]
        q35_43_options = [
            ["A. 年龄比较大", "B. 成绩很优秀", "C. 不理解表演", "D. 已经是演员"],
            ["A. 比赛", "B. 打折", "C. 积累经验", "D. 介绍手机"],
            ["A. 不值得做", "B. 非常可惜", "C. 会让人难过", "D. 是表示支持"],
            ["A. 耐心非常重要", "B. 生活会很精彩", "C. 输和赢不重要", "D. 要多参加活动"],
            ["A. 有趣的鼻子", "B. 怎样保护眼睛", "C. 重新认识耳朵", "D. 怎样打扮自己"],
            ["A. 很想买手表", "B. 突然流血了", "C. 把药吃错了", "D. 把手表吃了"],
            ["A. 不在家", "B. 很伤心", "C. 表丢了", "D. 不负责"],
            ["A. 保护孩子安全", "B. 教育孩子", "C. 回答问题", "D. 替孩子做决定"],
            ["A. 过程会很慢", "B. 会比较轻松", "C. 与年龄有关", "D. 受父母影响"]
        ]
        q35_43_ans = ["C", "D", "D", "C", "C", "D", "A", "B", "D"]
        user_q35_43 = []
        for i in range(9):
            st.markdown(f"<div class='question-card'>{q35_43_questions[i]}", unsafe_allow_html=True)
            ans = st.selectbox(f"Đáp án câu {i+35}:", ["Chưa chọn"] + q35_43_options[i], key=f"l16_read_p3_{i}")
            user_q35_43.append(ans[0] if ans != "Chưa chọn" else "Chưa chọn")
            st.markdown("</div>", unsafe_allow_html=True)

        if st.button("🚀 NỘP BÀI PHẦN ĐỌC", key="l16_btn_sub_read"):
            if not student_name.strip():
                st.error("⚠️ Bạn hãy điền Họ và tên học sinh ở đầu trang trước khi nộp nhé!")
            else:
                correct_cnt = 0
                for i in range(4):
                    if user_q23_26[i] == q23_26_ans[i]: correct_cnt += 1
                for i in range(4):
                    if user_q27_30[i] == q27_30_ans[i]: correct_cnt += 1
                for i in range(4):
                    if user_q31_34[i] == q31_34_ans[i]: correct_cnt += 1
                for i in range(9):
                    if user_q35_43[i] == q35_43_ans[i]: correct_cnt += 1
                st.session_state.l16_r_sub = True
                st.session_state.l16_r_score = f"{correct_cnt}/21"
                st.success(f"Chúc mừng bạn đã làm xong bài tập nha. Điểm số của bạn là: {st.session_state.l16_r_score}.")
                send_results_to_gsheet(student_name, "Bài 16", "PHẦN ĐỌC", st.session_state.l16_r_score)

        if st.session_state.l16_r_sub:
            st.markdown("### 🔍 CHI TIẾT CÂU SAI & ĐÁP ÁN ĐÚNG:")
            for i in range(4):
                if user_q23_26[i] != q23_26_ans[i]:
                    st.markdown(f"<span style='color:#D32F2F;'>❌ Câu {i+23} sai:</span> {q23_26_texts[i]}", unsafe_allow_html=True)
                    st.markdown(f"👉 Đáp án đúng: **{q23_26_ans[i]}**")
            for i in range(4):
                if user_q27_30[i] != q27_30_ans[i]:
                    st.markdown(f"<span style='color:#D32F2F;'>❌ Câu {i+27} sai:</span> {q27_30_texts[i]}", unsafe_allow_html=True)
                    st.markdown(f"👉 Đáp án đúng: **{q27_30_ans[i]}**")

    # ------------------ PHẦN VIẾT BÀI 16 ------------------
    with t_write:
        st.markdown("### 三、书写 (Phần viết)")
        st.markdown("#### **第一部分 (Phần 1) - Sắp xếp câu hoàn chỉnh**")
        st.warning("⚠️ Chú ý: Phần viết được chấm tuyệt đối nghiêm ngặt. Sai bất kỳ 1 chữ hoặc 1 dấu câu nào cũng tính là sai hoàn toàn cả câu.")
        
        q44_48_words = [
            "44. 200 / 估计 / 王老师 / 报名人数 / 会 / 超过",
            "45. 传真号码 / 是 / 你们 / 多少 / 公司 / 的",
            "46. 请 / 帮我 / 一个 / 当地导游 / 你能 / 吗",
            "47. 失望 / 让 / 那个 / 很 / 电影 / 观众",
            "48. 是 / 好消息 / 激动人心的 / 实在 / 一个 / 这"
        ]
        q44_48_acceptable_ans = [
            ["王老师估计报名人数会超过200。", "估计王老师报名人数会超过200。"],
            ["你们公司的传真号码是多少？", "你们公司传真号码是多少？"],
            ["你能帮我请一个当地导游吗？", "你能帮我请个当地导游吗？"],
            ["那个电影让观众很失望。"],
            ["这实在是一个激动人心的好消息。", "这实在是个激动人心的好消息。"]
        ]
        user_q44_48 = []
        for i, words in enumerate(q44_48_words):
            st.markdown(f"<div class='question-card'><strong>Câu {i+44}:</strong> {words}", unsafe_allow_html=True)
            ans = st.text_input("Nhập câu hoàn chỉnh của bạn tại đây:", key=f"l16_write_p1_{i}").strip()
            user_q44_48.append(ans)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### **第二部分 (Phần 2) - Nhìn tranh đặt câu (Tự luận đối chiếu gợi ý)**")
        st.markdown("<div class='question-card'><strong>Câu 49:</strong> Tranh người thanh niên chơi bóng rổ. Từ gợi ý: <strong>小伙子</strong></div>", unsafe_allow_html=True)
        user_q49 = st.text_area("Viết câu của bạn:", key="l16_write_p2_49")
        st.markdown("<div class='question-card'><strong>Câu 50:</strong> Tranh cầm bút điền vào bảng đơn. Từ gợi ý: <strong>表格</strong></div>", unsafe_allow_html=True)
        user_q50 = st.text_area("Viết câu của bạn:", key="l16_write_p2_50")

        if st.button("🚀 NỘP BÀI PHẦN VIẾT", key="l16_btn_sub_write"):
            if not student_name.strip():
                st.error("⚠️ Bạn hãy điền Họ và tên học sinh ở đầu trang trước khi nộp nhé!")
            else:
                correct_cnt = 0
                for i in range(5):
                    user_ans = user_q44_48[i].strip()
                    matched = False
                    for possible_ans in q44_48_acceptable_ans[i]:
                        if user_ans == possible_ans.strip():
                            matched = True
                            break
                    if matched: correct_cnt += 1
                st.session_state.l16_w_sub = True
                st.session_state.l16_w_score = f"{correct_cnt}/5"
                st.success(f"Chúc mừng bạn đã làm xong bài tập nha. Điểm số của bạn là: {st.session_state.l16_w_score}.")
                send_results_to_gsheet(student_name, "Bài 16", "PHẦN VIẾT", st.session_state.l16_w_score)

        if st.session_state.l16_w_sub:
            st.markdown("### 🔍 CHI TIẾT CÂU SAI & ĐÁP ÁN ĐÚNG:")
            for i in range(5):
                user_ans = user_q44_48[i].strip()
                matched = False
                for possible_ans in q44_48_acceptable_ans[i]:
                    if user_ans == possible_ans.strip():
                        matched = True
                        break
                if not matched:
                    st.markdown(f"<span style='color:#D32F2F;'>❌ Câu {i+44} viết chưa chính xác:</span>", unsafe_allow_html=True)
                    st.markdown(f"Đáp án của bạn: `{user_q44_48[i]}`")
                    st.markdown(f"👉 Đáp án đúng: **{q44_48_acceptable_ans[i][0]}**")


# ==============================================================================
# HÀM HIỂN THỊ CHI TIẾT BÀI 17
# ==============================================================================
def show_lesson_17(student_name):
    # Khởi tạo state riêng cho Bài 17
    if 'l17_l_sub' not in st.session_state: st.session_state.l17_l_sub = False
    if 'l17_r_sub' not in st.session_state: st.session_state.l17_r_sub = False
    if 'l17_w_sub' not in st.session_state: st.session_state.l17_w_sub = False

    t_lis, t_read, t_write = st.tabs(["PHẦN NGHE", "PHẦN ĐỌC", "PHẦN VIẾT"])

    # ------------------ PHẦN NGHE BÀI 17 ------------------
    with t_lis:
        st.markdown("### 一、听力 (Phần nghe)")
        st.markdown("#### **第一部分 (Phần 1) - 判断对错**")
        play_audio("17-1")
        
        q1_5_text = [
            "1. ★ 秋季不适合去黄山。",
            "2. ★ 地图上蓝色表示海洋。",
            "3. ★ 开车时听广播很不安全。",
            "4. ★ 海洋里的植物很少。",
            "5. ★ 明天是中秋节。"
        ]
        q1_5_ans = ["✘", "✔", "✘", "✘", "✘"]
        user_q1_5 = []
        col1, col2 = st.columns(2)
        for i, q_text in enumerate(q1_5_text):
            target_col = col1 if i < 3 else col2
            with target_col:
                st.markdown(f"<div class='question-card'><strong>{q_text}</strong>", unsafe_allow_html=True)
                ans = st.radio(f"Chọn câu {i+1}:", ["Chưa chọn", "✔ (Đúng)", "✘ (Sai)"], key=f"l17_lis_p1_{i}")
                user_q1_5.append(ans)
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### **第二部分 (Phần 2) - 单项选择**")
        play_audio("17-2")
        
        q6_12_options = [
            ["A. 入口很远", "B. 应该右拐", "C. 女的在问路", "D. 海洋馆很好"],
            ["A. 想请假", "B. 被表扬了", "C. 受到邀请了", "D. 要写计划书"],
            ["A. 没有精神", "B. 发烧了", "C. 适应环境", "D. 肚子饿了"],
            ["A. 地铁站", "B. 机场", "C. 公交站", "D. 火车站"],
            ["A. 做生意很容易", "B. 比赛非常精彩", "C. 价格已经最低", "D. 竞争也有好处"],
            ["A. 回趟家", "B. 去国外", "C. 看奶奶", "D. 准备考试"],
            ["A. 电影票免费", "B. 票还没买", "C. 女的下午有事", "D. 电影很精彩"]
        ]
        q6_12_ans = ["C", "D", "A", "C", "D", "D", "B"]
        user_q6_12 = []
        col1, col2 = st.columns(2)
        for i in range(7):
            target_col = col1 if i < 4 else col2
            with target_col:
                st.markdown(f"<div class='question-card'><strong>Câu {i+6}:</strong>", unsafe_allow_html=True)
                ans = st.selectbox(f"Đáp án câu {i+6}:", ["Chưa chọn"] + q6_12_options[i], key=f"l17_lis_p2_{i}")
                user_q6_12.append(ans[0] if ans != "Chưa chọn" else "Chưa chọn")
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### **第三部分 (Phần 3) - 单项选择**")
        play_audio("17-3")
        
        q13_22_options = [
            ["A. 喜欢照相", "B. 五岁了", "C. 有个哥哥", "D. 个子不高"],
            ["A. 公园", "B. 餐厅", "C. 超市", "D. 宾馆"],
            ["A. 下雨了", "B. 在下雪", "C. 很暖和", "D. 刮风了"],
            ["A. 地球大小", "B. 海水颜色", "C. 节约用水", "D. 空气污染"],
            ["A. 害怕失败", "B. 还没输过", "C. 不太会打", "D. 没有男的好"],
            ["A. 植物园", "B. 卧室", "C. 院子里", "D. 南方"],
            ["A. 植物学", "B. 医学", "C. 历史学", "D. 动物学"],
            ["A. 自然", "B. 节目", "C. 老虎", "D. 亚洲"],
            ["A. 寒假", "B. 暑假", "C. 每天中午", "D. 每月15号"],
            ["A. 天气太热", "B. 地方太小", "C. 提前下班", "D. 保证安全"]
        ]
        q13_22_ans = ["C", "A", "B", "C", "B", "C", "D", "C", "B", "D"]
        user_q13_22 = []
        col1, col2 = st.columns(2)
        for i in range(10):
            target_col = col1 if i < 5 else col2
            with target_col:
                st.markdown(f"<div class='question-card'><strong>Câu {i+13}:</strong>", unsafe_allow_html=True)
                ans = st.selectbox(f"Đáp án câu {i+13}:", ["Chưa chọn"] + q13_22_options[i], key=f"l17_lis_p3_{i}")
                user_q13_22.append(ans[0] if ans != "Chưa chọn" else "Chưa chọn")
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 NỘP BÀI PHẦN NGHE", key="l17_btn_sub_lis"):
            if not student_name.strip():
                st.error("⚠️ Bạn hãy điền Họ và tên học sinh ở đầu trang trước khi nộp nhé!")
            else:
                correct_cnt = 0
                for i in range(5):
                    u_v = "✔" if "✔" in user_q1_5[i] else "✘" if "✘" in user_q1_5[i] else "Chưa chọn"
                    if u_v == q1_5_ans[i]: correct_cnt += 1
                for i in range(7):
                    if user_q6_12[i] == q6_12_ans[i]: correct_cnt += 1
                for i in range(10):
                    if user_q13_22[i] == q13_22_ans[i]: correct_cnt += 1
                st.session_state.l17_l_sub = True
                st.session_state.l17_l_score = f"{correct_cnt}/22"
                st.success(f"Chúc mừng bạn đã làm xong bài tập nha. Điểm số của bạn là: {st.session_state.l17_l_score}.")
                send_results_to_gsheet(student_name, "Bài 17", "PHẦN NGHE", st.session_state.l17_l_score)

        if st.session_state.l17_l_sub:
            st.markdown("### 🔍 CHI TIẾT CÂU SAI & ĐÁP ÁN ĐÚNG:")
            for i in range(5):
                u_v = "✔" if "✔" in user_q1_5[i] else "✘" if "✘" in user_q1_5[i] else "Chưa chọn"
                if u_v != q1_5_ans[i]:
                    st.markdown(f"<span style='color:#D32F2F;'>❌ Câu {i+1} sai:</span> {q1_5_text[i]}", unsafe_allow_html=True)
                    st.markdown(f"👉 Đáp án đúng: **{q1_5_ans[i]}**")
                    with st.expander(f"📖 Xem Lời thoại (Script) Câu {i+1}"):
                        scripts = [
                            "我觉得秋天是去黄山的最好季节，因为这时候天气不冷也不热，而且山上的树叶有很多种颜色，绿的、黄的、红的，漂亮极了。\n(Tôi thấy mùa thu là mùa đẹp nhất để đi Hoàng Sơn, vì lúc này trời không nóng cũng không lạnh, và lá cây trên núi có rất nhiều màu sắc, vàng, xanh, đỏ, vô cùng xinh đẹp.)",
                            "儿子，你看，地图上不同的颜色表示不同的地方，绿色的是森林，蓝色的是海洋。\n(Con trai nhìn này, màu sắc khác nhau trên bản đồ đại diện cho các vùng đất khác nhau, màu xanh lá cây là rừng rậm, màu xanh da trời là đại dương.)",
                            "很多司机都喜欢开车时听广播，因为通过听广播，他们不但可以了解路上的堵车情况，而且开车时也不会觉得太无聊。\n(Rất nhiều tài xế đều thích nghe radio khi lái xe, vì qua đó họ không chỉ biết được tình trạng tắc đường mà còn không cảm thấy quá tẻ nhạt.)",
                            "和森林一样，在海洋里也有很多种植物，它们与海洋里的动物，共同组成了一个海底世界。\n(Cũng giống như rừng rậm, trong đại dương có rất nhiều loại thực vật, chúng cùng động vật biển cấu thành một thế giới dưới lòng đại dương.)",
                            "昨天是中秋节，这一天的月亮应该是一年中最大最亮的。但是让人失望的是，昨天的月亮一直在厚厚的云层后面睡觉，我们什么也看不见。\n(Hôm qua là tết Trung thu, trăng hôm qua đáng lẽ phải to nhất sáng nhất năm, nhưng đáng tiếc là mặt trăng trốn sau đám mây dày ngủ say, chúng ta chả nhìn thấy gì.)"
                        ]
                        st.markdown(scripts[i])

    # ------------------ PHẦN ĐỌC BÀI 17 ------------------
    with t_read:
        st.markdown("### 二、阅读 (Phần đọc)")
        st.markdown("#### **第一部分 (Phần 1) - 选词填空**")
        st.markdown("**第 23-26 题：**")
        st.code("A 严格    B 梦    C 抱    D 坚持    E 入口")
        
        q23_26_texts = [
            "23. 小姐，您的包不能带入馆内。\n\n（      ） 处有专门存包的地方，您可以把包放在那儿。",
            "24. 有的父母为了让孩子更好地发展而对孩子从小就\n\n（      ） 要求，却忘记了快乐地生活对孩子才是最重要的。",
            "25. 小时候，我们往往会有许多浪漫的理想。\n\n但是随着年龄的增长，我们天天忙工作、忙生活，\n\n那些（      ） 慢慢地离我们远去了。",
            "26. 在昨天的羽毛球男子双打比赛中，小马和小张最后赢了比赛。\n\n赛后 他们激动地（      ） 在了一起。"
        ]
        q23_26_ans = ["E", "A", "B", "C"]
        user_q23_26 = []
        col1, col2 = st.columns(2)
        for i, q_text in enumerate(q23_26_texts):
            target_col = col1 if i < 2 else col2
            with target_col:
                st.markdown(f"<div class='question-card'><strong>{q_text}</strong>", unsafe_allow_html=True)
                ans = st.selectbox(f"Từ điền câu {i+23}:", ["Chưa chọn", "A. 严格", "B. 梦", "C. 抱", "D. 坚持", "E. 入口"], key=f"l17_read_p1_1_{i}")
                user_q23_26.append(ans[0] if ans != "Chưa chọn" else "Chưa chọn")
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("**第 27-30 题：**")
        st.code("A 剩    B 趟    C 干 (gàn)    D 温度    E 照")
        q27_30_texts = [
            "27. A：站在这儿（      ） 什么？\n\n怎么不进去？忘拿东西了？\n\nB：没有，我在等我儿子，我要带他去公园玩儿。",
            "28. A：（      ） 了这么多菜没吃完，太浪费了。\n\nB：让服务员拿几个盒子来，我们 都带回去吧。",
            "29. A：这张照片在哪儿（      ） 的？真漂亮！\n\nB：中山公园。最近天气暖和了，好多花儿都开了。",
            "30. A：王小姐，辛苦你了，让你周末还跑一（      ）。\n\nB：不用客气，我正好经过这儿，就顺便给您带来了。"
        ]
        q27_30_ans = ["C", "A", "E", "B"]
        user_q27_30 = []
        for i, q_text in enumerate(q27_30_texts):
            target_col = col1 if i < 2 else col2
            with target_col:
                st.markdown(f"<div class='question-card'><strong>{q_text}</strong>", unsafe_allow_html=True)
                ans = st.selectbox(f"Từ điền câu {i+27}:", ["Chưa chọn", "A. 剩", "B. 趟", "C. 干 (gàn)", "D. 温度", "E. 照"], key=f"l17_read_p1_2_{i}")
                user_q27_30.append(ans[0] if ans != "Chưa chọn" else "Chưa chọn")
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### **第二部分 (Phần 2) - 排列顺序**")
        q31_34_texts = [
            "31.\n\nA. 不但能看到小鱼 在河里游来游去\n\nB. 这儿的河水仍然非常干净，站在河边\n\nC. 还能看到河底绿绿的水草",
            "32.\n\nA. 这次艺术节吸引了 3000 多人参加\n\nB. 是参加人数最多的一次\n\nC. 京剧艺术节于 9 月 21 日 在北京举办",
            "33.\n\nA. 森林是大自然不可缺少的一部分\n\nB. 我觉得这张画主要是想告诉人们\n\nC. 保护森林就是在保护地球，保护 我们共同的家",
            "34.\n\nA. 我来北京两年了，却还没去过长城\n\nB. 所以我打算这个周末去一趟\n\nC. 有人说没去过长城就不算来过北京"
        ]
        q31_34_ans = ["BAC", "CAB", "BAC", "CAB"]
        user_q31_34 = []
        for i, q_text in enumerate(q31_34_texts):
            st.markdown(f"<div class='question-card'>{q_text}", unsafe_allow_html=True)
            ans = st.text_input(f"Thứ tự câu {i+31} (Ví dụ: ABC):", key=f"l17_read_p2_{i}").strip().upper()
            user_q31_34.append(ans)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### **第三部分 (Phần 3) - 阅读理解**")
        q35_43_questions = [
            "35. 我向大家介绍一下，我们前面看到的就是“老虎山”。\n\n为什么叫这个名字呢？\n\n不是因为山里有老虎，而是 因为从山脚下向上看，山很像一只老虎。\n\n★ 关于“老虎山”，可以知道：",
            "36. 社会的发展不能光看经济的发展，还要重视环境的保护。\n\n环境 如果被污染了，经济的发展 也无法为我们带来美好的生活。\n\n★ 这段话主要谈经济发展 和什么的关系？",
            "37. 当地球上的空气还不适合生命出现的时候，海洋中就已经出现了生命。\n\n海洋中的水对生命有保护作用，生命在海水中不容易受到坏的环境的影响。\n\n★ 生命先出现在海洋里的原因是海水：",
            "38. 很多人常为了昨天的事而烦恼，也常为了明天的事而担心，生活得并不快乐。\n\n在这一点上，动物有很多值得人 学习的地方。\n\n拿猫来说吧，它们该睡觉的时候睡觉，该吃饭的时候吃饭，好像一点儿烦恼都没有。\n\n如果人们能有它们那样的生活态度，一定会健康快乐很多。\n\n★ 根据这段话，人们应该怎么生活？",
            "39. 很多人害怕与周围的人比较，比较不但让失败的人更难受，\n\n而且让 那些成功的人感到有压力，因为肯定还有比 他们更成功的人。\n\n但是从另一方面来看，通过比较可以发现自己的优点、缺点，\n\n使自己取得更大的成绩。\n\n★ 比较的好处是可以：",
            "[40-41] 由于气候条件不同，世界各地植物叶子的样子也很不相同。\n\n在暖和而且空气水分很多的地方，叶子往往长得又宽又厚；\n\n在比较干、阳光特别厉害的地方，因为空气中水分少，\n\n当地植物 的叶子就会长得又瘦又长，有的甚至像针一样。\n\n40. ★ 世界各地植物叶子不同与什么有关？",
            "41. ★ 暖和、水分多的地方，植物叶子：",
            "[42-43] 我们虽然完全不懂小鸟的叫声代表什么意思，但仍然可能觉得很好听。\n\n虽然有的画儿看来去也看不懂，可是仍然可能觉得很美。\n\n其实美一直都在我们身边，在我们的眼睛里，\n\n尽管 我们不清楚美到底是什么，但美从来不会因为人们不懂而改变。\n\n只要我们长着一双发现美的眼睛，美就无处不在。\n\n42. ★ 美有什么特点？",
            "43. ★ 根据这段话，我们应该："
        ]
        q35_43_options = [
            ["A. 看起来像老虎", "B. 里面有动物园", "C. 只有一个入口", "D. 有很多种植物"],
            ["A. 历史文化", "B. 科学发展", "C. 环境保护", "D. 城市管理"],
            ["A. 很暖和", "B. 有吃的", "C. 能改变环境", "D. 能保护它们"],
            ["A. 多考虑将来", "B. 别忘记以前", "C. 跟动物一样", "D. 不要想太多"],
            ["A. 引起竞争", "B. 赢得同情", "C. 原谅别人", "D. 了解自己"],
            ["A. 长的速度", "B. 气候条件", "C. 经济发展", "D. 植物间的距离"],
            ["A. 很长", "B. 很宽", "C. 很亮", "D. 很多"],
            ["A. 有清楚的意思", "B. 有相同的标准", "C. 很容易被理解", "D. 不因为人改变"],
            ["A. 学习跟鸟交流", "B. 从画中理解美", "C. 欣赏身边的美", "D. 好好保护眼睛"]
        ]
        q35_43_ans = ["A", "C", "D", "D", "D", "B", "B", "D", "C"]
        user_q35_43 = []
        for i in range(9):
            st.markdown(f"<div class='question-card'>{q35_43_questions[i]}", unsafe_allow_html=True)
            ans = st.selectbox(f"Đáp án câu {i+35}:", ["Chưa chọn"] + q35_43_options[i], key=f"l17_read_p3_{i}")
            user_q35_43.append(ans[0] if ans != "Chưa chọn" else "Chưa chọn")
            st.markdown("</div>", unsafe_allow_html=True)

        if st.button("🚀 NỘP BÀI PHẦN ĐỌC", key="l17_btn_sub_read"):
            if not student_name.strip():
                st.error("⚠️ Bạn hãy điền Họ và tên học sinh ở đầu trang trước khi nộp nhé!")
            else:
                correct_cnt = 0
                for i in range(4):
                    if user_q23_26[i] == q23_26_ans[i]: correct_cnt += 1
                for i in range(4):
                    if user_q27_30[i] == q27_30_ans[i]: correct_cnt += 1
                for i in range(4):
                    if user_q31_34[i] == q31_34_ans[i]: correct_cnt += 1
                for i in range(9):
                    if user_q35_43[i] == q35_43_ans[i]: correct_cnt += 1
                st.session_state.l17_r_sub = True
                st.session_state.l17_r_score = f"{correct_cnt}/21"
                st.success(f"Chúc mừng bạn đã làm xong bài tập nha. Điểm số của bạn là: {st.session_state.l17_r_score}.")
                send_results_to_gsheet(student_name, "Bài 17", "PHẦN ĐỌC", st.session_state.l17_r_score)

        if st.session_state.l17_r_sub:
            st.markdown("### 🔍 CHI TIẾT CÂU SAI & ĐÁP ÁN ĐÚNG:")
            for i in range(4):
                if user_q23_26[i] != q23_26_ans[i]:
                    st.markdown(f"<span style='color:#D32F2F;'>❌ Câu {i+23} sai:</span> {q23_26_texts[i]}", unsafe_allow_html=True)
                    st.markdown(f"👉 Đáp án đúng: **{q23_26_ans[i]}**")
            for i in range(4):
                if user_q27_30[i] != q27_30_ans[i]:
                    st.markdown(f"<span style='color:#D32F2F;'>❌ Câu {i+27} sai:</span> {q27_30_texts[i]}", unsafe_allow_html=True)
                    st.markdown(f"👉 Đáp án đúng: **{q27_30_ans[i]}**")

    # ------------------ PHẦN VIẾT BÀI 17 ------------------
    with t_write:
        st.markdown("### 三、书写 (Phần viết)")
        st.markdown("#### **第一部分 (Phần 1) - Sắp xếp câu hoàn chỉnh**")
        st.warning("⚠️ Chú ý: Phần viết được chấm tuyệt đối nghiêm ngặt. Sai bất kỳ 1 chữ hoặc 1 dấu câu nào cũng tính là sai hoàn toàn cả câu.")
        
        q44_48_words = [
            "44. 把 / 一下 / 的 / 数字 / 排列 / 剩下",
            "45. 按照 / 同学们 / 顺序 / 排好 / 请 / 队",
            "46. 竞争 / 经济 / 推动 / 发展 / 鼓励 / 能",
            "47. 一万公里 / 这两个 / 距离 / 的 / 城市 / 是",
            "48. 应该 / 老师们 / 自己的 / 课 / 使 / 变得 / 活泼"
        ]
        q44_48_acceptable_ans = [
            ["把剩下的数字排列一下。"],
            ["请同学们按照顺序排好队。"],
            ["鼓励竞争能推动经济发展。"],
            ["这两个城市的距离是一万公里。"],
            ["老师们应该使自己的课变得活泼。"]
        ]
        user_q44_48 = []
        for i, words in enumerate(q44_48_words):
            st.markdown(f"<div class='question-card'><strong>Câu {i+44}:</strong> {words}", unsafe_allow_html=True)
            ans = st.text_input("Nhập câu hoàn chỉnh của bạn tại đây:", key=f"l17_write_p1_{i}").strip()
            user_q44_48.append(ans)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### **第二部分 (Phần 2) - Nhìn tranh đặt câu (Tự luận đối chiếu gợi ý)**")
        st.markdown("<div class='question-card'><strong>Câu 49:</strong> Tranh hai chú chó con dễ thương. Từ gợi ý: <strong>毛</strong></div>", unsafe_allow_html=True)
        user_q49 = st.text_area("Viết câu của bạn:", key="l17_write_p2_49")
        st.markdown("<div class='question-card'><strong>Câu 50:</strong> Tranh biển chỉ đường chỉ Thiên An Môn 2km. Từ gợi ý: <strong>公里</strong></div>", unsafe_allow_html=True)
        user_q50 = st.text_area("Viết câu của bạn:", key="l17_write_p2_50")

        if st.button("🚀 NỘP BÀI PHẦN VIẾT", key="l17_btn_sub_write"):
            if not student_name.strip():
                st.error("⚠️ Bạn hãy điền Họ và tên học sinh ở đầu trang trước khi nộp nhé!")
            else:
                correct_cnt = 0
                for i in range(5):
                    user_ans = user_q44_48[i].strip()
                    matched = False
                    for possible_ans in q44_48_acceptable_ans[i]:
                        if user_ans == possible_ans.strip():
                            matched = True
                            break
                    if matched: correct_cnt += 1
                st.session_state.l17_w_sub = True
                st.session_state.l17_w_score = f"{correct_cnt}/5"
                st.success(f"Chúc mừng bạn đã làm xong bài tập nha. Điểm số của bạn là: {st.session_state.l17_w_score}.")
                send_results_to_gsheet(student_name, "Bài 17", "PHẦN VIẾT", st.session_state.l17_w_score)

        if st.session_state.l17_w_sub:
            st.markdown("### 🔍 CHI TIẾT CÂU SAI & ĐÁP ÁN ĐÚNG:")
            for i in range(5):
                user_ans = user_q44_48[i].strip()
                matched = False
                for possible_ans in q44_48_acceptable_ans[i]:
                    if user_ans == possible_ans.strip():
                        matched = True
                        break
                if not matched:
                    st.markdown(f"<span style='color:#D32F2F;'>❌ Câu {i+44} viết chưa chính xác:</span>", unsafe_allow_html=True)
                    st.markdown(f"Đáp án của bạn: `{user_q44_48[i]}`")
                    st.markdown(f"👉 Đáp án đúng: **{q44_48_acceptable_ans[i][0]}**")



def show_lesson_18(student_name):
    st.markdown("### 📚 BÀI 18: 科技与世界")
    
    if 'l18_l_sub' not in st.session_state: st.session_state.l18_l_sub = False
    if 'l18_r_sub' not in st.session_state: st.session_state.l18_r_sub = False
    if 'l18_w_sub' not in st.session_state: st.session_state.l18_w_sub = False

    t_lis, t_read, t_write = st.tabs(["PHẦN NGHE", "PHẦN ĐỌC", "PHẦN VIẾT"])

    # ------------------ PHẦN NGHE BÀI 18 ------------------
    with t_lis:
        st.markdown("### 一、听力 (Phần nghe)")
        st.markdown("#### **第一部分 (Phần 1) - 判断对错**")
        play_audio("18-1")
        
        q1_5_text = [
            "1. ★ 地址填错地方了。",
            "2. ★ 他们要坐地铁。",
            "3. ★ 明天中午有大雪。",
            "4. ★ 遇到危险时要冷静。",
            "5. ★ 黄河是中国的“母亲河”。"
        ]
        q1_5_ans = ["✔", "✘", "✘", "✔", "✔"]
        user_q1_5 = []
        col1, col2 = st.columns(2)
        for i, q_text in enumerate(q1_5_text):
            target_col = col1 if i < 3 else col2
            with target_col:
                st.markdown(f"<div class='question-card'><strong>{q_text}</strong>", unsafe_allow_html=True)
                ans = st.radio(f"Chọn câu {i+1}:", ["Chưa chọn", "✔ (Đúng)", "✘ (Sai)"], key=f"l18_lis_p1_{i}")
                user_q1_5.append(ans)
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### **第二部分 (Phần 2) - 单项选择**")
        play_audio("18-2")
        
        q6_12_options = [
            ["A. 没有邮件", "B. 电脑坏了", "C. 电话有问题", "D. 密码错了"],
            ["A. 在超市", "B. 没带钱", "C. 在找人", "D. 迷路了"],
            ["A. 寄信", "B. 写地址", "C. 找信封", "D. 发邮件"],
            ["A. 做菜", "B. 咖啡", "C. 面条", "D. 葡萄酒"],
            ["A. 非常困", "B. 发烧了", "C. 没起床", "D. 受欢迎"],
            ["A. 高兴", "B. 无聊", "C. 担心", "D. 轻松"],
            ["A. 借钱", "B. 买饼干", "C. 找钥匙", "D. 问路"]
        ]
        q6_12_ans = ["D", "C", "C", "A", "A", "C", "A"]
        user_q6_12 = []
        col1, col2 = st.columns(2)
        for i in range(7):
            target_col = col1 if i < 4 else col2
            with target_col:
                st.markdown(f"<div class='question-card'><strong>Câu {i+6}:</strong>", unsafe_allow_html=True)
                ans = st.selectbox(f"Đáp án câu {i+6}:", ["Chưa chọn"] + q6_12_options[i], key=f"l18_lis_p2_{i}")
                user_q6_12.append(ans[0] if ans != "Chưa chọn" else "Chưa chọn")
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### **第三部分 (Phần 3) - 单项选择**")
        play_audio("18-3")
        
        q13_22_options = [
            ["A. 大学毕业了", "B. 找到工作了", "C. 考上硕士了", "D. 做教育工作"],
            ["A. 火车站", "B. 机场", "C. 公园", "D. 图书馆"],
            ["A. 网站有问题", "B. 网址错了", "C. 上网速度不快", "D. 女的的电脑坏了"],
            ["A. 是新手", "B. 开车慢", "C. 想停车", "D. 技术好"],
            ["A. 学校", "B. 作者", "C. 办公室", "D. 中学生"],
            ["A. 介绍科学知识", "B. 特别有意思", "C. 赚了很多钱", "D. 解释了很多梦"],
            ["A. 开始时间", "B. 完成的情况", "C. 做事的顺序", "D. 别浪费时间"],
            ["A. 工作总结", "B. 管理效果", "C. 做计划的方法", "D. 时间的重要性"],
            ["A. 为了赚钱", "B. 减少污染", "C. 衣服太脏", "D. 洗衣服太辛苦"],
            ["A. 麻烦的好处", "B. 麻烦的原因", "C. 爬楼的快乐", "D. 交通工具的特点"]
        ]
        q13_22_ans = ["C", "D", "D", "A", "B", "C", "C", "D", "A", "A"]
        user_q13_22 = []
        col1, col2 = st.columns(2)
        for i in range(10):
            target_col = col1 if i < 5 else col2
            with target_col:
                st.markdown(f"<div class='question-card'><strong>Câu {i+13}:</strong>", unsafe_allow_html=True)
                ans = st.selectbox(f"Đáp án câu {i+13}:", ["Chưa chọn"] + q13_22_options[i], key=f"l18_lis_p3_{i}")
                user_q13_22.append(ans[0] if ans != "Chưa chọn" else "Chưa chọn")
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 NỘP BÀI PHẦN NGHE", key="l18_btn_sub_lis"):
            if not student_name.strip():
                st.error("⚠️ Bạn hãy điền Họ và tên học sinh ở đầu trang trước khi nộp nhé!")
            else:
                correct_cnt = 0
                for i in range(5):
                    u_v = "✔" if "✔" in user_q1_5[i] else "✘" if "✘" in user_q1_5[i] else "Chưa chọn"
                    if u_v == q1_5_ans[i]: correct_cnt += 1
                for i in range(7):
                    if user_q6_12[i] == q6_12_ans[i]: correct_cnt += 1
                for i in range(10):
                    if user_q13_22[i] == q13_22_ans[i]: correct_cnt += 1
                st.session_state.l18_l_sub = True
                st.session_state.l18_l_score = f"{correct_cnt}/22"
                st.success(f"Chúc mừng bạn đã làm xong bài tập nha. Điểm số của bạn là: {st.session_state.l18_l_score}.")
                send_results_to_gsheet(student_name, "Bài 18", "PHẦN NGHE", st.session_state.l18_l_score)

        if st.session_state.l18_l_sub:
            st.markdown("### 🔍 CHI TIẾT CÂU SAI & ĐÁP ÁN ĐÚNG:")
            # Phần 1
            for i in range(5):
                u_v = "✔" if "✔" in user_q1_5[i] else "✘" if "✘" in user_q1_5[i] else "Chưa chọn"
                if u_v != q1_5_ans[i]:
                    st.markdown(f"<span style='color:#D32F2F;'>❌ Câu {i+1} sai:</span> {q1_5_text[i]}", unsafe_allow_html=True)
                    st.markdown(f"👉 Đáp án đúng: **{q1_5_ans[i]}**")
                    with st.expander(f"📖 Xem Lời thoại (Script) Câu {i+1}"):
                        scripts = [
                            "先生，您把收件人和寄件人的地址填反了，这儿应该填您自己的地址。我再给您一张单子，您重新填一下吧。\n(Thưa ông, ông đã điền ngược địa chỉ người nhận và người gửi rồi, chỗ này nên điền địa chỉ của ông. Tôi đưa ông một tờ đơn khác, ông điền lại nhé.)",
                            "姐，咱们弄错方向了，去西边的公共汽车应该过马路去那边坐。正好前边有个天桥，我们从那儿过马路吧。\n(Chị ơi, chúng mình đi nhầm hướng rồi, xe buýt đi về phía Tây phải sang bên kia đường bắt. Vừa hay phía trước có cầu vượt, mình qua đường từ đó đi.)",
                            "由于冷空气南下，我省明天将迎来大风降温天气，有些地方还会有小到中雨，交通会受到一定影响，听众朋友们出行时一定要注意安全。\n(Do không khí lạnh tràn về phía Nam, tỉnh ta ngày mai sẽ đón thời tiết gió lớn hạ nhiệt, có nơi có mưa nhỏ đến mưa vừa, giao thông bị ảnh hưởng, thính giả chú ý an toàn khi ra ngoài.)",
                            "遇到危险时，哭不能解决任何问题，你应该想办法向别人求助。但在这之前，你必须先让自己冷静下来。\n(Khi gặp nguy hiểm, khóc không giải quyết được vấn đề gì, bạn nên tìm cách cầu cứu người khác. Nhưng trước đó, bạn phải bình tĩnh lại.)",
                            "黄河是中国第二大河，它有 5464 公里长，人们把它叫作“母亲河”。从地图上看，它就像一个大大的“几”字。\n(Sông Hoàng Hà là con sông lớn thứ hai ở Trung Quốc, dài 5464 km, người ta gọi nó là 'Sông Mẹ'. Nhìn trên bản đồ, nó giống như một chữ '几' lớn.)"
                        ]
                        st.markdown(scripts[i])

            # Phần 2
            for i in range(7):
                if user_q6_12[i] != q6_12_ans[i]:
                    st.markdown(f"<span style='color:#D32F2F;'>❌ Câu {i+6} sai.</span> Lựa chọn của bạn: `{user_q6_12[i]}`", unsafe_allow_html=True)
                    st.markdown(f"👉 Đáp án đúng: **{q6_12_ans[i]}**")
                    with st.expander(f"📖 Xem Lời thoại (Script) Câu {i+6}"):
                        scripts_p2 = [
                            "女：你叔叔刚打电话来说给你发了个电子邮件，让你查收。\n男：我正在上邮箱，可一直进不去，真奇怪，总说我的密码有错，没错啊。\n问：男的为什么感到奇怪？",
                            "男：喂，你在哪儿呢？我已经到公园了，怎么看不到你啊？\n女：我在公园旁边的超市呢，正好我买了一箱矿泉水，你来接我一下吧。\n问：关于男的，下列哪个正确？",
                            "男：你那儿有大一点儿的信封吗？这个太小了。\n女：稍等一下，我发完这封电子邮件就给你找。\n问：男的让女的做什么？",
                            "男：你尝一下，这个菜味道怎么样？\n女：我尝了，稍微有点儿咸，是不是盐放多了？\n问：他们在谈什么？",
                            "男：你困了就先去睡一会儿吧，等比赛开始了，我再叫你起来接着看。\n女：好的，我实在受不了了，先去躺会儿。\n问：女的怎么了？",
                            "女：做得怎么样了？今天能解决这个问题吗？\n男：情况比我们想的复杂得多，还有一个技术问题不知道怎么办，今天恐怕完不了了。\n问：男的现在心情怎么样？",
                            "男：我想买这本词典，可出门忘带钱包了，你能不能先借我一点儿？一会儿回去还你。\n女：没问题。高老师，您要多少？\n问：男的在做什么？"
                        ]
                        st.markdown(scripts_p2[i])

            # Phần 3
            for i in range(10):
                if user_q13_22[i] != q13_22_ans[i]:
                    st.markdown(f"<span style='color:#D32F2F;'>❌ Câu {i+13} sai.</span> Lựa chọn của bạn: `{user_q13_22[i]}`", unsafe_allow_html=True)
                    st.markdown(f"👉 Đáp án đúng: **{q13_22_ans[i]}**")
                    with st.expander(f"📖 Xem Lời thoại (Script) Câu {i+13}"):
                        scripts_p3 = [
                            "女：大学毕业后就没联系了，你现在在哪儿工作呢？\n男：毕业后在老家工作了一年，接着又考上了北京大学，现在在读研究生。\n女：真厉害！是硕士了。你读什么专业？几年？\n男：教育学，三年。\n问：女的为什么说男的很厉害？",
                            "男：明天见面的地点改在东门了？\n女：是，从那边去国家图书馆方便一些。\n男：那我通知班里的同学。时间变了吗？\n女：没变，还是上午八点。\n问：他们明天要去哪儿？",
                            "女：这个网站地址是不是错的？试了好几遍都打不开。\n男：你把网址发过来，我试一下。\n女：怎么样？你那儿能打开吗？\n男：可以，速度挺快的，是不是你电脑有问题？\n问：根据对话，可以知道：",
                            "女：危险！你开得太快了。\n男：好吧，好吧，我开慢点儿。\n女：你现在把车停下，我来开，我真受不了你了！\n男：让我再开会儿。你不是也刚学会几天吗？自己也是个新手。\n女：至少比你开得慢，技术比你好。\n问：通过对话，可以知道男的：",
                            "女：你联系那位作者了吗？\n男：联系了，她竟然是一位在校大学生，没想到她那么年轻。\n女：她同意和我们聊一聊了？\n男：是的，暂定在下星期一，她上午九点来我们办公室谈。\n问：通过对话，可以知道男的联系了：",
                            "男：我昨天晚上做了一个特别有意思的梦，梦到家里有好多好多水，高兴死我了。\n女：这有什么可高兴的？晚上睡觉时，身体感觉到什么，人就容易梦到什么内容。\n男：早上一醒，我就去查了《周公解梦》，书上说梦到水，说明会有很大一笔收入呢！\n女：那你慢慢等着吧，那本书上的内容一点儿也不科学。\n问：关于《周公解梦》，下列哪个最可能正确？",
                            "每个人都应该学会管理时间，而做计划表、严格按照计划做事是有效管理时间的第一步。在做计划表时首先要注意把重要的事安排在前面，除此之外，还要写明完成时间，这样才能做到不浪费一分一秒。\n19．做计划表时，首先要注意什么？\n20．这段话主要谈的是什么？",
                            "每个人都应该学会管理时间，而做计划表、严格按照计划做事是有效管理时间的第一步。在做计划表时首先要注意把重要的事安排在前面，除此之外，还要写明完成时间，这样才能做到不浪费一分一秒。\n19．做计划表时，首先要注意什么？\n20．这段话主要谈的是什么？",
                            "因为有些人觉得用手写字麻烦，于是有了打字机；因为有些人觉得每天爬楼麻烦，于是有了电梯；因为有些人觉得洗衣服麻烦，于是有了洗衣机；同样因为有些人觉得走路又累又麻烦，才有了各种交通工具。所以，觉得麻烦不一定是件坏事。\n21．根据这段话，为什么会出现洗衣机？\n22．这段话主要想告诉我们什么？",
                            "因为有些人觉得用手写字麻烦，于是有了打字机；因为有些人觉得每天爬楼麻烦，于是有了电梯；因为有些人觉得洗衣服麻烦，于是有了洗衣机；同样因为有些人觉得走路又累又麻烦，才有了各种交通工具。所以，觉得麻烦不一定是件坏事。\n21．根据这段话，为什么会出现洗衣机？\n22．这段话主要想告诉我们什么？"
                        ]
                        st.markdown(scripts_p3[i])

    # ------------------ PHẦN ĐỌC BÀI 18 ------------------
    with t_read:
        st.markdown("### 二、阅读 (Phần đọc)")
        st.markdown("#### **第一部分 (Phần 1) - 选词填空**")
        st.markdown("**第 23-26 题：**")
        st.code("A 举    B 是否    C 火    D 坚持    E 警察")
        
        q23_26_texts = [
            "23. 校门口右边那家饭馆的菜做得确实好吃，\n\n吃饭时间经常有人排队等座，生意越来越（      ）了。",
            "24. 小时候我的理想是当一名（      ），\n\n但现在我却成了一个动物园管理员，跟熊猫和老虎成了好朋友。",
            "25. 随着年龄的增长，我们会遇到许多机会，\n\n但问题是当它来到你身边时，你（      ）已经做好了准备。",
            "26. 每个人都有自己特别感兴趣的东西，\n\n（      ）个例子，作家爱讲故事，演员爱表演。\n\n我们只有了解了自己的兴趣爱好后，才能更好地发展自己。"
        ]
        q23_26_ans = ["C", "E", "B", "A"]
        user_q23_26 = []
        col1, col2 = st.columns(2)
        for i, q_text in enumerate(q23_26_texts):
            target_col = col1 if i < 2 else col2
            with target_col:
                st.markdown(f"<div class='question-card'><strong>{q_text}</strong>", unsafe_allow_html=True)
                ans = st.selectbox(f"Từ điền câu {i+23}:", ["Chưa chọn", "A. 举", "B. 是否", "C. 火", "D. 坚持", "E. 警察"], key=f"l18_read_p1_1_{i}")
                user_q23_26.append(ans[0] if ans != "Chưa chọn" else "Chưa chọn")
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("**第 27-30 题：**")
        st.code("A 咸    B 桥    C 温度    D 收    E 座")
        q27_30_texts = [
            "27. A：我刚从会议室过来，怎么一个人也没有？\n\nB：对不起，今天的会议改到明天上午了，您没（      ）到通知吗？",
            "28. A：中午去海边游泳了？感觉怎么样？\n\nB：还行，就是海水太（      ）了。",
            "29. A：这儿的景色真美！帮我照张相吧。\n\nB：好的，你稍微往左边站一点儿，我帮你把后面的大（      ）也照上。",
            "30. A：北京有一（      ）香山，非常有名。每到秋天，满山都是红叶，景色特别漂亮。\n\nB：是吗？那我有机会一定要去看看。"
        ]
        q27_30_ans = ["D", "A", "B", "E"]
        user_q27_30 = []
        for i, q_text in enumerate(q27_30_texts):
            target_col = col1 if i < 2 else col2
            with target_col:
                st.markdown(f"<div class='question-card'><strong>{q_text}</strong>", unsafe_allow_html=True)
                ans = st.selectbox(f"Từ điền câu {i+27}:", ["Chưa chọn", "A. 咸", "B. 桥", "C. 温度", "D. 收", "E. 座"], key=f"l18_read_p1_2_{i}")
                user_q27_30.append(ans[0] if ans != "Chưa chọn" else "Chưa chọn")
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### **第二部分 (Phần 2) - 排列顺序**")
        q31_34_texts = [
            "31.\n\nA. 因为无论对自己还是对其他人\n\nB. 司机喝酒后不允许开车\n\nC. 酒后开车都是非常危险的",
            "32.\n\nA. 即使已经过去了几个世纪\n\nB. 仍然受到读者们的喜爱\n\nC. 这个美丽的爱情故事，感动过无数人",
            "33.\n\nA. 祝 homework/祝 revolutions/祝 national/祝他们在今后的生活中\n\nB. 让我们一起举杯\n\nC. 一切顺利，永远幸福",
            "34.\n\nA. 只要找出文章中的关键信息\n\nB. 就可以在短时间内了解文章的大意\n\nC. 做到快速阅读其实不难，简单来说"
        ]
        # Let's fix text of 33 in q31_34_texts:
        q31_34_texts[2] = "33.\n\nA. 祝他们在今后的生活中\n\nB. 让我们一起举杯\n\nC. 一切顺利，永远幸福"
        
        q31_34_ans = ["BAC", "CAB", "BAC", "CAB"]
        user_q31_34 = []
        for i, q_text in enumerate(q31_34_texts):
            st.markdown(f"<div class='question-card'>{q_text}", unsafe_allow_html=True)
            ans = st.text_input(f"Thứ tự câu {i+31} (Ví dụ: ABC):", key=f"l18_read_p2_{i}").strip().upper()
            user_q31_34.append(ans)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### **第三部分 (Phần 3) - 阅读理解**")
        q35_43_questions = [
            "35. 一般情况下，飞机起飞的方向是和风向相反的，\n这样飞机可以得到更多向上的助力；\n另外，相反方向的风能使飞机的离地速度减慢，这样能够保证安全。\n\n★ 飞机起飞的方向应该：",
            "36. 森林里有一种奇特的植物，它开的花比普通的花大很多。\n这种植物会吸引来一些小动物，当小动物走近花时，植物就会把它们吃掉。\n\n★ 这种植物：",
            "37. 二三十年前很多人还有通过写信交友的习惯，\n但是进入 21 世纪以后，随着科学技术的发展，\n现在几乎没有人会选择写信了，人们更愿意上网交流。\n\n★ 现在人们更愿意：",
            "38. 小姐，我们这种矿泉水取自雪山，不仅好喝，\n用它来洗脸对皮肤也有好处，所以价格要比其他矿泉水贵一些。\n\n★ 这种矿泉水的特点是：",
            "39. 随着科学技术的发展，距离对人与人之间交流的影响越来越小了，\n只要打个电话或者发个电子邮件，就能联系到千里之外的人。\n\n★ 科技发展带来的好处是：",
            "[40-41] 昨天下午女朋友突然想让我陪她去逛街买衣服，\n于是她就开始准备起来了。\n她先洗了个澡，接着又在脸上画了半天，过了一个小时了她还没弄好。\n我提醒她商场六点关门，她说马上就好，我只能继续等着。\n结果，等我们到商场时，商场已经关门了。\n她很生气，说我没注意时间，真让我受不了。\n\n40. ★ 出门前女朋友在做什么？",
            "41. ★ 女朋友为什么生气？",
            "[42-43] 不知道从什么时候开始，我们的生活已经离不开密码：\n用银行卡取钱需要密码，打开手机需要密码，\n在互联网上收发邮件、聊天需要密码，有时候甚至连开门都需要密码。\n密码让我们的生活变得更方便安全，可除此以外，它也给我们增加了不少烦恼。\n试着想一想，如果谁不小心忘记了那些密码，他的生活会变成什么样。\n\n42. ★ 人们需要记住什么？",
            "43. ★ 这段话主要讲的是："
        ]
        q35_43_options = [
            ["A. 向南", "B. 向北", "C. 与风向相反", "D. 与风向相同"],
            ["A. 会吃小动物", "B. 花很漂亮", "C. 夏天才开花", "D. 没有叶子"],
            ["A. 发短信", "B. 写日记", "C. 上网聊", "D. 看杂志"],
            ["A. 干净", "B. 有点儿咸", "C. 来自海洋", "D. 洗脸对皮肤好"],
            ["A. 减少误会", "B. 减少污染", "C. 交流更方便", "D. 增加安全感"],
            ["A. 画画儿", "B. 打扫房间", "C. 打扮自己", "D. 等朋友来"],
            ["A. 朋友来晚了", "B. 忘带钥匙了", "C. 衣服不打折", "D. 商场关门了"],
            ["A. 银行卡", "B. 地址", "C. 密码", "D. 手机号码"],
            ["A. 科学技术的发展", "B. 互联网的优缺点", "C. 密码对人的影响", "D. 哪些地方用密码"]
        ]
        q35_43_ans = ["C", "A", "C", "D", "C", "C", "D", "C", "C"]
        user_q35_43 = []
        for i in range(9):
            st.markdown(f"<div class='question-card'>{q35_43_questions[i]}", unsafe_allow_html=True)
            ans = st.selectbox(f"Đáp án câu {i+35}:", ["Chưa chọn"] + q35_43_options[i], key=f"l18_read_p3_{i}")
            user_q35_43.append(ans[0] if ans != "Chưa chọn" else "Chưa chọn")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 NỘP BÀI PHẦN ĐỌC", key="l18_btn_sub_read"):
            if not student_name.strip():
                st.error("⚠️ Bạn hãy điền Họ và tên học sinh ở đầu trang trước khi nộp nhé!")
            else:
                correct_cnt = 0
                for i in range(4):
                    if user_q23_26[i] == q23_26_ans[i]: correct_cnt += 1
                for i in range(4):
                    if user_q27_30[i] == q27_30_ans[i]: correct_cnt += 1
                for i in range(4):
                    if user_q31_34[i] == q31_34_ans[i]: correct_cnt += 1
                for i in range(9):
                    if user_q35_43[i] == q35_43_ans[i]: correct_cnt += 1
                st.session_state.l18_r_sub = True
                st.session_state.l18_r_score = f"{correct_cnt}/21"
                st.success(f"Chúc mừng bạn đã làm xong bài tập nha. Điểm số của bạn là: {st.session_state.l18_r_score}.")
                send_results_to_gsheet(student_name, "Bài 18", "PHẦN ĐỌC", st.session_state.l18_r_score)

        if st.session_state.l18_r_sub:
            st.markdown("### 🔍 CHI TIẾT CÂU SAI & ĐÁP ÁN ĐÚNG:")
            for i in range(4):
                if user_q23_26[i] != q23_26_ans[i]:
                    st.markdown(f"<span style='color:#D32F2F;'>❌ Câu {i+23} sai:</span> {q23_26_texts[i]}", unsafe_allow_html=True)
                    st.markdown(f"👉 Đáp án đúng: **{q23_26_ans[i]}**")
            for i in range(4):
                if user_q27_30[i] != q27_30_ans[i]:
                    st.markdown(f"<span style='color:#D32F2F;'>❌ Câu {i+27} sai:</span> {q27_30_texts[i]}", unsafe_allow_html=True)
                    st.markdown(f"👉 Đáp án đúng: **{q27_30_ans[i]}**")
            for i in range(4):
                if user_q31_34[i] != q31_34_ans[i]:
                    st.markdown(f"<span style='color:#D32F2F;'>❌ Câu {i+31} sai:</span>", unsafe_allow_html=True)
                    st.markdown(f"👉 Lựa chọn của bạn: `{user_q31_34[i]}` | Đáp án đúng: **{q31_34_ans[i]}**")
            for i in range(9):
                if user_q35_43[i] != q35_43_ans[i]:
                    st.markdown(f"<span style='color:#D32F2F;'>❌ Câu {i+35} sai:</span> {q35_43_questions[i]}", unsafe_allow_html=True)
                    st.markdown(f"👉 Lựa chọn của bạn: `{user_q35_43[i]}` | Đáp án đúng: **{q35_43_ans[i]}**")

    # ------------------ PHẦN VIẾT BÀI 18 ------------------
    with t_write:
        st.markdown("### 三、书写 (Phần viết)")
        st.markdown("#### **第一部分 (Phần 1) - Sắp xếp câu hoàn chỉnh**")
        st.warning("⚠️ Chú ý: Phần viết được chấm tuyệt đối nghiêm ngặt. Sai bất kỳ 1 chữ hoặc 1 dấu câu nào cũng tính là sai hoàn toàn cả câu.")
        
        q44_48_words = [
            "44. 飞机 / 最 / 被认为 / 是 / 安全的 / 交通方式",
            "45. 一个 / 责任感 / 警察 / 有 / 优秀的 / 需要",
            "46. 我顺便 / 回来的路上 / 邮局 / 去 / 趟 / 了",
            "47. 历史教授 / 著名的 / 是位 / 作者 / 这本书 / 的",
            "48. 密码 / 你爸 / 把 / 信用卡的 / 了 / 改"
        ]
        
        q44_48_acceptable_ans = [
            ["飞机被认为是最安全的交通方式。"],
            ["一个优秀的警察需要有责任感。", "优秀的警察需要有一个责任感。"],
            ["回来的路上我顺便去了趟邮局。", "我回来的路上顺便去了趟邮局。"],
            ["这本书的作者是位著名的历史教授。", "著名的历史教授是这本书的作者。"],
            ["你爸把信用卡的密码改了。"]
        ]
        
        user_q44_48 = []
        for i, words in enumerate(q44_48_words):
            st.markdown(f"<div class='question-card'><strong>Câu {i+44}:</strong> {words}", unsafe_allow_html=True)
            ans = st.text_input("Nhập câu hoàn chỉnh của bạn tại đây:", key=f"l18_write_p1_{i}").strip()
            user_q44_48.append(ans)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### **第二部分 (Phần 2) - Nhìn tranh đặt câu (Tự luận đối chiếu gợi ý)**")
        
        st.markdown("""
        <div class='question-card'>
            <strong>Câu 49:</strong> Tranh một chiếc飞机在跑道降落。<br>
            Từ gợi ý: <strong>降落</strong>
        </div>
        """, unsafe_allow_html=True)
        user_q49 = st.text_area("Viết câu tự luận của bạn tại đây:", key="l18_write_p2_49")
        
        st.markdown("""
        <div class='question-card'>
            <strong>Câu 50:</strong> Tranh một người đi trong rừng bị lạc.<br>
            Từ gợi ý: <strong>迷路</strong>
        </div>
        """, unsafe_allow_html=True)
        user_q50 = st.text_area("Viết câu tự luận của bạn tại đây:", key="l18_write_p2_50")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 NỘP BÀI PHẦN VIẾT", key="l18_btn_sub_write"):
            if not student_name.strip():
                st.error("⚠️ Bạn hãy điền Họ và tên học sinh ở đầu trang trước khi nộp nhé!")
            else:
                correct_cnt = 0
                for i in range(5):
                    user_ans = user_q44_48[i].strip()
                    matched = False
                    for possible_ans in q44_48_acceptable_ans[i]:
                        if user_ans == possible_ans.strip():
                            matched = True
                            break
                    if matched:
                        correct_cnt += 1
                        
                st.session_state.l18_w_sub = True
                st.session_state.l18_w_score = f"{correct_cnt}/5"
                st.success(f"Chúc mừng bạn đã làm xong bài tập nha. Điểm số của bạn là: {st.session_state.l18_w_score}.")
                send_results_to_gsheet(student_name, "Bài 18", "PHẦN VIẾT", st.session_state.l18_w_score)

        if st.session_state.l18_w_sub:
            st.markdown("### 🔍 CHI TIẾT CÂU SAI & ĐÁP ÁN ĐÚNG:")
            for i in range(5):
                user_ans = user_q44_48[i].strip()
                matched = False
                for possible_ans in q44_48_acceptable_ans[i]:
                    if user_ans == possible_ans.strip():
                        matched = True
                        break
                if not matched:
                    st.markdown(f"<span style='color:#D32F2F;'>❌ Câu {i+44} viết chưa chính xác:</span>", unsafe_allow_html=True)
                    st.markdown(f"Đáp án của bạn: `{user_q44_48[i]}`")
                    st.markdown(f"👉 Đáp án đúng: **{q44_48_acceptable_ans[i][0]}**")
                    
            st.markdown("---")
            st.markdown("#### 💡 CÂU GỢI Ý MẪU CHO PHẦN ĐẶT CÂU THEO TRANH:")
            st.markdown("- **Câu 49 (降落):** `飞机马上就要降落了，一会儿告诉他我们在机场门口等他。` *(Máy bay sắp hạ cánh rồi, lát nữa bảo anh ấy chúng ta đợi ở cửa sân bay nhé.)*")
            st.markdown("- **Câu 50 (迷路):** `那座山小路特别多，第一次来的人很容易迷路。` *(Ngọn núi đó rất nhiều đường nhỏ, người mới tới lần đầu rất dễ bị lạc.)*")


# ==============================================================================
# HỆ THỐNG MENU VÀ TỰ ĐỘNG SẮP XẾP BÀI MỚI LÊN TRƯỚC (SCALABLE ARCHITECTURE)
# ==============================================================================

# Khi bạn thêm bài học mới (ví dụ Bài 18, 19, 20...), bạn chỉ cần định nghĩa hàm tương tự như trên
# rồi khai báo thêm vào dictionary LESSONS dưới đây.
# Bộ máy Streamlit sẽ tự động hiển thị bài học mới nhất lên đầu tiên trong ô chọn bài tập!


def show_lesson_19(student_name):
    if 'l19_l_sub' not in st.session_state: st.session_state.l19_l_sub = False
    if 'l19_r_sub' not in st.session_state: st.session_state.l19_r_sub = False
    if 'l19_w_sub' not in st.session_state: st.session_state.l19_w_sub = False

    t_lis, t_read, t_write = st.tabs(["PHẦN NGHE", "PHẦN ĐỌC", "PHẦN VIẾT"])

    # ------------------ PHẦN NGHE BÀI 19 ------------------
    with t_lis:
        st.markdown("### 一、听力 (Phần nghe)")
        
        # --- PART 1 ---
        st.markdown("#### **第一部分 (Phần 1) - 判断对错**")
        play_audio("19-1")
        
        q1_5_text = [
            "1. ★ 想重新让人相信很难。",
            "2. ★ 他在理发店。",
            "3. ★ 他想租个大房子。",
            "4. ★ 人们可以通过音乐交流感情。",
            "5. ★ 他刚来这儿不久。"
        ]
        q1_5_ans = ["✔", "✔", "✘", "✔", "✘"]
        user_q1_5 = []
        col1, col2 = st.columns(2)
        for i, q_text in enumerate(q1_5_text):
            target_col = col1 if i < 3 else col2
            with target_col:
                st.markdown(f"<div class='question-card'><strong>{q_text}</strong>", unsafe_allow_html=True)
                ans = st.radio(f"Chọn câu {i+1}:", ["Chưa chọn", "✔ (Đúng)", "✘ (Sai)"], key=f"l19_lis_p1_{i}")
                user_q1_5.append(ans)
                st.markdown("</div>", unsafe_allow_html=True)

        # --- PART 2 ---
        st.markdown("---")
        st.markdown("#### **第二部分 (Phần 2) - 单项选择**")
        play_audio("19-2")
        
        q6_12_options = [
            ["A. 不愿意", "B. 同意教男的", "C. 没时间", "D. 打得不好"],
            ["A. 迟到了", "B. 去打印材料", "C. 没听到", "D. 没带材料"],
            ["A. 爱吃饺子", "B. 鼻子受了伤", "C. 肚子饿了", "D. 刚打完网球"],
            ["A. 衣服很贵", "B. 男的觉得热", "C. 窗户坏了", "D. 女的穿得多"],
            ["A. 手表", "B. 包", "C. 出租车", "D. 钱包"],
            ["A. 重新做", "B. 增加一列", "C. 打印表格", "D. 减少一列"],
            ["A. 太亮了", "B. 坏了", "C. 太小了", "D. 很好看"]
        ]
        q6_12_ans = ["B", "B", "C", "B", "A", "B", "C"]
        user_q6_12 = []
        col1, col2 = st.columns(2)
        for i in range(7):
            target_col = col1 if i < 4 else col2
            with target_col:
                st.markdown(f"<div class='question-card'><strong>Câu {i+6}:</strong>", unsafe_allow_html=True)
                ans = st.selectbox(f"Đáp án câu {i+6}:", ["Chưa chọn"] + q6_12_options[i], key=f"l19_lis_p2_{i}")
                user_q6_12.append(ans[0] if ans != "Chưa chọn" else "Chưa chọn")
                st.markdown("</div>", unsafe_allow_html=True)

        # --- PART 3 ---
        st.markdown("---")
        st.markdown("#### **第三部分 (Phần 3) - 单项选择**")
        play_audio("19-3")
        
        q13_22_options = [
            ["A. 大使馆", "B. 银行", "C. 学校", "D. 医院"],
            ["A. 体育馆", "B. 电影院", "C. 宾馆", "D. 图书馆"],
            ["A. 带家具的", "B. 购物方便的", "C. 房租便宜的", "D. 离学校近的"],
            ["A. 图书馆", "B. 学校东门", "C. 商店", "D. 一楼"],
            ["A. 桌子", "B. 沙发", "C. 冰箱", "D. 饮料"],
            ["A. 年龄小", "B. 有基础", "C. 胳膊长", "D. 长得高"],
            ["A. 喜欢功夫", "B. 个子不高", "C. 十六岁了", "D. 考试第一"],
            ["A. 五十五岁", "B. 十五岁", "C. 五十六岁", "D. 十六岁"],
            ["A. 同事", "B. 同学", "C. 学生", "D. 老师"],
            ["A. 没上班", "B. 看错了", "C. 速度慢", "D. 声音小"]
        ]
        q13_22_ans = ["D", "B", "C", "C", "B", "B", "B", "B", "A", "B"]
        user_q13_22 = []
        col1, col2 = st.columns(2)
        for i in range(10):
            target_col = col1 if i < 5 else col2
            with target_col:
                st.markdown(f"<div class='question-card'><strong>Câu {i+13}:</strong>", unsafe_allow_html=True)
                ans = st.selectbox(f"Đáp án câu {i+13}:", ["Chưa chọn"] + q13_22_options[i], key=f"l19_lis_p3_{i}")
                user_q13_22.append(ans[0] if ans != "Chưa chọn" else "Chưa chọn")
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 NỘP BÀI PHẦN NGHE", key="l19_btn_sub_lis"):
            if not student_name.strip():
                st.error("⚠️ Bạn hãy điền Họ và tên học sinh ở đầu trang trước khi nộp nhé!")
            else:
                correct_cnt = 0
                for i in range(5):
                    u_v = "✔" if "✔" in user_q1_5[i] else "✘" if "✘" in user_q1_5[i] else "Chưa chọn"
                    if u_v == q1_5_ans[i]: correct_cnt += 1
                for i in range(7):
                    if user_q6_12[i] == q6_12_ans[i]: correct_cnt += 1
                for i in range(10):
                    if user_q13_22[i] == q13_22_ans[i]: correct_cnt += 1
                st.session_state.l19_l_sub = True
                st.session_state.l19_l_score = f"{correct_cnt}/22"
                st.success(f"Chúc mừng bạn đã làm xong bài tập nha. Điểm số của bạn là: {st.session_state.l19_l_score}.")
                send_results_to_gsheet(student_name, "Bài 19", "PHẦN NGHE", st.session_state.l19_l_score)

        if st.session_state.l19_l_sub:
            st.markdown("### 🔍 CHI TIẾT CÂU SAI & ĐÁP ÁN ĐÚNG:")
            scripts_p1 = [
                "别以为做错了事道个歉，说句对不起就行了。\n因为得到别人的原谅很容易，但要重新让别人再相信你却很难。\n(Đừng tưởng làm sai điều gì chỉ cần xin lỗi một tiếng là xong. Vì nhận được sự tha thứ của người khác thì dễ, nhưng để họ lại tin tưởng bạn thì rất khó.)",
                "你好，我想理个发，稍微短一点儿就可以。\n一会儿我还有些事要办，所以麻烦你快一点儿。\n(Xin chào, tôi muốn cắt tóc, ngắn một chút là được. Lát nữa tôi còn có chút việc phải làm, nên phiền bạn nhanh một chút.)",
                "我想租一个交通方便的房子，离地铁站近点儿，\n但是周围环境不能太吵，房租最好也别太贵。当然，如果房东比较友好，那就更好了。\n(Tôi muốn thuê một căn nhà giao thông thuận tiện, gần ga tàu điện ngầm một chút, nhưng môi trường xung quanh không được quá ồn, tiền thuê nhà tốt nhất cũng đừng quá đắt. Tất nhiên nếu chủ nhà thân thiện thì càng tốt.)",
                "音乐不仅是一门艺术，也是一种语言。\n人们对音乐的喜爱与国籍无关。\n通过音乐，不同国家的人可以交流感情，增进了解。\n(Âm nhạc không chỉ là nghệ thuật mà còn là một ngôn ngữ. Sự yêu thích âm nhạc của con người không liên quan đến quốc tịch. Thông qua âm nhạc, con người ở các quốc gia khác nhau có thể giao lưu cảm xúc, tăng cường hiểu biết.)",
                "他虽然不是在这儿出生的，但却是在这儿长大的。\n他三岁跟父亲母亲一起来到这儿，就再也没离开过。\n因此，他对这个地方感情很深。\n(Anh ấy tuy không sinh ra ở đây nhưng lại lớn lên ở đây. Anh ấy theo bố mẹ đến đây từ năm ba tuổi và chưa từng rời đi. Do đó, tình cảm của anh ấy dành cho nơi này rất sâu sắc.)"
            ]
            for i in range(5):
                u_v = "✔" if "✔" in user_q1_5[i] else "✘" if "✘" in user_q1_5[i] else "Chưa chọn"
                if u_v != q1_5_ans[i]:
                    st.markdown(f"<span style='color:#D32F2F;'>❌ Câu {i+1} sai:</span> {q1_5_text[i]}", unsafe_allow_html=True)
                    st.markdown(f"👉 Đáp án đúng: **{q1_5_ans[i]}**")
                    with st.expander(f"📖 Xem Lời thoại (Script) Câu {i+1}"):
                        st.markdown(scripts_p1[i])
                        
            scripts_p2 = [
                "男：你乒乓球打得真不错，有时间能教教我吗？\n女：没问题。我每周六都会来体育馆，到时候你来找我就行了。\n问：女的是什么意思？",
                "男：你这么着急去哪儿啊？我刚才叫你两次你都没听到。\n女：我去打印几份材料，一会儿上课讨论的时候要用。\n问：女的为什么很着急？",
                "女：打了一下午羽毛球，肚子有点儿饿了。真香，今天吃什么？\n男：你鼻子真好，今晚我们吃饺子。再等一会儿，饭马上就好。\n问：关于女的，可以知道什么？",
                "男：开一下窗户吧，热得我都有点儿受不了了。\n女：是你穿得太多了，把外面那件衣服脱了吧。\n问：根据对话，可以知道什么？",
                "女：你看见我的手表没有？我印象里上车的时候还戴着呢。\n男：那看看在不在你包里。不会丢在出租车上了吧？\n问：女的在找什么？",
                "男：孙小姐，表格我做好了，您看看有什么问题没有？\n女：刚才忘和你说了，还要再加上一列“性别”。\n问：女的要求怎么做？",
                "男：厨房里的这个灯太小了，抽时间换一个大点儿、亮点儿的吧。\n女：以前不觉得，你现在一说，我也觉得确实挺小的。我今天下班去超市买一个。\n问：他们觉得厨房的灯怎么样？"
            ]
            for i in range(7):
                if user_q6_12[i] != q6_12_ans[i]:
                    st.markdown(f"<span style='color:#D32F2F;'>❌ Câu {i+6} sai.</span> Lựa chọn của bạn: `{user_q6_12[i]}`", unsafe_allow_html=True)
                    st.markdown(f"👉 Đáp án đúng: **{q6_12_ans[i]}**")
                    with st.expander(f"📖 Xem Lời thoại (Script) Câu {i+6}"):
                        st.markdown(scripts_p2[i])

            scripts_p3 = [
                "女：请把姓名、年龄、性别、联系方式等信息填在这张表上。\n男：好的，是在一楼打针吗？\n女：对，一楼，第二个房间就是打针室。到时候表交给护士就行了。\n男：好的，谢谢你。\n问：男的最可能在哪儿？",
                "男：您好，我要两张电影票，八点二十那场。\n女：好的，您选一下座位吧，电脑上这些蓝色的都可以选。\n男：我要中间的，第十排，九号和十号。\n女：好的，先生，一共一百二十元。\n问：他们最可能在哪儿？",
                "男：你想租什么样的房子？\n女：最好是离公司近一点儿，周围要安静，当然也不能太贵了。\n男：咱公司附近是购物中心，估计没有太便宜的房子。\n女：如果交通方便，稍微远一点儿，我也可以考虑。\n问：女的想找什么样的房子？",
                "男：请问，附近哪儿可以复印？\n女：图书馆一楼东边有几台自助复印机。\n男：图书馆那儿人太多，总是排队，还有其他地方吗？\n女：那你要去学校外面了，南门对面有个小商店，那儿也可以复印。\n问：根据对话，男的最可能去哪儿？",
                "男：小心，您慢点儿，我跟您一起搬吧。\n女：没关系，这个小沙发我自己搬得动。\n男：您这是要把它搬出来放哪儿啊？\n女：就这儿，再往左边一点儿就好了。\n问：女的在搬什么？",
                "男：你学得可真快！\n女：我小时候学过两年的舞蹈，有点儿基础。\n男：原来是这样啊，那你帮我看看，我的动作对不对？\n女：总的来说，你跳得也不错，不过，胳膊再抬高点儿就更标准了。\n问：女的为什么学得快？",
                "邓亚萍是中国著名的乒乓球运动员，也是获得世界乒乓球比赛第一次数最多的女运动员。她身高只有一米五五，看上去好像不是打乒乓球的材料，但她通过自己的努力，十三岁就获得全国第一，十五岁获得亚洲第一，第二年又成为世界第一，改变了人们认为高个子才适合打乒乓球的看法。\n19．关于邓亚萍，可以知道什么？\n20．邓亚萍什么时候获得亚洲第一？",
                "邓亚萍十六岁成为世界第一，十五岁获得亚洲第一。",
                "今天早上在上班路上，我看见同事小月走在前面不远处，就想跟她打个招呼。于是，我一边快走一边叫她的名字，可她一直没回头。我只好加快速度向她跑了过去，等到了她身边，才发现原来我认错人了。\n21．说话人一开始想和谁打招呼？\n22．说话人怎么了？",
                "认错人了。"
            ]
            for i in range(10):
                if user_q13_22[i] != q13_22_ans[i]:
                    st.markdown(f"<span style='color:#D32F2F;'>❌ Câu {i+13} sai.</span> Lựa chọn của bạn: `{user_q13_22[i]}`", unsafe_allow_html=True)
                    st.markdown(f"👉 Đáp án đúng: **{q13_22_ans[i]}**")
                    with st.expander(f"📖 Xem Lời thoại (Script) Câu {i+13}"):
                        st.markdown(scripts_p3[i])

    # ------------------ PHẦN ĐỌC BÀI 19 ------------------
    with t_read:
        st.markdown("### 二、阅读 (Phần đọc)")
        st.markdown("#### **第一部分 (Phần 1) - 选词填空**")
        st.markdown("**第 23-26 题：**")
        st.code("A 戴    B 抬    C 禁止    D 坚持    E 道歉")
        
        q23_26_texts = [
            "23. 夏天的晚上，我喜欢躺在草地上，\n\n（      ） 头看着满天的星星，那种感觉真是太棒了。",
            "24. 这件事情看起来确实是我误会他了。\n\n我明天就去向他（      ），希望他能原谅我。",
            "25. 走路的时候（      ） 着耳机听音乐，\n\n会影响你的注意力还有判断力，有时候是十分危险的。",
            "26. 先生，对不起，我们宾馆有规定，\n\n这里（      ） 抽烟。前面有专门的吸烟室，往前走就能看到，就在楼梯右边。"
        ]
        q23_26_opts = ["A. 戴", "B. 抬", "C. 禁止", "D. 坚持", "E. 道歉"]
        q23_26_ans = ["B", "E", "A", "C"]
        user_q23_26 = []
        col1, col2 = st.columns(2)
        for i, q_text in enumerate(q23_26_texts):
            target_col = col1 if i < 2 else col2
            with target_col:
                st.markdown(f"<div class='question-card'><strong>{q_text}</strong>", unsafe_allow_html=True)
                ans = st.selectbox(f"Từ điền câu {i+23}:", ["Chưa chọn"] + q23_26_opts, key=f"l19_read_p1_1_{i}")
                user_q23_26.append(ans[0] if ans != "Chưa chọn" else "Chưa chọn")
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("**第 27-30 题：**")
        st.code("A 占线    B 场    C 温度    D 转    E 眼镜")
        q27_30_texts = [
            "27. A：这个礼拜天我看了一（      ） 精彩的足球赛。\n\nB：是北京队跟上海队踢的那场吧？我也看了，踢得真不错！",
            "28. A：您好！请问这附近是不是有家东北饺子馆？\n\nB：对，你走到前面路口左（      ） 就能看见了。",
            "29. A：对面戴（      ） 的那个人你认识吗？\n\nB：她呀，她是新来的护士，好像是姓元。",
            "30. A：王大夫办公室的电话怎么一直（      ） 呢？\n\nB：是不是电话没放好？你还是直接过去找他一趟吧。"
        ]
        q27_30_opts = ["A. 占线", "B. 场", "C. 温度", "D. 转", "E. 眼镜"]
        q27_30_ans = ["B", "D", "E", "A"]
        user_q27_30 = []
        for i, q_text in enumerate(q27_30_texts):
            target_col = col1 if i < 2 else col2
            with target_col:
                st.markdown(f"<div class='question-card'><strong>{q_text}</strong>", unsafe_allow_html=True)
                ans = st.selectbox(f"Từ điền câu {i+27}:", ["Chưa chọn"] + q27_30_opts, key=f"l19_read_p1_2_{i}")
                user_q27_30.append(ans[0] if ans != "Chưa chọn" else "Chưa chọn")
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### **第二部分 (Phần 2) - 排列顺序**")
        q31_34_texts = [
            "31.\n\nA. 但在校长的鼓励下，她还是坚持了下来\n\nB. 学舞蹈是一件很辛苦的事\n\nC. 每天都要对着镜子练习同样的动作",
            "32.\n\nA. 开车千万别喝酒，喝酒千万别开车\n\nB. 每个人都应该记住这句话\n\nC. 法律禁止司机酒后开车",
            "33.\n\nA. 今天的晚会太精彩了\n\nB. 动作既标准又好看，非常棒\n\nC. 特别是那些外国留学生表演的中国功夫",
            "34.\n\nA. 道歉时应该让人感觉到你真心的歉意\n\nB. 道歉不仅仅是一句简单的“对不起”\n\nC. 那样才有可能获得别人的原谅"
        ]
        q31_34_ans = ["BCA", "CAB", "ACB", "BAC"]
        user_q31_34 = []
        for i, q_text in enumerate(q31_34_texts):
            st.markdown(f"<div class='question-card'>{q_text}", unsafe_allow_html=True)
            ans = st.text_input(f"Thứ tự câu {i+31} (Ví dụ: ABC):", key=f"l19_read_p2_{i}").strip().upper()
            user_q31_34.append(ans)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### **第三部分 (Phần 3) - 阅读理解**")
        q35_43_questions = [
            "35. 很多人喜欢吃辣的食物，特别是在冷天，吃点儿辣的会让人觉得暖和。\n但是如果吃得太多，对胃不好。\n\n★ 这段话主要想告诉我们：",
            "36. 我刚来这个城市的时候，这里很小，也很旧。\n十几年过去了，这里建起了很多高楼，路也变宽了，\n变得越来越漂亮、越来越热闹了。\n\n★ 关于这个城市，可以知道：",
            "37. 人们常用“酸甜苦辣”来形容生活的各种味道。\n其实，生活中的困难和失败就像“苦”和“辣”，\n虽然让人难受，但它能让人成长。\n\n★ “苦”和“辣”可以让人：",
            "38. 阳光、空气和水是生命不可缺少的。\n如果缺少了阳光，植物就无法生长；\n如果缺少了水，生命就无法继续。\n\n★ 这段话主要谈：",
            "39. 我上学校网站看了课表，发现李老师这学期开了一门“汉字与文化”课，\n我想去听听，之前看过他写的一篇关于这方面的文章，非常有趣。\n\n★ 他在谈：",
            "[40-41] 生活中我们总是需要做出各种各样的选择，\n比如选择哪个人做自己的妻子或丈夫，\n毕业后怎么选择适合自己发展的职业，\n购物时怎么选择质量又好、价格又便宜的东西等等。\n当你选择其中一个的同时，就说明得放弃别的选择。\n因此，有人说成功关键在于正确的选择。\n只有在正确选择的基础上，你才有可能成功。\n\n40. ★ 根据这段话可以知道，“选择”：",
            "41. ★ 这段话告诉我们要：",
            "[42-43] 跟其他家在外地的大学毕业生一样，\n小张走出社会遇到的第一个大问题就是租房。\n那时，他每个月的工资不到 1000 元，除了吃穿，用来租房的钱剩不了多少。\n因此，他只好到处找便宜的房子。\n“当时我租的房子只能放一张床、一个桌子，洗澡、做饭得用公共的，\n但是每月房租才 280 元，房东也不错，我在那里住了 6 年。”小张说。\n这么便宜的房子现在肯定找不到了，\n也正是因为这么便宜的房租，他才能存下钱，付上了买房的首付款。\n\n42. ★ 对于家在外地的大学毕业生来说，走出社会首先遇到的最大困难是：",
            "43. ★ 根据这段话，可以知道小张："
        ]
        q35_43_options = [
            ["A. 冷天多吃辣", "B. 辣的食物不能多吃", "C. 辣的对胃好", "D. 要学会做辣菜"],
            ["A. 发展很快", "B. 人特别多", "C. 没有高楼", "D. 环境不好"],
            ["A. 得到成长", "B. 感到快乐", "C. 忘记失败", "D. 减少困难"],
            ["A. 怎样保护植物", "B. 水的作用", "C. 生命不可缺少的东西", "D. 阳光的颜色"],
            ["A. 选课", "B. 课前预习", "C. 汉语语法", "D. 对汉字的看法"],
            ["A. 需要别人帮助", "B. 是成功的关键", "C. 不用我们担心", "D. 只是暂时的"],
            ["A. 快速选择", "B. 不能放弃", "C. 正确选择", "D. 相信自己"],
            ["A. 找工作", "B. 租房子", "C. 买家具", "D. 学做饭"],
            ["A. 想租房", "B. 刚毕业", "C. 已买房", "D. 很有钱"]
        ]
        q35_43_ans = ["B", "C", "A", "C", "A", "B", "C", "B", "C"]
        user_q35_43 = []
        for i in range(9):
            st.markdown(f"<div class='question-card'>{q35_43_questions[i]}", unsafe_allow_html=True)
            ans = st.selectbox(f"Đáp án câu {i+35}:", ["Chưa chọn"] + q35_43_options[i], key=f"l19_read_p3_{i}")
            user_q35_43.append(ans[0] if ans != "Chưa chọn" else "Chưa chọn")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 NỘP BÀI PHẦN ĐỌC", key="l19_btn_sub_read"):
            if not student_name.strip():
                st.error("⚠️ Bạn hãy điền Họ và tên học sinh ở đầu trang trước khi nộp nhé!")
            else:
                correct_cnt = 0
                for i in range(4):
                    if user_q23_26[i] == q23_26_ans[i]: correct_cnt += 1
                for i in range(4):
                    if user_q27_30[i] == q27_30_ans[i]: correct_cnt += 1
                for i in range(4):
                    if user_q31_34[i] == q31_34_ans[i]: correct_cnt += 1
                for i in range(9):
                    if user_q35_43[i] == q35_43_ans[i]: correct_cnt += 1
                st.session_state.l19_r_sub = True
                st.session_state.l19_r_score = f"{correct_cnt}/21"
                st.success(f"Chúc mừng bạn đã làm xong bài tập nha. Điểm số của bạn là: {st.session_state.l19_r_score}.")
                send_results_to_gsheet(student_name, "Bài 19", "PHẦN ĐỌC", st.session_state.l19_r_score)

        if st.session_state.l19_r_sub:
            st.markdown("### 🔍 CHI TIẾT CÂU SAI & ĐÁP ÁN ĐÚNG:")
            for i in range(4):
                if user_q23_26[i] != q23_26_ans[i]:
                    st.markdown(f"<span style='color:#D32F2F;'>❌ Câu {i+23} sai:</span> {q23_26_texts[i]}", unsafe_allow_html=True)
                    st.markdown(f"👉 Đáp án đúng: **{q23_26_ans[i]}**")
            for i in range(4):
                if user_q27_30[i] != q27_30_ans[i]:
                    st.markdown(f"<span style='color:#D32F2F;'>❌ Câu {i+27} sai:</span> {q27_30_texts[i]}", unsafe_allow_html=True)
                    st.markdown(f"👉 Đáp án đúng: **{q27_30_ans[i]}**")
            for i in range(4):
                if user_q31_34[i] != q31_34_ans[i]:
                    st.markdown(f"<span style='color:#D32F2F;'>❌ Câu {i+31} sai:</span> Lựa chọn của bạn: `{user_q31_34[i]}`", unsafe_allow_html=True)
                    st.markdown(f"👉 Đáp án đúng: **{q31_34_ans[i]}**")
            for i in range(9):
                if user_q35_43[i] != q35_43_ans[i]:
                    st.markdown(f"<span style='color:#D32F2F;'>❌ Câu {i+35} sai:</span> Lựa chọn của bạn: `{user_q35_43[i]}`", unsafe_allow_html=True)
                    st.markdown(f"👉 Đáp án đúng: **{q35_43_ans[i]}**")

    # ------------------ PHẦN VIẾT BÀI 19 ------------------
    with t_write:
        st.markdown("### 三、书写 (Phần viết)")
        st.markdown("#### **第一部分 (Phần 1) - Sắp xếp câu hoàn chỉnh**")
        st.warning("⚠️ Chú ý: Phần viết được chấm tuyệt đối nghiêm ngặt. Sai bất kỳ 1 chữ hoặc 1 dấu câu nào cũng tính là sai hoàn toàn cả câu.")
        
        q44_48_words = [
            "44. 有 / 我这里 / 很多零钱 / 你 / 可以 / 借给",
            "45. 左右 / 房东 / 晚上 / 回来 / 每天 / 9点",
            "46. 学期 / 我选了 / 最喜欢的 / 中国 / 这个 / 音乐史",
            "47. 变得 / 破街道 / 以前 / 那条 / 热闹 / 真",
            "48. 收拾 / 的时候 / 把衣服 / 弄脏了 / 厨房 / 我"
        ]
        
        q44_48_acceptable_ans = [
            ["我这里有很多零钱可以借给你。"],
            ["房东每天晚上9点左右回来。", "房东每天晚上九点左右回来。"],
            ["这个学期我选了最喜欢的中国音乐史。"],
            ["以前那条破街道变得真热闹！", "以前那条破街道变得真热闹。"],
            ["我收拾厨房的时候把衣服弄脏了。"]
        ]
        
        user_q44_48 = []
        for i, words in enumerate(q44_48_words):
            st.markdown(f"<div class='question-card'><strong>Câu {i+44}:</strong> {words}", unsafe_allow_html=True)
            ans = st.text_input("Nhập câu hoàn chỉnh của bạn tại đây:", key=f"l19_write_p1_{i}").strip()
            user_q44_48.append(ans)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### **第二部分 (Phần 2) - Nhìn tranh đặt câu (Tự luận đối chiếu gợi ý)**")
        
        st.markdown("""
        <div class='question-card'>
            <strong>Câu 49:</strong> Tranh đĩa và dao nĩa ăn đồ Tây.<br>
            Từ gợi ý: <strong>刀</strong>
        </div>
        """, unsafe_allow_html=True)
        user_q49 = st.text_area("Viết câu tự luận của bạn tại đây:", key="l19_write_p2_49")
        
        st.markdown("""
        <div class='question-card'>
            <strong>Câu 50:</strong> Tranh khu dân cư biệt thự xanh đẹp.<br>
            Từ gợi ý: <strong>小区</strong>
        </div>
        """, unsafe_allow_html=True)
        user_q50 = st.text_area("Viết câu tự luận của bạn tại đây:", key="l19_write_p2_50")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 NỘP BÀI PHẦN VIẾT", key="l19_btn_sub_write"):
            if not student_name.strip():
                st.error("⚠️ Bạn hãy điền Họ và tên học sinh ở đầu trang trước khi nộp nhé!")
            else:
                correct_cnt = 0
                for i in range(5):
                    user_ans = user_q44_48[i].strip()
                    matched = False
                    for possible_ans in q44_48_acceptable_ans[i]:
                        if user_ans == possible_ans.strip():
                            matched = True
                            break
                    if matched:
                        correct_cnt += 1
                        
                st.session_state.l19_w_sub = True
                st.session_state.l19_w_score = f"{correct_cnt}/5"
                
                st.success(f"Chúc mừng bạn đã làm xong bài tập nha. Điểm số của bạn là: {st.session_state.l19_w_score}.")
                send_results_to_gsheet(student_name, "Bài 19", "PHẦN VIẾT", st.session_state.l19_w_score)

        if st.session_state.l19_w_sub:
            st.markdown("### 🔍 CHI TIẾT CÂU SAI & ĐÁP ÁN ĐÚNG:")
            for i in range(5):
                user_ans = user_q44_48[i].strip()
                matched = False
                for possible_ans in q44_48_acceptable_ans[i]:
                    if user_ans == possible_ans.strip():
                        matched = True
                        break
                if not matched:
                    st.markdown(f"<span style='color:#D32F2F;'>❌ Câu {i+44} viết chưa chính xác:</span>", unsafe_allow_html=True)
                    st.markdown(f"Đáp án của bạn: `{user_q44_48[i]}`")
                    st.markdown(f"👉 Đáp án đúng: **{q44_48_acceptable_ans[i][0]}**")
                    
            st.markdown("---")
            st.markdown("#### 💡 CÂU GỢI Ý MẪU CHO PHẦN ĐẶT CÂU THEO TRANH:")
            st.markdown("- **Câu 49 (刀):** `吃西餐用的刀一般都放在盘子右边。` *(Dao dùng ăn đồ Tây thường được đặt ở bên phải đĩa.)*")
            st.markdown("- **Câu 50 (小区):** `他们小区的环境很不错，又漂亮又安静。` *(Môi trường trong khu dân cư của họ rất tốt, vừa đẹp vừa yên tĩnh.)*")




# ==============================================================================
# HỆ THỐNG MENU VÀ TỰ ĐỘNG SẮP XẾP BÀI MỚI LÊN TRƯỚC (SCALABLE ARCHITECTURE)
# ==============================================================================

LESSONS = {
    "Bài 19: 生活的味道": show_lesson_19,
    "Bài 18: 科技与世界": show_lesson_18,
    "Bài 17: 人与自然": show_lesson_17,
    "Bài 16: 生活可以更美好": show_lesson_16,
}

# Tiêu đề bài học
st.markdown("<h1>BÀI TẬP HSK4 (TẬP 2)</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>🌸 Chúc các bạn học tập tốt và làm bài vui vẻ! 🌸</div>", unsafe_allow_html=True)

# Ô nhập họ tên học sinh ở đầu trang
student_name = st.text_input(
    "👤 Họ và tên học sinh:", 
    value=st.session_state.student_name,
    placeholder="Ví dụ: Nguyễn Văn A",
    key="name_input"
)
st.session_state.student_name = student_name

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<div style='font-size:16px; font-weight:700; color:#275338; margin-bottom:8px;'>📖 CHỌN BÀI HỌC:</div>", unsafe_allow_html=True)

# DÀN HÀNG NGANG CHỌN BÀI HỌC NGAY TRÊN TRANG CHÍNH (THÂN THIỆN ĐIỆN THOẠI)
lesson_keys = list(LESSONS.keys())

if hasattr(st, "pills"):
    selected_lesson = st.pills(
        label="Chọn bài học",
        options=lesson_keys,
        default=lesson_keys[0],
        label_visibility="collapsed"
    )
    if not selected_lesson:
        selected_lesson = lesson_keys[0]
else:
    selected_lesson = st.radio(
        label="Chọn bài học",
        options=lesson_keys,
        horizontal=True,
        label_visibility="collapsed"
    )

st.markdown("---")

# Gọi hàm hiển thị bài học đã chọn
if selected_lesson in LESSONS:
    st.markdown(f"## {selected_lesson}")
    LESSONS[selected_lesson](student_name)

# --- FOOTER ---
st.markdown("""
<div class="footer">
    黄宝玉老师
</div>
""", unsafe_allow_html=True)
