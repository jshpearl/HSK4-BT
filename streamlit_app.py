import streamlit as st
import requests
import json

# --- CONFIGURATION & PAGE SETTINGS ---
st.set_page_config(
    page_title="BÀI TẬP BÀI 16 (HSK4)",
    page_icon="📚",
    layout="wide"
)

# --- CSS FOR HIGH CONTRAST & PASTEL STYLING ---
# Toàn bộ chữ màu đen đậm tuyệt đối (#000000), dễ nhìn, không viết ký hiệu thừa
st.markdown("""
<style>
    /* Nền trang xanh nhạt pastel dịu nhẹ */
    .stApp {
        background-color: #F4F9F4 !important;
    }
    
    /* Ép tất cả văn bản sang màu đen đậm nguyên bản */
    h1, h2, h3, h4, h5, h6, p, label, span, li, option, select, 
    div[data-testid="stMarkdownContainer"] p, 
    .st-emotion-cache-1dp5vir, .st-emotion-cache-ue694m,
    .stWidgetLabel, div[role="radiogroup"] label, div[role="radiogroup"] p,
    div[data-testid="stNotification"] p, div[data-testid="stNotification"] div {
        color: #000000 !important;
        font-weight: 700 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
    }
    
    /* Thiết kế thẻ câu hỏi viền xanh nhạt, nền trắng tinh tế */
    .question-card {
        background-color: #FFFFFF !important;
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #E2EFE7 !important;
        margin-bottom: 20px;
    }
    
    /* Chân trang giáo viên */
    .footer {
        text-align: center;
        padding: 25px 0px;
        font-size: 18px;
        color: #000000 !important;
        font-weight: bold !important;
        border-top: 2px solid #E2EFE7;
        margin-top: 50px;
    }
</style>
""", unsafe_allow_html=True)

# --- WEBHOOK GOOGLE SHEETS (Tham khảo từ Ghi chú mới) ---
# Địa chỉ Webhook mới từ nguồn tham khảo của bạn
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbxfZ7f292zc7Rcq8OdalCQIKl9WDY1fAc21pBMAmXFKr1qnQ3F8FeH-vJqIebuWKQ1U8A/exec"

def send_results_to_gsheet(student_name, score_listening, score_reading, score_writing):
    payload = {
        "name": student_name,
        "lesson": "Bài 16: 生活可以更美好 (HSK4)",
        "score_listening": score_listening,
        "score_reading": score_reading,
        "score_writing": score_writing
    }
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        return response.status_code == 200
    except:
        return False

# --- GIAO DIỆN HEADER ---
st.markdown("<h1>📚 BÀI TẬP BÀI 16 (HSK4)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; color: #000000; font-weight: bold;'>Chúc các bạn làm bài vui!</p>", unsafe_allow_html=True)

# --- CẤU HÌNH LIÊN KẾT AUDIO GITHUB TỰ ĐỘNG ---
# Nhập link Github của giáo viên, hệ thống tự tách để lấy link Raw phát audio trực tiếp
github_link_input = st.text_input(
    "👉 Nhập link GitHub của bạn chứa thư mục audio (Ví dụ: https://github.com/hoangbaoyugiao-vien/hsk4-audio):",
    value="https://github.com/hoangbaoyugiao-vien/hsk4-audio"
)

# Tự động chuyển đổi sang link Raw của Github
if "github.com" in github_link_input:
    raw_base = github_link_input.replace("github.com", "raw.githubusercontent.com")
    # Nếu link có chứa "/blob/", loại bỏ nó để tạo link Raw chuẩn
    if "/blob/" in raw_base:
        raw_base = raw_base.replace("/blob/", "/")
    # Gắn nhánh mặc định main nếu không chỉ định rõ
    if not any(branch in raw_base for branch in ["/main", "/master"]):
        raw_base = raw_base + "/main"
    
    AUDIO_16_1 = f"{raw_base}/audio/16-1.mp3"
    AUDIO_16_2 = f"{raw_base}/audio/16-2.mp3"
    AUDIO_16_3 = f"{raw_base}/audio/16-3.mp3"
