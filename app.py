import streamlit as st
import streamlit.components.v1 as components
import json
import io
import os
import re
import html

from openai import OpenAI
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib import colors


# ==========================================
# إعدادات التطبيق
# ==========================================

st.set_page_config(
    page_title="مُعين | MUEEN",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Cairo', sans-serif;
    direction: rtl;
    text-align: right;
}

.stApp {
    background: #f7f9fc;
}

.main-title {
    background: linear-gradient(120deg, #102e46, #176b75);
    padding: 35px;
    border-radius: 22px;
    color: white;
    text-align: center;
    margin-bottom: 25px;
}

.main-title h1 {
    font-size: 45px;
    font-weight: 800;
}

.main-title p {
    font-size: 18px;
}

.stButton button {
    border-radius: 12px;
    font-weight: bold;
}

div[data-testid="stMetric"] {
    background: white;
    padding: 15px;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# وظائف الذكاء الاصطناعي
# ==========================================

def demo_lesson(data):

    topic = data["topic"]
    subject = data["subject"]

    return {
        "title": topic,

        "objectives": [
            f"أن يشرح الطالب مفهوم {topic}.",
            f"أن يطبق الطالب {topic} في مثال.",
            "أن يشارك في النشاط ويبرر إجابته."
        ],

        "slides": [
            {
                "title": f"مرحبًا بكم في درس {topic}",
                "body": f"المادة: {subject}\nالصف: {data['grade']}\n\nهيا نتعلم معًا!"
            },
            {
                "title": "تهيئة الدرس",
                "body": f"ماذا تعرف عن {topic}؟\nأين يمكن أن نلاحظ هذا المفهوم في حياتنا؟"
            },
            {
                "title": "أهداف الدرس",
                "body": "\n".join(data_objectives(data))
            },
            {
                "title": "شرح المفهوم",
                "body": f"تعرف على {topic} من خلال شرح مبسط وأمثلة مناسبة لمستواك الدراسي."
            },
            {
                "title": "مثال تطبيقي",
                "body": "اقرأ المثال جيدًا.\nحدد المعلومات المهمة.\nفكر في طريقة الحل.\nتحقق من إجابتك."
            },
            {
                "title": "نشاط تعليمي",
                "body": f"نفذ نشاطًا باستخدام استراتيجية {data['strategy']}."
            },
            {
                "title": "ناقش مع زملائك",
                "body": f"كيف يمكن استخدام {topic} في الحياة اليومية؟"
            },
            {
                "title": "تقويم التعلم",
                "body": "ما أهم فكرة تعلمتها اليوم؟\nما السؤال الذي لا يزال لديك؟"
            },
            {
                "title": "ملخص الدرس",
                "body": f"تعلمنا اليوم عن {topic} وطبقنا المفهوم في أمثلة وأنشطة."
            }
        ],

        "worksheet": [
            {
                "question": f"اشرح معنى {topic} بأسلوبك.",
                "options": [],
                "answer": "إجابة الطالب وفق المفهوم الصحيح."
            },
            {
                "question": f"اذكر مثالًا على {topic}.",
                "options": [],
                "answer": "مثال صحيح مرتبط بالدرس."
            },
            {
                "question": f"أي عبارة تصف {topic} بشكل أفضل؟",
                "options": [
                    "فهم المفهوم وتطبيقه",
                    "حفظ العنوان فقط",
                    "تجاهل الأمثلة"
                ],
                "answer": "فهم المفهوم وتطبيقه"
            }
        ],

        "game": [
            {
                "question": f"ما موضوع درسنا اليوم؟",
                "options": [
                    topic,
                    "موضوع آخر",
                    "لا شيء مما سبق"
                ],
                "correct": 0
            },
            {
                "question": "ما أفضل طريقة للتعلم؟",
                "options": [
                    "الفهم والتطبيق",
                    "الحفظ دون فهم",
                    "عدم المشاركة"
                ],
                "correct": 0
            },
            {
                "question": "ماذا نفعل بعد حل السؤال؟",
                "options": [
                    "نتحقق من الإجابة",
                    "نتجاهل الحل",
                    "نترك السؤال"
                ],
                "correct": 0
            }
        ],

        "teacher_guide": (
            f"ابدأ بتهيئة الطلاب لموضوع {topic}، "
            "ثم اشرح المفهوم باستخدام أمثلة مناسبة. "
            f"استخدم استراتيجية {data['strategy']}، "
            "واختم بتقويم قصير."
        )
    }


def data_objectives(data):
    return [
        f"• أن يشرح الطالب مفهوم {data['topic']}.",
        "• أن يطبق المفهوم في مثال.",
        "• أن يشارك في النشاط التعليمي."
    ]


def extract_json(text):

    text = text.strip()
    text = re.sub(r"^```(?:json)?", "", text)
    text = re.sub(r"```$", "", text)

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("تعذر قراءة نتيجة الذكاء الاصطناعي.")

    return json.loads(text[start:end + 1])


def generate_lesson(data, api_key, model):

    if not api_key:
        return demo_lesson(data)

    client = OpenAI(api_key=api_key)

    prompt = f"""
أنت خبير في تصميم المناهج والتعلم والتعليم.

أنشئ حزمة تعليمية باللغة العربية.

بيانات الدرس:
{json.dumps(data, ensure_ascii=False)}

المطلوب:
1. أهداف تعليمية قابلة للقياس.
2. تسع شرائح عرض.
3. ورقة عمل من خمسة أسئلة.
4. لعبة تعليمية من خمسة أسئلة.
5. دليل مختصر للمعلم.

يجب أن تكون المخرجات مترابطة وتخدم أهداف الدرس نفسها.

الاستراتيجية التعليمية:
{data['strategy']}

مدة الحصة:
{data['duration']} دقيقة.

اجعل اللغة مناسبة للمرحلة والصف.

لا تخترع أرقام صفحات من الكتب المدرسية.
لا تدّعِ مطابقة المحتوى للمنهج الرسمي دون مصدر موثوق.
إذا كانت هناك معلومة تحتاج إلى تحقق، وضح ذلك.

أعد النتيجة بصيغة JSON فقط بهذا الشكل:

{{
 "title": "عنوان الدرس",
 "objectives": ["هدف 1", "هدف 2"],
 "slides": [
  {{"title": "عنوان الشريحة", "body": "محتوى الشريحة"}}
 ],
 "worksheet": [
  {{
   "question": "السؤال",
   "options": ["خيار 1", "خيار 2", "خيار 3"],
   "answer": "الإجابة"
  }}
 ],
 "game": [
  {{
   "question": "السؤال",
   "options": ["خيار 1", "خيار 2", "خيار 3"],
   "correct": 0
  }}
 ],
 "teacher_guide": "دليل المعلم"
}}
"""

    response = client.responses.create(
        model=model,
        input=prompt
    )

    result = extract_json(response.output_text)

    required = [
        "title",
        "slides",
        "worksheet",
        "game",
        "teacher_guide"
    ]

    for key in required:
        if key not in result:
            raise ValueError(f"النتيجة ناقصة: {key}")

    return result


# ==========================================
# إنشاء PowerPoint
# ==========================================

def create_powerpoint(lesson, data):

    prs = Presentation()

    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    navy = RGBColor(16, 46, 70)
    teal = RGBColor(23, 107, 117)
    white = RGBColor(255, 255, 255)

    all_slides = [
        {
            "title": lesson["title"],
            "body": (
                f"{data['subject']} | {data['grade']}\n"
                "منصة مُعين التعليمية"
            )
        }
    ] + lesson["slides"]

    for item in all_slides:

        slide = prs.slides.add_slide(
            prs.slide_layouts[6]
        )

        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = navy

        bar = slide.shapes.add_shape(
            1,
            0,
            0,
            prs.slide_width,
            Inches(0.18)
        )

        bar.fill.solid()
        bar.fill.fore_color.rgb = teal
        bar.line.fill.background()

        title = slide.shapes.add_textbox(
            Inches(0.7),
            Inches(0.6),
            Inches(12),
            Inches(1.1)
        )

        p = title.text_frame.paragraphs[0]
        p.text = str(item.get("title", ""))
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = "Arial"
        p.font.size = Pt(30)
        p.font.bold = True
        p.font.color.rgb = white

        body = slide.shapes.add_textbox(
            Inches(0.8),
            Inches(2),
            Inches(11.8),
            Inches(4.7)
        )

        frame = body.text_frame
        frame.word_wrap = True

        for i, line in enumerate(
            str(item.get("body", "")).split("\n")
        ):

            p = (
                frame.paragraphs[0]
                if i == 0
                else frame.add_paragraph()
            )

            p.text = line
            p.alignment = PP_ALIGN.RIGHT
            p.font.name = "Arial"
            p.font.size = Pt(21)
            p.font.color.rgb = white

    output = io.BytesIO()
    prs.save(output)

    return output.getvalue()


# ==========================================
# إنشاء PDF
# ==========================================

def create_pdf(lesson, data):

    output = io.BytesIO()

    doc = SimpleDocTemplate(
        output,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ArabicTitle",
        parent=styles["Title"],
        fontSize=18,
        leading=25,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#163954")
    )

    body_style = ParagraphStyle(
        "ArabicBody",
        parent=styles["BodyText"],
        fontSize=12,
        leading=21,
        alignment=TA_RIGHT
    )

    story = []

    story.append(
        Paragraph(
            html.escape("ورقة عمل: " + lesson["title"]),
            title_style
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            html.escape(
                data["subject"] + " - " + data["grade"]
            ),
            body_style
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "اسم الطالب: ........................................",
            body_style
        )
    )

    story.append(Spacer(1, 20))

    for i, q in enumerate(lesson["worksheet"], 1):

        story.append(
            Paragraph(
                html.escape(
                    f"{i}. {q.get('question', '')}"
                ),
                body_style
            )
        )

        for option in q.get("options", []):

            story.append(
                Paragraph(
                    html.escape("□ " + option),
                    body_style
                )
            )

        story.append(Spacer(1, 30))

    doc.build(story)

    return output.getvalue()


# ==========================================
# اللعبة التفاعلية
# ==========================================

def create_game(lesson):

    questions = json.dumps(
        lesson["game"],
        ensure_ascii=False
    ).replace("</", "<\\/")

    return f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">

<style>
body {{
    font-family: Arial;
    background: #f1f6f7;
    padding: 20px;
}}

.box {{
    background: white;
    max-width: 700px;
    margin: auto;
    padding: 25px;
    border-radius: 20px;
}}

button {{
    display: block;
    width: 100%;
    padding: 15px;
    margin: 10px 0;
    border-radius: 12px;
    border: 1px solid #ddd;
    background: white;
    font-size: 17px;
    cursor: pointer;
}}

button:hover {{
    background: #e5f4f2;
}}

#next {{
    background: #176b75;
    color: white;
}}

