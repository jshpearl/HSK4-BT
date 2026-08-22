import streamlit as st
import requests
import os

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="BÀI TẬP BÀI 16 (HSK4)",
    page_icon="📚",
    layout="wide"
)

# --- CSS PHONG CÁCH ĐƠN GIẢN, CHỮ ĐEN ĐẬM TUYỆT ĐỐI ---
# Ép toàn bộ màu chữ của mọi thành phần trên trang thành màu đen (#000000)
# Sử dụng nét phân cách đứt đơn giản thay vì các khung nền phức tạp
st.markdown("""
<style>
    /* Nền trang xanh pastel dịu nhẹ */
    .stApp {
        background-color: #F4F9F4 !important;
    }
    
    /* Ép tất cả các văn bản, tiêu đề, nhãn widget, lựa chọn sang màu đen đậm nguyên bản */
    *, p, span, label, h1, h2, h3, h4, h5, h6, li, option, select, input, button, div,
    .stMarkdown, .stWidgetLabel, .stMarkdownContainer p,
    div[data-testid="stMarkdownContainer"] p,
    div[role="radiogroup"] label, div[role="radiogroup"] p,
    div[data-testid="stNotification"] p, div[data-testid="stNotification"] div {
        color: #000000 !important;
        font-weight: 700 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
    }

    /* Phong cách tối giản: phân cách câu hỏi bằng nét đứt mỏng màu xanh nhạt */
    .question-card {
        padding: 15px 0px;
        border-bottom: 1px dashed #C8E6C9;
        margin-bottom: 15px;
    }
    
    /* Ẩn hoàn toàn các nút hệ thống góc trên bên phải để tối giản giao diện */
    header, [data-testid="stDecoration"], [data-testid="stStatusWidget"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Chân trang của giáo viên */
    .footer {
        text-align: center;
        padding: 25px 10px 10px 10px;
        font-size: 18px;
        border-top: 1px dashed #C8E6C9;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)

# --- WEBHOOK GỬI ĐIỂM VỀ GOOGLE SHEETS ---
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbxfZ7f292zc7Rcq8OdalCQIKl9WDY1fAc21pBMAmXFKr1qnQ3F8FeH-vJqIebuWKQ1U8A/exec"

def send_score_to_sheets(student_name, section_name, score):
    payload = {
        "name": student_name,
        "lesson": f"Bài 16 (HSK4) - {section_name}",
        "score": score
    }
    try:
        requests.post(WEBHOOK_URL, json=payload)
    except:
        pass

# --- HÀM PHÁT FILE NGHE AN TOÀN TUYỆT ĐỐI (KHÔNG CƠ HỘI GÂY CRASH TRANG) ---
# Kiểm tra sự tồn tại của file trước khi phát, nếu không có thì hiện thông báo hướng dẫn gọn gàng chứ không crash.
def play_audio(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, "rb") as f:
                audio_bytes = f.read()
            st.audio(audio_bytes, format="audio/mp3")
        except Exception as e:
            st.warning(f"⚠️ Có lỗi khi đọc tệp âm thanh cục bộ: {e}")
    else:
        st.error(f"⚠️ Không tìm thấy tệp nghe tại đường dẫn: `{file_path}`. "
                 f"Bạn hãy chắc chắn đã tải thư mục `audio` chứa các tệp nghe lên đúng thư mục gốc của GitHub Repository của bạn.")

# Đường dẫn file nghe cục bộ
AUDIO_16_1 = "audio/16-1.mp3"
AUDIO_16_2 = "audio/16-2.mp3"
AUDIO_16_3 = "audio/16-3.mp3"

# Khởi tạo trạng thái làm bài của học sinh
if 'listening_submitted' not in st.session_state:
    st.session_state.listening_submitted = False
if 'reading_submitted' not in st.session_state:
    st.session_state.reading_submitted = False
if 'writing_submitted' not in st.session_state:
    st.session_state.writing_submitted = False
if 'student_name' not in st.session_state:
    st.session_state.student_name = ""

# --- TIÊU ĐỀ TRANG WEB ---
st.markdown("<h1>📚 BÀI TẬP BÀI 16 (HSK4)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; color: #000000; font-weight: bold;'>Chúc các bạn làm bài vui!</p>", unsafe_allow_html=True)

# Nhập tên học sinh
student_name = st.text_input(
    "👤 Nhập họ và tên học viên:",
    value=st.session_state.student_name,
    placeholder="Nhập tên của bạn tại đây..."
)
st.session_state.student_name = student_name

# Tạo 3 Tabs tương ứng với các kỹ năng
tab_listening, tab_reading, tab_writing = st.tabs(["🎧 PHẦN NGHE (听力)", "📖 PHẦN ĐỌC (阅读)", "✍️ PHẦN VIẾT (书写)"])

# ==========================================
# 1. TAB LISTENING (PHẦN NGHE)
# ==========================================
with tab_listening:
    st.markdown("## 🎧 一、听力 (Phần nghe)")
    
    # --- PART 1 ---
    st.markdown("### 第一部分 (Phần 1) - 判断对错")
    st.info("💡 Nghe audio và chọn Đúng (✔) hoặc Sai (✘) cho mỗi câu dưới đây.")
    play_audio(AUDIO_16_1)
    
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
            ans = st.radio(f"Chọn đáp án câu {i+1}:", ["Chưa chọn", "✔ (Đúng)", "✘ (Sai)"], key=f"lis_p1_{i}")
            user_q1_5.append(ans)
            st.markdown("</div>", unsafe_allow_html=True)
            
    # --- PART 2 ---
    st.markdown("---")
    st.markdown("### 第二部分 (Phần 2) - 单项选择")
    play_audio(AUDIO_16_2)
    
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
            ans = st.selectbox(f"Chọn đáp án câu {i+6}:", ["Chưa chọn"] + q6_12_options[i], key=f"lis_p2_{i}")
            user_q6_12.append(ans[0] if ans != "Chưa chọn" else "Chưa chọn")
            st.markdown("</div>", unsafe_allow_html=True)

    # --- PART 3 ---
    st.markdown("---")
    st.markdown("### 第三部分 (Phần 3) - 单项选择")
    play_audio(AUDIO_16_3)
    
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
            ans = st.selectbox(f"Chọn đáp án câu {i+13}:", ["Chưa chọn"] + q13_22_options[i], key=f"lis_p3_{i}")
            user_q13_22.append(ans[0] if ans != "Chưa chọn" else "Chưa chọn")
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 NỘP BÀI PHẦN NGHE", key="btn_sub_listening"):
        if not student_name.strip():
            st.error("⚠️ Vui lòng nhập họ và tên ở đầu trang trước khi nộp bài!")
        else:
            correct_cnt = 0
            for i in range(5):
                user_val = "✔" if "✔" in user_q1_5[i] else "✘" if "✘" in user_q1_5[i] else "Chưa chọn"
                if user_val == q1_5_ans[i]:
                    correct_cnt += 1
            for i in range(7):
                if user_q6_12[i] == q6_12_ans[i]:
                    correct_cnt += 1
            for i in range(10):
                if user_q13_22[i] == q13_22_ans[i]:
                    correct_cnt += 1
            
            st.session_state.listening_submitted = True
            st.session_state.listening_score = f"{correct_cnt}/22"
            
            st.success("🎉 Chúc mừng bạn đã làm xong bài tập nha")
            st.info(f"📊 Điểm số của bạn là: {st.session_state.listening_score}.")
            
            # Gửi kết quả về Google Sheets
            send_score_to_sheets(student_name, "Phần Nghe", st.session_state.listening_score)

    if st.session_state.listening_submitted:
        st.markdown("### 🔍 CHI TIẾT BÀI LÀM & ĐÁP ÁN:")
        st.markdown("#### **Phần 1:**")
        for i in range(5):
            user_val = "✔" if "✔" in user_q1_5[i] else "✘" if "✘" in user_q1_5[i] else "Chưa chọn"
            is_correct = user_val == q1_5_ans[i]
            status = "✅ Đúng" if is_correct else "❌ Sai"
            st.markdown(f"**Câu {i+1}:** Lựa chọn: `{user_val}` -> {status}")
            if not is_correct:
                with st.expander(f"📖 Xem Lời thoại (Script) & Giải thích Câu {i+1}"):
                    scripts = [
                        """**Script:** 办签证需要准备哪些材料，我也不太清楚，不过我有大使馆的电话号码，我可以帮你问一下。
(Tôi cũng không rõ cần chuẩn bị giấy tờ gì để làm visa, nhưng tôi có số điện thoại của Đại sứ quán, để tôi hỏi giúp bạn.)

**Giải thích:** Đề bài bảo "Anh ấy biết cách làm visa" -> Sai (✘).""",
                        """**Script:** 只有通过了考试，完全符合要求后，护士才能正式开始工作。医院对护士这一职业的要求是：专业、负责、尊重生命。
(Chỉ sau khi vượt qua kỳ thi và hoàn toàn đáp ứng yêu cầu, y tá mới có thể chính thức bắt đầu làm việc. Yêu cầu của bệnh viện đối với nghề y tá là: chuyên nghiệp, trách nhiệm và tôn trọng sinh mệnh.)

**Giải thích:** Đề bài bảo "Y tá phải thi trước khi làm việc" -> Đúng (✔).""",
                        """**Script:** 第一次跟女朋友见面的时候，他紧张极了，脸和耳朵都红了，几乎不敢看女朋友的眼睛。
(Lần đầu gặp bạn gái, anh ấy vô cùng căng thẳng, mặt và tai đều đỏ bừng, hầu như không dám nhìn vào mắt cô ấy.)

**Giải thích:** Đề bài bảo "Anh ấy rất thư giãn trong lần đầu gặp bạn gái" -> Sai (✘).""",
                        """**Script:** 这篇文章你还得拿回去好好改改，主要是内容有点儿乱，重点不够清楚，另外，有几个句子还有语法问题。
(Bài viết này bạn phải mang về sửa lại thật kỹ, chủ yếu là nội dung hơi lộn xộn, trọng tâm chưa rõ ràng, ngoài ra một số câu còn gặp vấn đề ngữ pháp.)

**Giải thích:** Đề bài bảo "Bài viết viết rất xuất sắc" -> Sai (✘).""",
                        """**Script:** 受到批评时，也别伤心失望，谁都有做错事或者做得不够好的时候。只要不放弃努力，你就仍然有希望。
(Khi bị phê bình thì cũng đừng đau lòng thất vọng, ai cũng có lúc làm sai hoặc làm chưa đủ tốt. Chỉ cần không từ bỏ nỗ lực, bạn vẫn luôn có hy vọng.)

**Giải thích:** Đề bài bảo "Lúc làm chưa tốt đừng thất vọng" -> Đúng (✔)."""
                    ]
                    st.markdown(scripts[i])

        st.markdown("#### **Phần 2:**")
        for i in range(7):
            is_correct = user_q6_12[i] == q6_12_ans[i]
            status = "✅ Đúng" if is_correct else f"❌ Sai (Đáp án đúng: {q6_12_ans[i]})"
            st.markdown(f"**Câu {i+6}:** Bạn chọn: `{user_q6_12[i]}` -> {status}")
            if not is_correct:
                with st.expander(f"📖 Xem Lời thoại (Script) & Giải thích Câu {i+6}"):
                    scripts_p2 = [
                        """**Script:**
男：喂，姐，我找到你的成绩单了，给你寄过去吗？
女：你还是发传真吧，我现在就要。
问：男的找到什么了？

**Giải thích:** Lựa chọn đúng là B (成绩单 - Bảng điểm) vì người nam nói tìm thấy bảng điểm của người nữ.""",
                        """**Script:**
男：你钢琴弹得这么好，怎么没去参加比赛呢？
女：我错过了报名时间，只能等下次了。
问：女的为什么没参加比赛？

**Giải thích:** Lựa chọn đúng là C (没有报名 - Chưa đăng ký) vì người nữ bị bỏ lỡ thời gian đăng ký.""",
                        """**Script:**
男：已经两点了，你怎么还不睡觉？
女：这本小说还有几页，我想看看最后到底怎么样了。
问：女的为什么还不睡？

**Giải thích:** Lựa chọn đúng là D (在看小说 - Đang đọc tiểu thuyết) vì người nữ cố đọc nốt mấy trang tiểu thuyết cuối.""",
                        """**Script:**
女：我们想了解一下客人对我们宾馆的服务是不是满意，您只需要填个表格就行。
男：好的，没问题，希望表格不要太复杂。
问：女的请男的做什么？

**Giải thích:** Lựa chọn đúng là B (填表格 - Điền biểu mẫu) vì người nữ yêu cầu điền tờ khảo sát dịch vụ khách sạn.""",
                        """**Script:**
女：小刘，帮我把公司的这两页材料传真给李记者，他下周的一篇新闻里要用这些数字。
男：好，我马上去。他的传真号码是多少？
问：对话最可能发生在哪儿？

**Giải thích:** Lựa chọn đúng là C (公司 - Công ty) vì họ đang trao đổi xử lý tài liệu công việc văn phòng.""",
                        """**Script:**
男：现在有的人二十多岁了还没学会照顾自己，而有的人十几岁就开始工作，赚钱养家。
女：年龄大并不一定代表有能力，穷人的孩子早当家，他们也许没有很多钱，却可能比富人家的孩子经历得更多。
问：十几岁就工作的人怎么样？

**Giải thích:** Lựa chọn đúng là A (经历丰富 - Trải nghiệm phong phú) vì người nữ cho biết họ đã trải qua và trải nghiệm nhiều hơn.""",
                        """**Script:**
男：你叔叔太厉害了，他的书里写了那么多地方的景色，这些地方他都去过吗？
女：我叔叔以前是记者，因为职业的关系，他几乎走遍了中国所有的地方... 后来他就把自己的经历写成了一本书。
问：根据对话，可以知道女的的叔叔怎么样？

**Giải thích:** Lựa chọn đúng là D (去过很多地方 - Đi nhiều nơi) vì chú của người nữ làm phóng viên và đã đi khắp nơi trên đất nước."""
                    ]
                    st.markdown(scripts_p2[i])

        st.markdown("#### **Phần 3:**")
        for i in range(10):
            is_correct = user_q13_22[i] == q13_22_ans[i]
            status = "✅ Đúng" if is_correct else f"❌ Sai (Đáp án đúng: {q13_22_ans[i]})"
            st.markdown(f"**Câu {i+13}:** Bạn chọn: `{user_q13_22[i]}` -> {status}")
            if not is_correct:
                with st.expander(f"📖 Xem Lời thoại (Script) & Giải thích Câu {i+13}"):
                    scripts_p3 = [
                        """**Script:**
男：您好，我想办一张信用卡。
女：办信用卡的话，您得先填一下这张表格。
问：关于男的，可以知道什么？

**Giải thích:** Lựa chọn đúng là D (要填表格) vì người nữ bảo muốn làm thẻ tín dụng trước hết phải điền tờ đơn.""",
                        """**Script:**
女：这是女儿专门给我们画的。
男：这张画儿的景色实在太漂亮了！你看，花草画得像真的一样。
女：我想把它挂起来，天天看。
男：好主意, 就挂在书房的墙上吧。
问：男的想把画儿挂在哪儿？

**Giải thích:** Lựa chọn đúng là B (书房 - Phòng đọc sách).""",
                        """**Script:**
女：我们坐出租车去机场吧？
男：现在正是上下班时间，路上可堵了，坐出租车去恐怕时间来不及。
女：那怎么办？坐地铁去？
男：坐地铁应该来得及，飞机还有两个半小时才起飞。
问：男的打算怎么去机场？

**Giải thích:** Lựa chọn đúng là A (坐地铁) để tránh bị tắc đường lúc cao điểm.""",
                        """**Script:**
女：你怎么了？什么事让你不高兴？
男：下午的足球比赛我们班输了。
女：比赛总是有输有赢，下次再努力。
男：就差一个球，实在太可惜了。
问：男的为什么不高兴？

**Giải thích:** Lựa chọn đúng là C (比赛输了) vì đội bóng lớp bạn nam thua tiếc nuối.""",
                        """**Script:**
男：你的包里没有？是不是忘办公室了？
女：不会，刚才是我开的门。
男：那你到底放哪儿了？你再仔细找找。
女：我去门口看看，是不是掉那儿了。
问：他们最可能在找什么？

**Giải thích:** Lựa chọn đúng là B (钥匙) vì người nữ nhắc tới việc mình vừa mới tự mở cửa.""",
                        """**Script:**
男：见到你真高兴！你已经硕士毕业了吧？
女：是的，我去年就毕业了，但还没参加工作呢，毕业后直接读博士了。
男：还是读经济学吗？
女：对，研究方向是国际经济。
问：女的读哪个专业？

**Giải thích:** Lựa chọn đúng là B (经济学 - Ngành kinh tế học).""",
                        """**Script:**
母亲对女儿说：“选丈夫不能马虎，一定要考虑清楚。你看你爸，什么都会修，冰箱、洗衣机，连汽车坏了他都能修……”没等母亲说完，女儿就说：“我明白了！”
问：她们在谈什么？

**Giải thích:** Lựa chọn đúng là D (选择丈夫 - Chọn chồng) vì hai mẹ con đang bàn về tiêu chí kén chồng.""",
                        """**Script:**
没想到母亲接着说：“你明白什么啊！如果你也找个像你爸这样的丈夫，就别想用上新东西了。”
问：关于女孩儿的爸爸，可以知道什么？

**Giải thích:** Lựa chọn đúng là B (爱修东西) vì đồ hỏng là bố đều sửa dùng tiếp, không cho mua đồ mới.""",
                        """**Script:**
我弟弟叫王小帅，今年四年级。他最大的特点是不爱学习，课前不预习，考前不复习，几乎没按时完成过作业。
问：关于王小帅，可以知道什么？

**Giải thích:** Lựa chọn đúng là B (不爱学习) vì không học bài, không làm bài tập đầy đủ.""",
                        """**Script:**
一天，他骄傲地对我说：“哥，今天老师问了个问题，除了我，谁也答不出来！”我都不敢相信自己的耳朵，问他是什么问题，他说：“老师问：‘谁没交作业？’”
问：说话人说“不敢相信自己的耳朵”是什么意思？

**Giải thích:** Lựa chọn đúng là A (很怀疑 - Ngạc nhiên/Nghi ngờ) vì ngạc nhiên khi thấy cậu em học dốt lại tự tin trả lời được câu hỏi độc nhất."""
                    ]
                    st.markdown(scripts_p3[i])


# ==========================================
# 2. TAB READING (PHẦN ĐỌC)
# ==========================================
with tab_reading:
    st.markdown("## 📖 二、阅读 (Phần đọc)")
    
    # --- PART 1 ---
    st.markdown("### 第一部分 (Phần 1) - 选词填空")
    st.markdown("#### **第 23-26 题：**")
    st.code("A 冷静    B 尊重    C 敢    D 坚持    E 呀")
    
    q23_26_texts = [
        "23. 哥，你快来看，这是什么植物（ ）？叶子怎么这么宽？",
        "24. 做事情不要一开始就考虑太多，害怕失败，什么都不（ ）做怎么可能成功？",
        "25. 邀请别人吃饭，至少要提前一天联系。首先，这是对被邀请人表示（ ）；其次，也方便别人做好安排。",
        "26. 当事情没有按照原来的计划进行时，不要太着急、太担心，而应该使自己（ ）下来，态度积极地去想解决问题的办法。"
    ]
    q23_26_ans = ["E", "C", "B", "A"]
    user_q23_26 = []
    
    col1, col2 = st.columns(2)
    for i, q_text in enumerate(q23_26_texts):
        target_col = col1 if i < 2 else col2
        with target_col:
            st.markdown(f"<div class='question-card'><strong>{q_text}</strong>", unsafe_allow_html=True)
            ans = st.selectbox(f"Chọn từ điền câu {i+23}:", ["Chưa chọn", "A", "B", "C", "D", "E"], key=f"read_p1_1_{i}")
            user_q23_26.append(ans)
            st.markdown("</div>", unsafe_allow_html=True)
            
    st.markdown("#### **第 27-30 题：**")
    st.code("A 激动    B 挂    C 温度    D 报名    E 郊区")
    
    q27_30_texts = [
        "27. A：我那件红衬衫呢？你放哪儿了？\n    B：洗了，在外边（ ）着，还没干呢。你穿这件就很好，很精神。",
        "28. A：去植物园玩儿的同事一共是十二位，现在还有人要（ ）吗？\n    B：我也想去。明天我们大概去多长时间？几点能回来呢？",
        "29. A：外面雪下得这么大，那些小伙子们怎么都跑外边去了？\n    B：他们都是南方人，南方冬天很少下雪，更不用说这么大的雪，所以他们肯定特别（ ）。",
        "30. A：现在城市里越来越多的人喜欢到（ ）过周末了。\n    B：是啊，那里空气新鲜、环境安静，可以让人好好放松一下。"
    ]
    q27_30_ans = ["B", "D", "A", "E"]
    user_q27_30 = []
    
    for i, q_text in enumerate(q27_30_texts):
        target_col = col1 if i < 2 else col2
        with target_col:
            st.markdown(f"<div class='question-card'><strong>{q_text}</strong>", unsafe_allow_html=True)
            ans = st.selectbox(f"Chọn từ điền câu {i+27}:", ["Chưa chọn", "A", "B", "C", "D", "E"], key=f"read_p1_2_{i}")
            user_q27_30.append(ans)
            st.markdown("</div>", unsafe_allow_html=True)

    # --- PART 2 ---
    st.markdown("---")
    st.markdown("### 第二部分 (Phần 2) - 排列顺序")
    
    q31_34_texts = [
        "**31.**\nA 因此，预习是学习的第一步\nB 上课的时候，学习效果才会更好\nC 提前对要学的内容有个大概的了解",
        "**32.**\nA 结果眼睛越来越不好\nB 所以现在我不敢再躺着看书了\nC 拿我来说，小时候我总喜欢躺在床上看书",
        "**33.**\nA 我们还是把它推到里面去吧\nB 沙发太大了，放这儿容易堵着门，进出不方便\nC 把这个地方空出来",
        "**34.**\nA 也许你会发现，这些事情其实用不着烦恼\nB 每次发脾气前，请先给自己几分钟\nC 冷静地想一想，是不是值得为此生气"
    ]
    q31_34_ans = ["CBA", "CAB", "BAC", "BCA"]
    user_q31_34 = []
    
    for i, q_text in enumerate(q31_34_texts):
        st.markdown(f"<div class='question-card'>{q_text}", unsafe_allow_html=True)
        ans = st.text_input(f"Nhập thứ tự câu {i+31} (Ví dụ: ABC):", key=f"read_p2_{i}").strip().upper()
        user_q31_34.append(ans)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- PART 3 ---
    st.markdown("---")
    st.markdown("### 第三部分 (Phần 3) - 阅读理解")
    
    q35_43_questions = [
        "35. 每年有成千上万的高中毕业生报名参加电影学院的艺术考试，他们中很多人都抱着成为著名演员的理想，但其实大部分考生并不清楚表演到底是什么。\n★ 根据这段话，很多考生：",
        "36. 举办这次活动，主要是为了向大家介绍我们公司推出的最新手机，希望通过这次活动引起大家的兴趣，让大家更了解我们。\n★ 举办这次活动是为了：",
        "37. 在别人伤心难过的时候，我们总会对他/她表示同情。同情是最美好的情感之一，然而同情并不是高高在上的关心，它应该是对别人的理解、尊重和支持。\n★ 这段话认为，同情别人：",
        "38. 现在的输或者赢都只是暂时的，没有人会永远输，也没有人会一直赢。生活的关键就是：只要你敢想、敢做、积极努力了，那么无论是输还是赢，生活都一样精彩。\n★ 根据这段话，可以知道：",
        "39. 耳朵每天都帮助我们听到各种各样的声音，但我们可不像重视眼睛、鼻子那样重视它。很多时候人们常常感觉不到它，甚至忘记了它。其实我们都错了，有研究发现，通过耳朵可以看出一个人是不是健康，甚至是什么样的性格。\n★ 这段话主要讲：",
        "**** “我找林医生，我有急事！”一位妈妈非常着急地给林医生打电话，林医生的妻子接的电话... “我的小儿子刚才把我的手表吃到肚子里了，林医生什么时候能回来？”“两个小时左右。”... “这段时间我该怎么办呀？”“我很抱歉，您恐怕只能先用另一块儿手表了。”\n\n40. ★ 孩子怎么了？",
        "41. ★ 关于林医生，可以知道什么？",
        "**** 父母是孩子第一位老师，也是最重要的老师。父母不仅要帮助孩子认识世界，教会他们知识，还应该帮助孩子养成好的生活习惯... 比如睡前刷牙、节约用水... \n\n42. ★ 根据这段话，父母有什么责任？",
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
        ["A. 保护孩子安全", "B. 教育孩子", "C. 回答问题", "D. 替孩子做 quyết định"],
        ["A. 过程会很慢", "B. 会比较轻松", "C. 与年龄有关", "D. 受父母影响"]
    ]
    q35_43_ans = ["C", "D", "D", "C", "C", "D", "A", "B", "D"]
    user_q35_43 = []
    
    for i in range(9):
        st.markdown(f"<div class='question-card'>{q35_43_questions[i]}", unsafe_allow_html=True)
        ans = st.selectbox(f"Chọn đáp án câu {i+35}:", ["Chưa chọn"] + q35_43_options[i], key=f"read_p3_{i}")
        user_q35_43.append(ans[0] if ans != "Chưa chọn" else "Chưa chọn")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 NỘP BÀI PHẦN ĐỌC", key="btn_sub_reading"):
        if not student_name.strip():
            st.error("⚠️ Vui lòng nhập họ và tên ở đầu trang trước khi nộp bài!")
        else:
            correct_cnt = 0
            for i in range(4):
                if user_q23_26[i] == q23_26_ans[i]:
                    correct_cnt += 1
            for i in range(4):
                if user_q27_30[i] == q27_30_ans[i]:
                    correct_cnt += 1
            for i in range(4):
                if user_q31_34[i] == q31_34_ans[i]:
                    correct_cnt += 1
            for i in range(9):
                if user_q35_43[i] == q35_43_ans[i]:
                    correct_cnt += 1
                    
            st.session_state.reading_submitted = True
            st.session_state.reading_score = f"{correct_cnt}/21"
            
            st.success("🎉 Chúc mừng bạn đã làm xong bài tập nha")
            st.info(f"📊 Điểm số của bạn là: {st.session_state.reading_score}.")
            
            # Gửi kết quả về Google Sheets
            send_score_to_sheets(student_name, "Phần Đọc", st.session_state.reading_score)

    if st.session_state.reading_submitted:
        st.markdown("### 🔍 CHI TIẾT BÀI LÀM & ĐÁP ÁN ĐÚNG:")
        for i in range(4):
            is_correct = user_q23_26[i] == q23_26_ans[i]
            status = "✅ Đúng" if is_correct else f"❌ Sai (Đáp án đúng: {q23_26_ans[i]})"
            st.markdown(f"**Câu {i+23}:** Bạn chọn: `{user_q23_26[i]}` -> {status}")
            
        for i in range(4):
            is_correct = user_q27_30[i] == q27_30_ans[i]
            status = "✅ Đúng" if is_correct else f"❌ Sai (Đáp án đúng: {q27_30_ans[i]})"
            st.markdown(f"**Câu {i+27}:** Bạn chọn: `{user_q27_30[i]}` -> {status}")
            
        for i in range(4):
            is_correct = user_q31_34[i] == q31_34_ans[i]
            status = "✅ Đúng" if is_correct else f"❌ Sai (Đáp án đúng: {q31_34_ans[i]})"
            st.markdown(f"**Câu {i+31}:** Bạn chọn: `{user_q31_34[i]}` -> {status}")
            
        for i in range(9):
            is_correct = user_q35_43[i] == q35_43_ans[i]
            status = "✅ Đúng" if is_correct else f"❌ Sai (Đáp án đúng: {q35_43_ans[i]})"
            st.markdown(f"**Câu {i+35}:** Bạn chọn: `{user_q35_43[i]}` -> {status}")


# ==========================================
# 3. TAB WRITING (PHẦN VIẾT)
# ==========================================
with tab_writing:
    st.markdown("## ✍️ 三、书写 (Phần viết)")
    
    # --- PART 1 ---
    st.markdown("### 第一部分 (Phần 1) - Sắp xếp câu thành câu hoàn chỉnh")
    st.warning("⚠️ Chú ý: Phần viết sai một chữ cũng tính là sai hoàn toàn câu. Hãy nhập chính xác dấu câu (dấu câu tiếng Trung như '。' hoặc '？').")
    
    q44_48_words = [
        "44. 200    估计    王老师    报名人数    会    超过",
        "45. 传真号码    是    你们    多少    公司    的",
        "46. 请    帮我    一个    当地导游    你能    吗",
        "47. 失望    让    那个    很    电影    观众",
        "48. 是    好消息    激动人心的    实在    一个    这"
    ]
    
    q44_48_acceptable_ans = [
        ["王老师估计报名人数会超过200。", "估计王老师报名人数会超过200。"],
        ["你们公司的传真号码是多少？", "你们公司传真号码是多少？"],
        ["你能帮我请一个当地导游吗？", "你能帮我请个当地导游吗？"],
        ["那个电影让观众很失望。", "那个电影很让观众失望。"],
        ["这实在是一个激动人心的好消息。", "这实在是个激动人心的好消息。"]
    ]
    
    user_q44_48 = []
    for i, words in enumerate(q44_48_words):
        st.markdown(f"<div class='question-card'><strong>Câu {i+44}:</strong> {words}", unsafe_allow_html=True)
        ans = st.text_input(f"Nhập câu hoàn chỉnh của bạn tại đây:", key=f"write_p1_{i}").strip()
        user_q44_48.append(ans)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- PART 2 ---
    st.markdown("---")
    st.markdown("### 第二部分 (Phần 2) - Nhìn tranh đặt câu (Tự luận học sinh tự đối chiếu đáp án gợi ý)")
    
    st.markdown("""
    <div class='question-card'>
        <strong>Câu 49:</strong> (Hình ảnh một tiểu soái ca/chàng trai đang chơi bóng rổ)<br>
        Từ gợi ý: <strong>小伙子</strong>
    </div>
    """, unsafe_allow_html=True)
    user_q49 = st.text_area("Viết câu của bạn:", key="write_p2_49")
    
    st.markdown("""
    <div class='question-card'>
        <strong>Câu 50:</strong> (Hình ảnh tay một người đang cầm bút viết điền vào bảng biểu)<br>
        Từ gợi ý: <strong>表格</strong>
    </div>
    """, unsafe_allow_html=True)
    user_q50 = st.text_area("Viết câu của bạn:", key="write_p2_50")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 NỘP BÀI PHẦN VIẾT", key="btn_sub_writing"):
        if not student_name.strip():
            st.error("⚠️ Vui lòng nhập họ và tên ở đầu trang trước khi nộp bài!")
        else:
            correct_cnt = 0
            for i in range(5):
                user_ans_clean = user_q44_48[i].replace(" ", "")
                matched = False
                for possible_ans in q44_48_acceptable_ans[i]:
                    if user_ans_clean == possible_ans.replace(" ", ""):
                        matched = True
                        break
                if matched:
                    correct_cnt += 1
                    
            st.session_state.writing_submitted = True
            st.session_state.writing_score = f"{correct_cnt}/5"
            
            st.success("🎉 Chúc mừng bạn đã làm xong bài tập nha")
            st.info(f"📊 Điểm số của bạn là: {st.session_state.writing_score} (Chỉ tính điểm tự động phần Sắp xếp câu).")
            
            # Gửi kết quả về Google Sheets
            send_score_to_sheets(student_name, "Phần Viết", st.session_state.writing_score)

    if st.session_state.writing_submitted:
        st.markdown("### 🔍 CHI TIẾT BÀI LÀM & ĐÁP ÁN ĐÚNG:")
        for i in range(5):
            user_ans_clean = user_q44_48[i].replace(" ", "")
            matched = False
            for possible_ans in q44_48_acceptable_ans[i]:
                if user_ans_clean == possible_ans.replace(" ", ""):
                    matched = True
                    break
            status = "✅ Đúng" if matched else "❌ Sai"
            st.markdown(f"**Câu {i+44}:** Bạn viết: `{user_q44_48[i]}` -> {status}")
            st.markdown(f"👉 Đáp án chuẩn: **{q44_48_acceptable_ans[i][0]}**")
            
        st.markdown("---")
        st.markdown("#### 💡 GỢI Ý CÂU VIẾT CHO PHẦN 2 (Đặt câu theo tranh):")
        st.markdown("- **Câu 49 (小伙子):** `我经常在体育馆遇见这个小伙子，他非常喜欢打篮球。` *(Tôi thường gặp chàng trai này ở nhà thi đấu, anh ấy rất thích chơi bóng rổ.)*")
        st.markdown("- **Câu 50 (表格):** `办签证时大使馆会要求你仔细填一张表格。` *(Khi xin visa đại sứ quán sẽ yêu cầu bạn điền cẩn thận một tờ đơn.)*")

# --- FOOTER ---
st.markdown("""
<div class="footer">
    黄宝玉老师
</div>
""", unsafe_allow_html=True)
