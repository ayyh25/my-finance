import streamlit as st
import pandas as pd

st.set_page_config(page_title="ميزانية أبو ميار", layout="centered")
st.title("📊 نظام الإدارة المالية والاستثمارات")

# رابط الملف (معرف ملفك V6)
sheet_id = "1NsqAFO4_l8-EiLPlw3P1fQzOX0skjWO0DvwUI15gp8k"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    df = pd.read_csv(sheet_url)
    st.metric("حالة المحفظة", "محدثة ✅")
    st.subheader("📈 بيانات الاستثمارات")
    st.dataframe(df)
    
    st.divider()
    with st.expander("➕ إضافة مصروف سريع"):
        st.number_input("المبلغ")
        st.selectbox("الفئة", ["قرض", "جمعية", "يومي"])
        st.button("حفظ")
except:
    st.error("تأكد من صلاحيات رابط جوجل شيت")