</style>
</head>

<body>

<div class="box">

<h2>🎮 تحدي مُعين</h2>

<p id="number"></p>

<h3 id="question"></h3>

<div id="answers"></div>

<p id="feedback"></p>

<button id="next" style="display:none">
السؤال التالي
</button>

<h3 id="result"></h3>

</div>

<script>

const questions = {questions};

let index = 0;
let score = 0;
let answered = false;

function showQuestion() {{

    answered = false;

    document.getElementById("feedback").innerText = "";
    document.getElementById("next").style.display = "none";

    if (index >= questions.length) {{
        finish();
        return;
    }}

    let q = questions[index];

    document.getElementById("number").innerText =
        "السؤال " + (index + 1) + " من " + questions.length;

    document.getElementById("question").innerText =
        q.question;

    let area = document.getElementById("answers");

    area.innerHTML = "";

    q.options.forEach((option, i) => {{

        let btn = document.createElement("button");

        btn.innerText = option;

        btn.onclick = () => checkAnswer(i);

        area.appendChild(btn);

    }});

}}

function checkAnswer(choice) {{

    if (answered) return;

    answered = true;

    let q = questions[index];

    let correct = Number(q.correct) === choice;

    if (correct) {{
        score++;
    }}

    document.getElementById("feedback").innerText =
        correct ? "إجابة صحيحة! أحسنت 🌟" : "ليست الإجابة الصحيحة، حاول في السؤال القادم.";

    document.getElementById("next").style.display = "block";

    document.getElementById("next").innerText =
        index === questions.length - 1
        ? "عرض النتيجة"
        : "السؤال التالي";

    document.querySelectorAll("#answers button").forEach(
        btn => btn.disabled = true
    );

}}

