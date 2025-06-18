
import streamlit as st
import os
import docx
import fitz  # PyMuPDF لقراءة PDF
from docx import Document
import tempfile
import re

# ----- نموذج تبسيطي لاستخراج القواعد (يُستبدل لاحقًا بذكاء اصطناعي) ----- #
def تحليل_الحكم_واستخراج_القواعد(text):
    # هذا نموذج تجريبي - يمكن ربطه لاحقًا بـ GPT لتحليل دقيق
    نوع_القضية = "مدنية" if "مدنية" in text else "غير محدد"
    الاشكاليات = "لم تُستخرج تلقائيًا - النموذج بسيط"
    رد_المحكمة = "لم يُحدد - النموذج التجريبي"
    القاعدة = "لم تُستخرج - يتطلب نموذج ذكي"
    return نوع_القضية, الاشكاليات, رد_المحكمة, القاعدة

# ----- قراءة محتوى PDF ----- #
def قراءة_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# ----- قراءة محتوى Word ----- #
def قراءة_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

# ----- واجهة Streamlit ----- #
st.title("تحليل الأحكام القضائية واستخراج القواعد")
st.write("قم برفع ملفات الأحكام بصيغة PDF أو Word، وسنقوم بتحليلها تلقائيًا.")

uploaded_files = st.file_uploader("ارفع الأحكام هنا", type=["pdf", "docx"], accept_multiple_files=True)

if uploaded_files:
    if st.button("ابدأ التحليل وإنشاء الملف"):
        output_doc = Document()

        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            # رقم الطعن من اسم الملف
            اسم_الملف = uploaded_file.name
            رقم_الطعن = re.findall(r"\d+", اسم_الملف)
            رقم_الطعن = رقم_الطعن[0] if رقم_الطعن else "غير معروف"

            # قراءة النص
            if uploaded_file.name.endswith(".pdf"):
                النص = قراءة_pdf(tmp_path)
            else:
                النص = قراءة_docx(tmp_path)

            # التحليل
            نوع, اشكاليات, رد, قاعدة = تحليل_الحكم_واستخراج_القواعد(نص)

            # إنشاء صفحة جديدة في ملف Word
            output_doc.add_paragraph(f"رقم الطعن: {رقم_الطعن}")
            output_doc.add_paragraph(f"نوع القضية: {نوع}")
            output_doc.add_paragraph(f"الإشكاليات المثارة: {اشكاليات}")
            output_doc.add_paragraph(f"رد المحكمة العليا: {رد}")
            output_doc.add_paragraph(f"القاعدة القضائية المستخلصة: {قاعدة}")
            output_doc.add_page_break()

            os.unlink(tmp_path)  # حذف الملف المؤقت

        # حفظ الملف النهائي
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as f:
            output_doc.save(f.name)
            st.success("تم إنشاء الملف بنجاح!")
            with open(f.name, "rb") as file:
                st.download_button("📥 تحميل الملف النهائي", file.read(), file_name="القواعد_القضائية.docx")