else:
    # Fallback mặc định
    AUDIO_16_1 = "https://raw.githubusercontent.com/username/repo/main/audio/16-1.mp3"
    AUDIO_16_2 = "https://raw.githubusercontent.com/username/repo/main/audio/16-2.mp3"
    AUDIO_16_3 = "https://raw.githubusercontent.com/username/repo/main/audio/16-3.mp3"

# --- NHẬP HỌ TÊN HỌC SINH ---
student_name = st.text_input(
    "👤 Nhập họ và tên học viên / 输入您的姓名:",
    placeholder="Nhập họ và tên của bạn tại đây..."
)

# --- QUẢN LÝ TRẠNG THÁI NỘP BÀI ---
if 'listening_submitted' not in st.session_state:
    st.session_state.listening_submitted = False
if 'reading_submitted' not in st.session_state:
    st.session_state.reading_submitted = False
if 'writing_submitted' not in st.session_state:
    st.session_state.writing_submitted = False

# --- PHÂN CHIA CÁC TABS BÀI TẬP ---
tab_listening, tab_reading, tab_writing = st.tabs(["🎧 PHẦN NGHE (听力)", "📖 PHẦN ĐỌC (阅读)", "✍️ PHẦN VIẾT (书写)"])

# ==========================================
# 1. TAB LISTENING (PHẦN NGHE)
# ==========================================
with tab_listening:
    st.markdown("## 一、听力 (Phần nghe)")
    
    # --- PART 1 ---
    st.markdown("### 第一部分 (Phần 1) - 判断对错")
    st.info("💡 Nghe audio và chọn Đúng (✔) hoặc Sai (✘)")
    st.audio(AUDIO_16_1, format="audio/mp3")
    
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
    st.audio(AUDIO_16_2, format="audio/mp3")
    
    q6_12_options = [
        ["A. 杂志", "B. 成绩单", "C. 报名表", "D. 传真"],
        ["A. 害怕失败", "B. 弹得不好", "C. 没有报名", "D. 没有时间"],
        ["A. 睡不着", "B. 还有工作", "C. 在等人", "D. 在看小说"],
        ["A. 来宾馆", "B. 填表格", "C. 说很满意", "D. 写总结"],
        ["A. 商店", "B. 学校", "C. 公司", "D. 饭馆"],
        ["A. 经历丰富", "B. 非常可怜", "C. 更会打扮", "D. 都很聪明"],
        ["A. 力气很大", "B. 爱看小说", "C. 现在 is 记者", "D. 去过很多地方"]
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
    st.audio(AUDIO_16_3, format="audio/mp3")
    
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

    # --- NỘP BÀI PHẦN NGHE ---
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 NỘP BÀI PHẦN NGHE", key="btn_sub_listening"):
        if not student_name.strip():
            st.error("⚠️ Vui lòng nhập họ và tên ở đầu trang trước khi nộp bài!")
        else:
            correct_cnt = 0
            # Chấm phần 1
            for i in range(5):
                user_val = "✔" if "✔" in user_q1_5[i] else "✘" if "✘" in user_q1_5[i] else "Chưa chọn"
                if user_val == q1_5_ans[i]:
                    correct_cnt += 1
            # Chấm phần 2
            for i in range(7):
                if user_q6_12[i] == q6_12_ans[i]:
                    correct_cnt += 1
            # Chấm phần 3
            for i in range(10):
                if user_q13_22[i] == q13_22_ans[i]:
                    correct_cnt += 1
            
            st.session_state.listening_submitted = True
            st.session_state.listening_score = f"{correct_cnt}/22"
            
            st.success("🎉 Chúc mừng bạn đã làm xong bài tập nha")
            st.info(f"📊 Điểm số của bạn là: {correct_cnt}/22.")
            
            # Đồng bộ kết quả
            send_results_to_gsheet(student_name, f"{correct_cnt}/22", "", "")

    # --- GIẢI THÍCH CHI TIẾT ---
    if st.session_state.listening_submitted:
        st.markdown("### 🔍 CHI TIẾT BÀI LÀM & ĐÁP ÁN:")
        
        st.markdown("#### **Phần 1:**")
        for i in range(5):
            user_val = "✔" if "✔" in user_q1_5[i] else "✘" if "✘" in user_q1_5[i] else "Chưa chọn"
            is_correct = user_val == q1_5_ans[i]
            status = "✅ Đúng" if is_correct else "❌ Sai"
            st.markdown(f"**Câu {i+1}:** Lựa chọn: `{user_val}` -> {status}")
            
            if not is_correct:
                with st.expander(f"📖 Lời thoại và Giải thích chi tiết Câu {i+1}"):
                    if i == 0:
                        st.markdown("""**Lời thoại:**
办签证需要准备哪些材料，我也不太清楚，不过我有大使馆的电话号码，我可以帮你问一下。
*(Tôi cũng không rõ cần chuẩn bị giấy tờ gì để làm visa, nhưng tôi có số điện thoại của Đại sứ quán, tôi có thể hỏi giúp bạn.)*

**Giải thích:**
Đề bài nhận định "Anh ấy biết cách làm visa" là sai. Đáp án đúng là ✘.""")
                    elif i == 1:
                        st.markdown("""**Lời thoại:**
只有通过了考试，完全符合要求后，护士才能正式开始工作。医院对护士这一职业的要求是：专业、负责、尊重生命。
*(Chỉ sau khi vượt qua kỳ thi và hoàn toàn đáp ứng yêu cầu, y tá mới có thể chính thức bắt đầu làm việc. Yêu cầu của bệnh viện đối với nghề y tá là: chuyên nghiệp, trách nhiệm và tôn trọng cuộc sống.)*

**Giải thích:**
Đề bài nhận định "Y tá phải thi trước khi làm việc" là đúng. Đáp án đúng là ✔.""")
                    elif i == 2:
                        st.markdown("""**Lời thoại:**
第一次跟女朋友见面的时候，他紧张极了，脸和耳朵都红了，几乎不敢看女朋友的眼睛。
*(Lần đầu gặp bạn gái, anh ấy vô cùng căng thẳng, mặt và tai đều đỏ bừng, hầu như không dám nhìn vào mắt cô ấy.)*

**Giải thích:**
Đề bài nhận định "Anh ấy rất thư giãn trong lần đầu gặp bạn gái" là sai. Đáp án đúng là ✘.""")
                    elif i == 3:
                        st.markdown("""**Lời thoại:**
这篇文章你还得拿回去好好改改，主要是内容有点儿乱，重点不够清楚，另外，有几个句子还有语法问题。
*(Bài viết này bạn phải mang về sửa lại thật kỹ, chủ yếu là nội dung hơi lộn xộn, trọng tâm chưa rõ ràng, ngoài ra còn vài câu bị lỗi ngữ pháp.)*

**Giải thích:**
Đề bài nhận định "Bài viết viết rất xuất sắc" là sai. Đáp án đúng là ✘.""")
                    elif i == 4:
                        st.markdown("""**Lời thoại:**
受到批评时，也别伤心失望，谁都有做错事或者做得不够好的时候。只要不放弃努力，你就仍然有希望。
*(Khi bị phê bình thì cũng đừng đau lòng thất vọng, ai cũng có lúc làm sai hoặc làm chưa đủ tốt. Chỉ cần không từ bỏ nỗ lực, bạn vẫn luôn có hy vọng.)*

**Giải thích:**
Đề bài nhận định "Lúc làm chưa tốt đừng thất vọng" là đúng. Đáp án đúng là ✔.""")


# ==========================================
# 2. TAB READING (PHẦN ĐỌC)
# ==========================================
with tab_reading:
    st.markdown("## 二、阅读 (Phần đọc)")
    
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
        "27. A：我那件红衬衫呢？你放哪儿了？\nB：洗了，在外边（ ）着，还没干呢。你穿这件就很好，很精神。",
        "28. A：去植物园玩儿的同事一共是十二位，现在还有人要（ ）吗？\nB：我也想去。明天我们大概去多长时间？几点能回来呢？",
        "29. A：外面雪下得这么大，那些小伙子们怎么都跑外边去了？\nB：他们都是南方人，南方冬天很少下雪，更不用说这么大的雪，所以他们肯定特别（ ）。",
        "30. A：现在城市里越来越多的人喜欢到（ ）过周末了。\nB：是啊，那里空气新鲜、环境安静，可以让人好好放松一下。"
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
        ans = st.text_input(f"Nhập thứ tự đúng câu {i+31} (Ví dụ: ABC):", key=f"read_p2_{i}").strip().upper()
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
        "**[40-41 题]**\n“我找林医生，我有急事！”一位妈妈非常着急地给林医生打电话，林医ens妻子接的电话。“他刚出去了，您有什么事吗？”“天哪，我的小儿子刚才把我的手表吃到肚子里了，林医生什么时候能回来？”“两个小时左右。”医生的妻子回答。“两个小时！这段时间我该怎么办呀？”“我很抱歉，您恐怕只能先用另一块儿手表了。”\n\n40. ★ 孩子怎么了？",
        "41. ★ 关于林医生，可以知道什么？",
        "**[42-43 题]**\n父母是孩子第一位老师，也是最重要的老师。父母不仅要帮助孩子认识世界，教会他们知识，还应该帮助孩子养成好的生活习惯，比如睡前刷牙、节约用水。另外，还要教会他们懂礼貌、对人诚实。这些都需要父母的耐心教育。孩子习惯的养成会受到父母的影响，所以做父母的平时一定要注意自己的言行。\n\n42. ★ 根据这段话，父母有什么责任？",
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
        ans = st.selectbox(f"Chọn đáp án câu {i+35}:", ["Chưa chọn"] + q35_43_options[i], key=f"read_p3_{i}")
        user_q35_43.append(ans[0] if ans != "Chưa chọn" else "Chưa chọn")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- NỘP BÀI PHẦN ĐỌC ---
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
            st.info(f"📊 Điểm số của bạn là: {correct_cnt}/21.")
            
            # Đồng bộ kết quả
            send_results_to_gsheet(student_name, "", f"{correct_cnt}/21", "")


# ==========================================
# 3. TAB WRITING (PHẦN VIẾT)
# ==========================================
with tab_writing:
    st.markdown("## 三、书写 (Phần viết)")
    
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
    st.markdown("### 第二部分 (Phần 2) - Nhìn tranh đặt câu")
    
    st.markdown("""
    <div class='question-card'>
        <strong>Câu 49:</strong> (Tranh chàng trai đang chơi bóng rổ)<br>
        Từ gợi ý: <strong>小伙子</strong>
    </div>
    """, unsafe_allow_html=True)
    user_q49 = st.text_area("Viết câu của bạn:", key="write_p2_49")
    
    st.markdown("""
    <div class='question-card'>
        <strong>Câu 50:</strong> (Tranh tay một người đang cầm bút viết điền vào bảng biểu)<br>
        Từ gợi ý: <strong>表格</strong>
    </div>
    """, unsafe_allow_html=True)
    user_q50 = st.text_area("Viết câu của bạn:", key="write_p2_50")

    # --- NỘP BÀI PHẦN VIẾT ---
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 NỘP BÀI PHẦN VIẾT", key="btn_sub_writing"):
        if not student_name.strip():
            st.error("⚠️ Vui lòng nhập họ và tên ở đầu trang trước khi nộp bài!")
        else:
            correct_cnt = 0
            for i in range(5):
                user_ans_clean = user_q44_48[i].replace(" ", "").strip()
                matched = False
                for possible_ans in q44_48_acceptable_ans[i]:
                    if user_ans_clean == possible_ans.replace(" ", "").strip():
                        matched = True
                        break
                if matched:
                    correct_cnt += 1
                    
            st.session_state.writing_submitted = True
            st.session_state.writing_score = f"{correct_cnt}/5"
            
            st.success("🎉 Chúc mừng bạn đã làm xong bài tập nha")
            st.info(f"📊 Điểm số của bạn là: {correct_cnt}/5 (Chỉ tính điểm tự động phần Sắp xếp câu).")
            
            # Đồng bộ kết quả
            send_results_to_gsheet(student_name, "", "", f"{correct_cnt}/5")

    # --- ĐÁP ÁN GỢI Ý PHẦN VIẾT ---
    if st.session_state.writing_submitted:
        st.markdown("### 🔍 CHI TIẾT BÀI LÀM & ĐÁP ÁN ĐÚNG:")
        for i in range(5):
            user_ans_clean = user_q44_48[i].replace(" ", "").strip()
            matched = False
            for possible_ans in q44_48_acceptable_ans[i]:
                if user_ans_clean == possible_ans.replace(" ", "").strip():
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