function finish() {{

    document.getElementById("question").innerText =
        "انتهت اللعبة!";

    document.getElementById("answers").innerHTML = "";

    document.getElementById("feedback").innerText = "";

    document.getElementById("next").style.display = "none";

    document.getElementById("result").innerText =
        "نتيجتك: " + score + " من " + questions.length;

}}

document.getElementById("next").onclick = () => {{
    index++;
    showQuestion();
}};

showQuestion();

</script>

</body>
</html>
"""


# ==========================================
# واجهة مُعين
# ==========================================

st.markdown("""
<div class="main-title">
<h1>مُعين | MUEEN 🎓</h1>
<p>درس واحد. كل أدواته. في دقائق.</p>
<p>منصة ذكية لمساعدة المعلمين والمعلمات</p>
</div>
""", unsafe_allow_html=True)


with st.sidebar:

    st.header("إعدادات الذكاء الاصطناعي")

    api_key = st.text_input(
        "مفتاح OpenAI API",
        type="password"
    )

    model = st.text_input(
        "اسم النموذج",
        value="gpt-4.1-mini"
    )

    st.divider()

    st.caption("MUEEN — منصة إعداد الدروس")


st.header("إنشاء حزمة تعليمية")

col1, col2 = st.columns(2)

with col1:

    stage = st.selectbox(
        "المرحلة الدراسية",
        ["الابتدائية", "المتوسطة", "الثانوية"]
    )

    grade = st.selectbox(
        "الصف الدراسي",
        [
            "الأول",
            "الثاني",
            "الثالث",
            "الرابع",
            "الخامس",
            "السادس",
            "الأول المتوسط",
            "الثاني المتوسط",
            "الثالث المتوسط",
            "الأول الثانوي",
            "الثاني الثانوي",
            "الثالث الثانوي"
        ]
    )

    subject = st.selectbox(
        "المادة",
        [
            "الرياضيات",
            "العلوم",
            "لغتي",
            "اللغة الإنجليزية",
            "الدراسات الإسلامية",
            "الدراسات الاجتماعية",
            "الفيزياء",
            "الكيمياء",
            "الأحياء",
            "الحاسب"
        ]
    )

with col2:

    strategy = st.selectbox(
        "الاستراتيجية التعليمية",
        [
            "التعلم باللعب",
            "التعلم التعاوني",
            "حل المشكلات",
            "العصف الذهني",
            "التعلم بالاكتشاف",
            "التعلم بالمشاريع",
            "التعلم المقلوب",
            "التعلم بالاستقصاء",
            "التعلم النشط",
            "اختيار تلقائي من مُعين"
        ]
    )

    duration = st.selectbox(
        "مدة الحصة",
        [30, 45, 60]
    )

    difficulty = st.selectbox(
        "مستوى الصعوبة",
        ["مبسط", "متوسط", "متقدم"]
    )

topic = st.text_input(
    "عنوان الدرس",
    placeholder="مثال: الكسور الاعتيادية"
)

notes = st.text_area(
    "ملاحظات إضافية",
    placeholder="اكتبي أي تفاصيل تريدين إضافتها للدرس."
)

design = st.selectbox(
    "نمط التصميم",
    [
        "احترافي",
        "ملون وجذاب",
        "بسيط",
        "بصري وتفاعلي"
    ]
)

st.divider()

generate = st.button(
    "✨ إنشاء الحزمة التعليمية",
    type="primary",
    use_container_width=True
)


if generate:

    if not topic.strip():

        st.error("اكتبي عنوان الدرس أولًا.")

    else:

        data = {
            "stage": stage,
            "grade": grade,
            "subject": subject,
            "strategy": strategy,
            "duration": duration,
            "difficulty": difficulty,
            "topic": topic.strip(),
            "notes": notes,
            "design": design
        }

        try:

            with st.spinner("مُعين يعمل على إعداد الدرس..."):

                lesson = generate_lesson(
                    data,
                    api_key,
                    model
                )

                st.session_state["lesson"] = lesson
                st.session_state["data"] = data

            st.success("تم إنشاء الحزمة التعليمية!")

        except Exception as e:

            st.error(f"حدث خطأ أثناء إنشاء الدرس: {e}")


# ==========================================
# عرض النتائج
# ==========================================

if "lesson" in st.session_state:

    lesson = st.session_state["lesson"]
    data = st.session_state["data"]

    st.divider()

    st.header("📚 " + lesson["title"])

    st.subheader("أهداف التعلم")

    for objective in lesson.get("objectives", []):

        st.write("✓ " + objective)

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs([
        "عرض PowerPoint",
        "ورقة العمل",
        "اللعبة",
        "دليل المعلم"
    ])

    with tab1:

        st.subheader("معاينة الشرائح")

        for i, slide in enumerate(lesson["slides"], 1):

            with st.expander(
                f"الشريحة {i}: {slide.get('title', '')}"
            ):

                st.write(slide.get("body", ""))

        pptx = create_powerpoint(lesson, data)

        st.download_button(
            "⬇️ تحميل PowerPoint",
            data=pptx,
            file_name="MUEEN_Presentation.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )

    with tab2:

        st.subheader("ورقة عمل الطالب")

        for i, question in enumerate(
            lesson["worksheet"], 1
        ):

            st.markdown(
                f"**{i}. {question['question']}**"
            )

            for option in question.get("options", []):

                st.write("□ " + option)

            st.write("الإجابة: __________________")

        pdf = create_pdf(lesson, data)

        st.download_button(
            "⬇️ تحميل ورقة العمل PDF",
            data=pdf,
            file_name="MUEEN_Worksheet.pdf",
            mime="application/pdf"
        )

        with st.expander("إظهار نموذج الإجابة"):

            for i, question in enumerate(
                lesson["worksheet"], 1
            ):

                st.write(
                    f"{i}. {question.get('answer', '')}"
                )

    with tab3:

        st.subheader("اللعبة التعليمية")

        game_html = create_game(lesson)

        components.html(
            game_html,
            height=600,
            scrolling=True
        )

        st.download_button(
            "⬇️ تحميل اللعبة",
            data=game_html.encode("utf-8"),
            file_name="MUEEN_Game.html",
            mime="text/html"
        )

    with tab4:

        st.subheader("دليل المعلم")

        st.write(lesson["teacher_guide"])

        st.subheader("بيانات الحصة")

        st.write("المرحلة: " + data["stage"])
        st.write("الصف: " + data["grade"])
        st.write("المادة: " + data["subject"])
        st.write("الاستراتيجية: " + data["strategy"])
        st.write(f"المدة: {data['duration']} دقيقة")

        lesson_json = json.dumps(
            lesson,
            ensure_ascii=False,
            indent=2
        )

        st.download_button(
            "⬇️ تحميل بيانات الدرس",
            data=lesson_json.encode("utf-8"),
            file_name="MUEEN_Lesson.json",
            mime="application/json"
        )

    st.warning(
        "المحتوى الناتج يحتاج مراجعة المعلم، "
        "ولا يُعد توثيقًا رسميًا لمحتوى المنهج السعودي."
    )

st.divider()

st.markdown(
    "<center>© MUEEN | مُعين — جميع الحقوق محفوظة</center>",
    unsafe_allow_html=True
)
