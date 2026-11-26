import streamlit as st

st.set_page_config(
    page_title="منصة المعلم الذكي | المناهج السعودية",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- تنسيق الواجهة العربية الحديثة وإخفاء زوائد Streamlit ---
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'IBM Plex Sans Arabic', sans-serif;
            direction: RTL;
            text-align: right;
        }

        #MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stDecoration"] {
            visibility: hidden;
            display: none;
        }

        .stApp {
            background: linear-gradient(180deg, #f3f6fb 0%, #eef2f7 100%);
        }

        .top-hero {
            background: linear-gradient(135deg, #0f3d3e 0%, #165b5d 55%, #1f7a7c 100%);
            color: #ffffff;
            padding: 24px 28px;
            border-radius: 20px;
            box-shadow: 0 12px 30px rgba(15, 61, 62, 0.16);
            margin-bottom: 20px;
        }

        .top-hero h1 {
            color: #ffffff;
            font-size: 1.65rem;
            font-weight: 700;
            margin: 0 0 6px 0;
        }

        .top-hero p {
            color: #d9f0f0;
            margin: 0;
            font-size: 0.98rem;
        }

        .badge-pill {
            display: inline-block;
            background: rgba(255, 255, 255, 0.16);
            border: 1px solid rgba(255, 255, 255, 0.25);
            color: #ffffff;
            padding: 5px 12px;
            border-radius: 999px;
            font-size: 0.82rem;
            font-weight: 600;
            margin-left: 8px;
            margin-top: 10px;
        }

        .panel-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 18px;
            padding: 20px;
            box-shadow: 0 6px 20px rgba(15, 23, 42, 0.04);
            margin-bottom: 16px;
        }

        .slide-stage {
            background: linear-gradient(160deg, #ffffff 0%, #f8fafc 100%);
            border: 2px solid #cbd5e1;
            border-radius: 22px;
            padding: 28px;
            min-height: 330px;
            box-shadow: 0 14px 32px rgba(15, 23, 42, 0.08);
            position: relative;
        }

        .slide-stage.fullscreen-mode {
            min-height: 520px;
            border-color: #165b5d;
            border-width: 2.5px;
        }

        .slide-header-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 12px;
            margin-bottom: 18px;
            gap: 10px;
            flex-wrap: wrap;
        }

        .slide-tag {
            background: #e6f4f1;
            color: #0f3d3e;
            font-weight: 700;
            font-size: 0.85rem;
            padding: 6px 14px;
            border-radius: 999px;
        }

        .slide-counter {
            background: #f1f5f9;
            color: #334155;
            font-weight: 600;
            font-size: 0.85rem;
            padding: 6px 12px;
            border-radius: 999px;
        }

        .slide-title {
            font-size: 1.35rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 14px;
        }

        .slide-body {
            font-size: 1.05rem;
            line-height: 1.85;
            color: #1e293b;
        }

        .highlight-box {
            background: #f0fdf4;
            border-right: 4px solid #15803d;
            padding: 12px 16px;
            border-radius: 10px;
            margin-top: 14px;
            color: #14532d;
            font-weight: 500;
        }

        .game-box {
            background: #fffbeb;
            border-right: 4px solid #d97706;
            padding: 14px 16px;
            border-radius: 10px;
            margin-top: 14px;
            color: #78350f;
        }

        div.stButton > button {
            border-radius: 12px;
            font-weight: 600;
            padding: 0.55rem 1rem;
            border: 1px solid #cbd5e1;
        }

        div.stButton > button[kind="primary"] {
            background: #165b5d;
            border-color: #165b5d;
            color: #ffffff;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- قاعدة بيانات شاملة لجميع المراحل والصفوف والمواد في المناهج السعودية ---
CURRICULUM = {
    "المرحلة الابتدائية": {
        "الأول الابتدائي": [
            "لغتي",
            "الرياضيات",
            "العلوم",
            "الدراسات الإسلامية",
            "التربية الفنية",
            "التربية البدنية والدفاع عن النفس",
            "الحياة الأسرية",
        ],
        "الثاني الابتدائي": [
            "لغتي",
            "الرياضيات",
            "العلوم",
            "الدراسات الإسلامية",
            "التربية الفنية",
            "التربية البدنية والدفاع عن النفس",
            "الحياة الأسرية",
        ],
        "الثالث الابتدائي": [
            "لغتي",
            "الرياضيات",
            "العلوم",
            "الدراسات الإسلامية",
            "التربية الفنية",
            "التربية البدنية والدفاع عن النفس",
            "الحياة الأسرية",
        ],
        "الرابع الابتدائي": [
            "لغتي",
            "الرياضيات",
            "العلوم",
            "الدراسات الإسلامية",
            "الدراسات الاجتماعية",
            "المهارات الرقمية",
            "التربية الفنية",
            "التربية البدنية والدفاع عن النفس",
            "المهارات الحياتية والأسرية",
        ],
        "الخامس الابتدائي": [
            "لغتي",
            "الرياضيات",
            "العلوم",
            "الدراسات الإسلامية",
            "الدراسات الاجتماعية",
            "المهارات الرقمية",
            "التربية الفنية",
            "التربية البدنية والدفاع عن النفس",
            "المهارات الحياتية والأسرية",
        ],
        "السادس الابتدائي": [
            "لغتي",
            "الرياضيات",
            "العلوم",
            "الدراسات الإسلامية",
            "الدراسات الاجتماعية",
            "المهارات الرقمية",
            "التربية الفنية",
            "التربية البدنية والدفاع عن النفس",
            "المهارات الحياتية والأسرية",
        ],
    },
    "المرحلة المتوسطة": {
        "الأول المتوسط": [
            "لغتي الخالدة",
            "الرياضيات",
            "العلوم",
            "الدراسات الإسلامية",
            "الدراسات الاجتماعية",
            "المهارات الرقمية",
            "التربية الفنية",
            "التربية البدنية والدفاع عن النفس",
            "المهارات الحياتية والأسرية",
        ],
        "الثاني المتوسط": [
            "لغتي الخالدة",
            "الرياضيات",
            "العلوم",
            "الدراسات الإسلامية",
            "الدراسات الاجتماعية",
            "المهارات الرقمية",
            "التربية الفنية",
            "التربية البدنية والدفاع عن النفس",
            "المهارات الحياتية والأسرية",
        ],
        "الثالث المتوسط": [
            "لغتي الخالدة",
            "الرياضيات",
            "العلوم",
            "الدراسات الإسلامية",
            "الدراسات الاجتماعية",
            "المهارات الرقمية",
            "التربية الفنية",
            "التربية البدنية والدفاع عن النفس",
            "المهارات الحياتية والأسرية",
        ],
    },
    "المرحلة الثانوية": {
        "الأول الثانوي (السنة المشتركة)": [
            "اللغة العربية (الكفايات اللغوية)",
            "الرياضيات",
            "الأحياء",
            "الكيمياء",
            "الفيزياء",
            "القرآن الكريم والدراسات الإسلامية",
            "الدراسات الاجتماعية",
            "التقنية الرقمية",
            "التربية الصحية والبدنية",
            "التفكير الناقد",
            "اللياقة والثقافة الصحية",
        ],
        "الثاني الثانوي": [
            "الرياضيات",
            "الأحياء",
            "الكيمياء",
            "الفيزياء",
            "اللغة العربية",
            "القرآن الكريم والدراسات الإسلامية",
            "الدراسات الاجتماعية",
            "التقنية الرقمية",
            "العلوم الإدارية والمالية",
            "التربية الصحية والبدنية",
        ],
        "الثالث الثانوي": [
            "الرياضيات",
            "الأحياء",
            "الكيمياء",
            "الفيزياء",
            "اللغة العربية",
            "القرآن الكريم والدراسات الإسلامية",
            "الدراسات الاجتماعية",
            "التقنية الرقمية",
            "العلوم الإدارية والمالية",
            "التربية الصحية والبدنية",
        ],
    },
}

STRATEGIES = [
    "التعلم التعاوني",
    "العصف الذهني",
    "الاستقصاء الموجّه",
    "فكر - زاوج - شارك",
    "التعلم باللعب",
    "الخرائط الذهنية",
]

# --- تهيئة حالة الجلسة ---
if "subscribed" not in st.session_state:
    st.session_state.subscribed = True
if "plan_name" not in st.session_state:
    st.session_state.plan_name = "الباقة الشهرية للمعلمين (نشطة)"
if "slide_idx" not in st.session_state:
    st.session_state.slide_idx = 0
if "fullscreen_slide" not in st.session_state:
    st.session_state.fullscreen_slide = False
if "deck" not in st.session_state:
    st.session_state.deck = None


def build_slides(stage, grade, subject, unit_title, p_start, p_end, strategy, notes):
    page_span = f"من صفحة {p_start} إلى صفحة {p_end}"
    lesson_label = unit_title.strip() if unit_title.strip() else f"وحدة {subject} ({page_span})"
    extra_note = notes.strip() if notes.strip() else "ربط المفاهيم بالواقع اليومي للطالب داخل الصف."

    return [
        {
            "tag": "الشريحة 1 • التمهيد والأهداف",
            "title": f"{subject} — {lesson_label}",
            "body": (
                f"<b>المرحلة والصف:</b> {stage} / {grade}<br>"
                f"<b>نطاق الكتاب المحدد:</b> {page_span}<br>"
                f"<b>استراتيجية التدريس:</b> {strategy}<br><br>"
                f"<b>هدف الحصة:</b> تمكين الطلاب من استيعاب المفاهيم الأساسية للنطاق المحدد وتطبيقها بثقة داخل الصف."
            ),
            "box": f"<b>ملاحظة المعلم:</b> {extra_note}",
            "box_type": "highlight",
        },
        {
            "tag": "الشريحة 2 • الشرح والمفاهيم الأساسية",
            "title": f"المفاهيم المحورية في ({lesson_label})",
            "body": (
                f"نستعرض في هذا الجزء العناصر الرئيسية الواردة في {page_span} من مقرر <b>{subject}</b> بلغة مبسطة ومتدرجة تناسب مستوى طلاب <b>{grade}</b>:<br>"
                f"• تعريف الفكرة المركزية وتحديد عناصرها الأساسية.<br>"
                f"• الربط بين المصطلحات والمواقف اليومية المألوفة للطالب.<br>"
                f"• التنبيه على الأخطاء الشائعة والتحقق من الفهم خطوة بخطوة."
            ),
            "box": f"<b>تطبيق استراتيجية ({strategy}):</b> قسّم الصف إلى مجموعات قصيرة، واطلب من كل مجموعة استخراج فكرة واحدة من {page_span}.",
            "box_type": "highlight",
        },
        {
            "tag": "الشريحة 3 • أمثلة وتطبيقات عملية",
            "title": "أمثلة صفية ونماذج محلولة",
            "body": (
                f"<b>مثال (1):</b> نموذج تطبيقي مباشر مستمد من موضوعات {page_span} في مادة <b>{subject}</b> مع توضيح خطوات الحل بوضوح.<br>"
                f"<b>مثال (2):</b> تطبيق واقعي مرتبط بحياة الطالب اليومية في المملكة لترسيخ الفكرة ومنع الحفظ المجرد."
            ),
            "box": "<b>سؤال للمناقشة السريعة:</b> كيف يمكنك تطبيق هذه الفكرة في موقف يمر بك يومياً؟",
            "box_type": "highlight",
        },
        {
            "tag": "الشريحة 4 • لعبة ونشاط تفاعلي",
            "title": f"نشاط تفاعلي بأسلوب: {strategy}",
            "body": (
                "<b>لعبة «تحدي البطاقات السريعة»:</b><br>"
                "1. يطرح المعلم سؤالاً مرتبطاً بالصفحات المحددة لمدة 30 ثانية.<br>"
                "2. ترفع المجموعات إجاباتها أو تجيب شفهياً دون الاعتماد على الكتاب المفتوح.<br>"
                "3. تُمنح نقطة لكل إجابة دقيقة مع ذكر السبب."
            ),
            "box": "<b>نشاط إضافي:</b> اطلب من طالب صياغة سؤال واحد لزملائه من محتوى الدرس.",
            "box_type": "game",
        },
        {
            "tag": "الشريحة 5 • الخلاصة والتقويم الختامي",
            "title": "ملخص الدرس وتقويم ختامي سريع",
            "body": (
                f"• راجعنا أهم مفاهيم <b>{lesson_label}</b> ({page_span}).<br>"
                f"• طبقنا أمثلة متنوعة ونشاطاً تفاعلياً وفق استراتيجية <b>{strategy}</b>.<br>"
                f"• <b>تقويم ختامي:</b> سؤالان قصيران للتحقق من تحقق هدف الحصة قبل نهاية الوقت."
            ),
            "box": "<b>تنبيه العرض:</b> العرض يعمل مباشرة داخل المنصة لتسهيل الشرح داخل الفصل دون الحاجة لتحميل ملفات.",
            "box_type": "highlight",
        },
    ]


# --- الشريط العلوي للواجهة الجديدة ---
st.markdown(
    """
    <div class="top-hero">
        <h1>🎓 منصة المعلم الذكي — عارض الدروس والشرائح التفاعلية</h1>
        <p>جميع المراحل من أول ابتدائي إلى ثالث ثانوي • عرض شرائح مباشر داخل التطبيق • أزرار تنقل سهلة</p>
        <span class="badge-pill">الابتدائية • المتوسطة • الثانوية</span>
        <span class="badge-pill">عرض شرائح داخلي</span>
        <span class="badge-pill">إدارة الاشتراكات</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- شريط الحالة والاشتراك السريع ---
col_s1, col_s2, col_s3 = st.columns([2, 1, 1])
with col_s1:
    if st.session_state.subscribed:
        st.success(f"حالة الاشتراك: {st.session_state.plan_name}")
    else:
        st.warning("حالة الاشتراك: متوقف — فعّل الاشتراك من تبويب (الاشتراك والباقات)")
with col_s2:
    if st.button("تبديل عرض الشريحة (عادي / مكبّر)", use_container_width=True):
        st.session_state.fullscreen_slide = not st.session_state.fullscreen_slide
        st.rerun()
with col_s3:
    if st.button("إعادة ضبط الشرائح", use_container_width=True):
        st.session_state.slide_idx = 0
        st.rerun()

tab_lesson, tab_sub = st.tabs(["📊 إعداد الدرس وعرض الشرائح", "💳 الاشتراك والباقات"])

with tab_lesson:
    left_col, right_col = st.columns([1.05, 1.45], gap="large")

    with left_col:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.subheader("1️⃣ اختيار المنهج والدرس")

        stage = st.selectbox("المرحلة الدراسية", list(CURRICULUM.keys()))
        grades_list = list(CURRICULUM[stage].keys())
        grade = st.selectbox("الصف الدراسي", grades_list)

        subjects_list = CURRICULUM[stage][grade]
        subject = st.selectbox("المادة الدراسية", subjects_list)

        unit_title = st.text_input(
            "اسم الوحدة أو الدرس",
            placeholder="مثال: الجملة الاسمية / الكسور / البناء الضوئي...",
        )

        p1, p2 = st.columns(2)
        with p1:
            p_start = st.number_input("من صفحة", min_value=1, max_value=400, value=12)
        with p2:
            p_end = st.number_input("إلى صفحة", min_value=1, max_value=400, value=18)

        strategy = st.selectbox("استراتيجية التدريس", STRATEGIES)
        notes = st.text_area(
            "تخصيص إضافي (اختياري)",
            placeholder="اكتب أي توجيه خاص بالصف أو الأنشطة...",
            height=75,
        )

        generate_clicked = st.button(
            "✨ إنشاء الشرائح وعرضها الآن",
            type="primary",
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        if generate_clicked:
            if not st.session_state.subscribed:
                st.error("يرجى تفعيل الاشتراك أولاً من تبويب (الاشتراك والباقات).")
            elif p_end < p_start:
                st.error("رقم صفحة النهاية يجب أن يكون أكبر من أو يساوي صفحة البداية.")
            else:
                st.session_state.deck = build_slides(
                    stage=stage,
                    grade=grade,
                    subject=subject,
                    unit_title=unit_title,
                    p_start=int(p_start),
                    p_end=int(p_end),
                    strategy=strategy,
                    notes=notes,
                )
                st.session_state.slide_idx = 0
                st.rerun()

    with right_col:
        st.subheader("2️⃣ عارض الشرائح الداخلي")

        if st.session_state.deck is None:
            st.session_state.deck = build_slides(
                stage="المرحلة الابتدائية",
                grade="الأول الابتدائي",
                subject="لغتي",
                unit_title="الدرس التمهيدي",
                p_start=1,
                p_end=6,
                strategy=STRATEGIES[0],
                notes="",
            )

        slides = st.session_state.deck
        total_slides = len(slides)
        idx = max(0, min(st.session_state.slide_idx, total_slides - 1))
        st.session_state.slide_idx = idx
        current_slide = slides[idx]

        # أزرار التنقل بين الشرائح
        nav_prev, nav_info, nav_next = st.columns([1, 1.4, 1])
        with nav_prev:
            if st.button("⬅️ الشريحة السابقة", use_container_width=True, disabled=(idx == 0)):
                st.session_state.slide_idx = idx - 1
                st.rerun()
        with nav_info:
            st.markdown(
                f"<div style='text-align:center; padding-top:8px; font-weight:700; color:#0f3d3e;'>شريحة {idx + 1} من {total_slides}</div>",
                unsafe_allow_html=True,
            )
        with nav_next:
            if st.button(
                "الشريحة التالية ➡️",
                use_container_width=True,
                disabled=(idx == total_slides - 1),
            ):
                st.session_state.slide_idx = idx + 1
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # عرض الشريحة الحالية داخل إطار داخلي مباشر
        stage_class = "slide-stage fullscreen-mode" if st.session_state.fullscreen_slide else "slide-stage"
        box_class = "game-box" if current_slide["box_type"] == "game" else "highlight-box"

        slide_html = f"""
        <div class="{stage_class}">
            <div class="slide-header-row">
                <span class="slide-tag">{current_slide["tag"]}</span>
                <span class="slide-counter">{idx + 1} / {total_slides}</span>
            </div>
            <div class="slide-title">{current_slide["title"]}</div>
            <div class="slide-body">{current_slide["body"]}</div>
            <div class="{box_class}">{current_slide["box"]}</div>
        </div>
        """
        st.markdown(slide_html, unsafe_allow_html=True)

        # شريط أرقام الشرائح للانتقال السريع
        st.markdown("<br>", unsafe_allow_html=True)
        quick_cols = st.columns(total_slides)
        for i, q_col in enumerate(quick_cols):
            with q_col:
                label = f"• {i + 1} •" if i == idx else f"{i + 1}"
                if st.button(label, key=f"jump_slide_{i}", use_container_width=True):
                    st.session_state.slide_idx = i
                    st.rerun()

with tab_sub:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.subheader("إدارة الاشتراك الشهري")
    st.write("تحكم في حالة اشتراك المعلم للوصول إلى جميع المراحل والمواد وعارض الشرائح الداخلي.")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### الباقة الشهرية للمعلم")
        st.write("• جميع المراحل (ابتدائي، متوسط، ثانوي)")
        st.write("• جميع المواد الدراسية المقررة")
        st.write("• عارض شرائح داخلي بأزرار تنقل")
        if st.button("تفعيل الباقة الشهرية", type="primary", use_container_width=True):
            st.session_state.subscribed = True
            st.session_state.plan_name = "الباقة الشهرية للمعلمين (نشطة)"
            st.rerun()

    with c2:
        st.markdown("### الباقة الفصلية المميزة")
        st.write("• أولوية الوصول للمزايا الجديدة")
        st.write("• تخصيص إضافي للأنشطة والاستراتيجيات")
        st.write("• عرض مباشر داخل التطبيق دون تنزيل")
        if st.button("تفعيل الباقة الفصلية", use_container_width=True):
            st.session_state.subscribed = True
            st.session_state.plan_name = "الباقة الفصلية المميزة (نشطة)"
            st.rerun()

    st.divider()
    if st.session_state.subscribed:
        if st.button("إيقاف الاشتراك مؤقتاً للاختبار"):
            st.session_state.subscribed = False
            st.session_state.plan_name = "غير مفعل"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
