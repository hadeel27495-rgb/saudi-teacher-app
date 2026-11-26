import streamlit as st
import pandas as pd
import time

# إعدادات صفحة التطبيق
st.set_page_config(page_title="منصة معلم الذكية - إدارة المناهج والدروس", page_icon="📚", layout="wide")

# --- 1. تهيئة الذاكرة المؤقتة لحفظ الدروس المحضرة ---
if "saved_lessons" not in st.session_state:
    st.session_state.saved_lessons = []

# --- 2. قاعدة بيانات الكتب والمناهج ---
CURRICULUM_DATABASE = {
    "المرحلة الابتدائية": {
        "الرياضيات": {
            "الصف الأول": {
                "الفصل الدراسي الأول": [
                    {"lesson": "المقارنة والتصنيف", "start_page": 10, "end_page": 25},
                    {"lesson": "الأعداد حتى 5", "start_page": 26, "end_page": 45},
                ]
            },
            "الصف الثاني": {
                "الفصل الدراسي الأول": [
                    {"lesson": "القيمة المنزلية حتى 100", "start_page": 12, "end_page": 35},
                    {"lesson": "جمع العدد إلى نفسه", "start_page": 36, "end_page": 50},
                ]
            }
        },
        "العلوم": {
            "الصف الثالث": {
                "الفصل الدراسي الأول": [
                    {"lesson": "النباتات وأجزاؤها", "start_page": 15, "end_page": 30},
                    {"lesson": "التكاثر في النباتات", "start_page": 31, "end_page": 48},
                ]
            }
        }
    },
    "المرحلة المتوسطة": {
        "الرياضيات": {
            "الصف الثاني المتوسط": {
                "الفصل الدراسي الثاني": [
                    {"lesson": "حجم المخروط والكرة", "start_page": 112, "end_page": 118},
                    {"lesson": "التشابه والمضلعات", "start_page": 120, "end_page": 135},
                ]
            }
        },
        "العلوم": {
            "الصف الأول المتوسط": {
                "الفصل الدراسي الأول": [
                    {"lesson": "طبيعة العلم", "start_page": 8, "end_page": 22},
                    {"lesson": "حركة الأجسام والقوى", "start_page": 25, "end_page": 44},
                ]
            }
        }
    }
}

# تصميم الواجهة الرئيسية
st.title("📚 منصة معلم الذكية - المناهج السعودية وتحضير الدروس")
st.markdown("---")

# الشريط الجانبي لاختيار المنهج واستعلام قاعدة البيانات
with st.sidebar:
    st.header("⚙️ إعدادات الدرس الجديد")
    
    stages = list(CURRICULUM_DATABASE.keys())
    stage = st.selectbox("المرحلة الدراسية", stages)
    
    subjects = list(CURRICULUM_DATABASE[stage].keys())
    subject = st.selectbox("المادة", subjects)
    
    grades = list(CURRICULUM_DATABASE[stage][subject].keys())
    grade = st.selectbox("الصف", grades)
    
    terms = list(CURRICULUM_DATABASE[stage][subject][grade].keys())
    term = st.selectbox("الفصل الدراسي", terms)
    
    st.markdown("---")
    st.subheader("📖 تحديد الدرس")
    
    lessons_list = CURRICULUM_DATABASE[stage][subject][grade][term]
    lesson_titles = [item["lesson"] for item in lessons_list]
    selected_lesson_title = st.selectbox("اختر الدرس", lesson_titles)
    
    selected_lesson_data = next(item for item in lessons_list if item["lesson"] == selected_lesson_title)
    
    col1, col2 = st.columns(2)
    with col1:
        start_page = st.number_input("من صفحة", value=selected_lesson_data["start_page"])
    with col2:
        end_page = st.number_input("إلى صفحة", value=selected_lesson_data["end_page"])
        
    st.markdown("---")
    
    strategy = st.selectbox(
        "استراتيجية التدريس",
        [
            "التعلم التعاوني (فكر - زاوج - شارك)",
            "العصف الذهني",
            "الرؤوس المرقمة",
            "استراتيجية القبعات الست",
            "حل المشكلات"
        ]
    )
    
    st.markdown("---")
    generate_btn = st.button("🚀 توليد الدرس وحفظه")

# منطقة العرض الرئيسية (مقسّمة لتبويبات)
tab_main, tab_saved = st.tabs(["✨ توليد وعرض الدرس الحالي", f"📁 سجل الدروس المحفوظة ({len(st.session_state.saved_lessons)})"])

with tab_main:
    if generate_btn:
        with st.spinner(f"جاري تحليل صفحات درس '{selected_lesson_title}' وتوليد المحتوى والشرائح والألعاب... ⏳"):
            time.sleep(2)
        
        new_lesson_record = {
            "title": selected_lesson_title,
            "path": f"{stage} > {subject} > {grade} > {term}",
            "pages": f"من ص {start_page} إلى ص {end_page}",
            "strategy": strategy,
            "date": time.strftime("%Y-%m-%d %H:%M")
        }
        
        if new_lesson_record not in st.session_state.saved_lessons:
            st.session_state.saved_lessons.append(new_lesson_record)
        
        st.success(f"✨ تم إنشاء وحفظ درس **{selected_lesson_title}** في سجل الدروس بنجاح!")
        st.info(f"📍 **المسار:** {new_lesson_record['path']}")
        
        st.subheader(f"📊 شرائح الباوربوينت (استراتيجية: {strategy})")
        st.markdown(f"""
        * **الشريحة 1:** التمهيد وطرح مشكلة مرتبطة بـ *{selected_lesson_title}*.
        * **الشريحة 2:** المفاهيم والأنشطة المستخرجة ({new_lesson_record['pages']}).
        * **الشريحة 3:** خطوات تطبيق استراتيجية **{strategy}**.
        * **الشريحة 4:** التقويم والواجب المدرسي.
        """)
        st.download_button("📥 تحميل ملف PowerPoint (PPTX)", data="dummy_data", file_name=f"{selected_lesson_title}.pptx")
        
        st.subheader("🎮 الألعاب والأنشطة المقترحة")
        st.markdown(f"1. **مسابقة تفاعلية حول موضوع: {selected_lesson_title}**")
        st.markdown("2. **تحدي المجموعات الذكية**")
        
    else:
        st.info("👈 قم باختيار بيانات الدرس من القائمة الجانبية ثم اضغط على زر **توليد الدرس وحفظه**.")

with tab_saved:
    st.subheader("📁 سجل التحضيرات السابقة")
    if len(st.session_state.saved_lessons) == 0:
        st.warning("⚠️ لا توجد دروس محفوظة حتى الآن. قم بتوليد درس جديد ليظهر هنا.")
    else:
        for idx, lesson in enumerate(st.session_state.saved_lessons):
            with st.expander(f"📚 {lesson['title']} ({lesson['path']})"):
                st.write(f"**الصفحات:** {lesson['pages']}")
                st.write(f"**استراتيجية التدريس:** {lesson['strategy']}")
                st.write(f"**تاريخ التحضير:** {lesson['date']}")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    st.download_button("📥 تحميل الباوربوينت", data="dummy_data", file_name=f"{lesson['title']}.pptx", key=f"down_{idx}")
                with col_btn2:
                    if st.button("🗑️ حذف من السجل", key=f"del_{idx}"):
                        st.session_state.saved_lessons.pop(idx)
                        st.rerun()
