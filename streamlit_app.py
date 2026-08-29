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

# --- CSS CAO CẤP: ÉP MÀU CHỮ ĐEN XÁM, FORCE LIGHT MODE CHO MỌI THÀNH PHẦN ---
# Thiết kế tông màu xanh pastel dịu nhẹ (#F4F8F5) kết hợp trắng, che sạch nút deploy/menu hệ thống.
# Các hộp expander và ô nhập liệu bắt buộc nền trắng tinh khiết, chữ đen/đen xám đậm rõ nét, chống tàng hình chữ khi máy học sinh bật Dark Mode.
st.markdown("""
<style>
    /* 1. Nền trang xanh pastel dịu nhẹ lai trắng */
    .stApp {
        background-color: #F4F8F5 !important;
    }
    
    /* 2. Ép toàn bộ phông chữ sang màu đen xám rõ nét, nổi trên nền */
    html, body, p, span, label, li, h1, h2, h3, h4, h5, h6, 
    .stMarkdown, .stWidgetLabel, .stMarkdownContainer p,
    div[data-testid="stMarkdownContainer"] p,
    div[role="radiogroup"] label, div[role="radiogroup"] p,
    div[data-testid="stNotification"] p, div[data-testid="stNotification"] div,
    .st-emotion-cache-1dp5vir, .st-emotion-cache-ue694m,
    .st-emotion-cache-zt5g90, .st-emotion-cache-1kyx60b, .st-emotion-cache-1629630 {
        color: #333333 !important;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif !important;
        font-weight: 600 !important;
        text-shadow: 0.5px 0.5px 1px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* 3. Tiêu đề chính lớn nổi bật */
    h1 {
        color: #2E5A44 !important;
        font-weight: 700 !important;
        text-align: center;
        margin-bottom: 5px;
    }
    
    /* Lời chào dưới tiêu đề */
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #4A7A60 !important;
        font-weight: bold;
        margin-bottom: 25px;
    }

    /* Khung hiển thị câu hỏi màu nhạt, đơn giản, tinh tế, nổi nhẹ */
    .question-card {
        background-color: #FFFFFF !important;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E1ECE5 !important;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02) !important;
    }

    /* 4. Sửa lỗi khung đen mất chữ (Force Light Mode cho các widgets) */
    
    /* Ô lựa chọn (Selectbox / Dropdown) */
    div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E1ECE5 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #333333 !important;
    }
    div[data-baseweb="select"] span {
        color: #333333 !important;
        font-weight: 600 !important;
    }
    
    /* Danh sách tùy chọn khi mở Dropdown */
    ul[role="listbox"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E1ECE5 !important;
    }
    ul[role="listbox"] li {
        background-color: #FFFFFF !important;
        color: #333333 !important;
    }
    ul[role="listbox"] li:hover {
        background-color: #F1F8F4 !important;
        color: #2E5A44 !important;
    }

    /* Ô nhập văn bản (Text Input & Text Area) */
    div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea {
        background-color: #FFFFFF !important;
        color: #333333 !important;
        border: 1px solid #E1ECE5 !important;
        border-radius: 8px !important;
    }

    /* Khung code chứa từ vựng gợi ý ở trên đầu bài đọc */
    div[data-testid="stCodeBlock"], code, pre {
        background-color: #FFFFFF !important;
        border: 1px solid #E1ECE5 !important;
        border-radius: 8px !important;
    }
    div[data-testid="stCodeBlock"] pre {
        background-color: #FFFFFF !important;
        border: none !important;
        padding: 10px !important;
        margin: 0 !important;
    }
    div[data-testid="stCodeBlock"] code, code, pre {
        background-color: #FFFFFF !important;
        color: #333333 !important;
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 16px !important;
        font-weight: 700 !important;
    }

    /* 5. Cải tạo Khung xổ ra (st.expander) nền trắng chữ đen tuyền rõ nét */
    div[data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E1ECE5 !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
    }
    div[data-testid="stExpander"] details summary {
        background-color: #FFFFFF !important;
        color: #333333 !important;
        font-weight: 600 !important;
    }
    div[data-testid="stExpander"] details > div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border-top: 1px solid #F1F8F4 !important;
        padding: 15px !important;
    }
    /* Chữ bên trong Khung xổ ra bắt buộc đen tuyền */
    div[data-testid="stExpander"] p, 
    div[data-testid="stExpander"] span, 
    div[data-testid="stExpander"] strong,
    div[data-testid="stExpander"] div {
        color: #000000 !important;
        font-weight: 600 !important;
    }

    /* Định dạng Tabs */
    button[data-baseweb="tab"] {
        color: #555555 !important;
        font-weight: 600 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #2E5A44 !important;
        border-bottom-color: #2E5A44 !important;
    }
    
    /* Ẩn hoàn toàn các ký hiệu, menu và nút Deploy góc trên bên phải */
    header {
        visibility: hidden !important;
        height: 0px !important;
    }
    [data-testid="stHeader"] {
        display: none !important;
    }
    .stAppDeployButton {
        display: none !important;
    }
    div[data-testid="stDecoration"] {
        display: none !important;
    }
    div[data-testid="stStatusWidget"] {
        display: none !important;
    }

    /* Định dạng chân trang */
    .footer {
        text-align: center;
        padding: 30px 10px 10px 10px;
        font-size: 16px;
        color: #555555 !important;
        font-weight: bold;
        border-top: 1px solid #E1ECE5;
        margin-top: 50px;
    }
</style>
""", unsafe_allow_html=True)

# --- KHỞI TẠO STATE HỌC SINH ---
if 'student_name' not in st.session_state:
    st.session_state.student_name = ""

# --- WEBHOOK GỬI ĐIỂM VỀ GOOGLE SHEETS ---
# Giáo viên chỉ việc dán link Web App Google Apps Script mới vào đây
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


# ==============================================================================
# HỆ THỐNG MENU VÀ TỰ ĐỘNG SẮP XẾP BÀI MỚI LÊN TRƯỚC (SCALABLE ARCHITECTURE)
# ==============================================================================

# Khi bạn thêm bài học mới (ví dụ Bài 18, 19, 20...), bạn chỉ cần định nghĩa hàm tương tự như trên
# rồi khai báo thêm vào dictionary LESSONS dưới đây.
# Bộ máy Streamlit sẽ tự động hiển thị bài học mới nhất lên đầu tiên trong ô chọn bài tập!

LESSONS = {
    "Bài 17: 人与自然": show_lesson_17,
    "Bài 16: 生活可以更美好": show_lesson_16,
    # Thêm bài học mới trong tương lai tại đây, ví dụ:
    # "Bài 18: 科技与世界": show_lesson_18,
}

# Tiêu đề bài học
st.markdown("<h1>BÀI TẬP BÀI HSK4 (TẬP 2)</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Chúc các bạn làm bài vui!</div>", unsafe_allow_html=True)

# sidebar chọn bài học (Bài mới thêm vào sẽ tự động nằm lên đầu vì dictionary được sắp xếp theo thứ tự khai báo)
lesson_keys = list(LESSONS.keys())
selected_lesson = st.sidebar.selectbox("📖 Chọn bài học để làm:", lesson_keys)

# Ô nhập họ tên học sinh ở đầu trang
student_name = st.text_input(
    "👤 Họ và tên học sinh:", 
    value=st.session_state.student_name,
    placeholder="Ví dụ: Nguyễn Văn A",
    key="name_input"
)
st.session_state.student_name = student_name

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
