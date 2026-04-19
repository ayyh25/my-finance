import streamlit as st
import pandas as pd

# إعدادات واجهة التطبيق
st.set_page_config(page_title="نظام الإدارة المالية", layout="centered")

# تنسيق العناوين من اليمين لليسار
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    div[data-testid="stMetricValue"] { text-align: right; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 نظام الإدارة المالية المطور")

# معرف ملف جوجل شيت V6 الخاص بك
sheet_id = "1NsqAFO4_l8-EiLPlw3P1fQzOX0skjWO0DvwUI15gp8k"

# دالة ذكية لجلب البيانات من ورقة محددة
@st.cache_data(ttl=60)
def get_data(sheet_name):
    try:
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        return pd.read_csv(url)
    except:
        return None

# جلب البيانات من الأوراق التي أنشأتها
df_invest = get_data("الاستثمارات")
df_ops = get_data("سجل العمليات")

# عرض قسم الاستثمارات
st.subheader("📈 محفظة الاستثمارات")
if df_invest is not None and not df_invest.empty:
    st.dataframe(df_invest, use_container_width=True)
else:
    st.info("بانتظار إضافة بيانات في ورقة 'الاستثمارات'")

st.divider()

# عرض سجل العمليات
st.subheader("💸 سجل العمليات والمصاريف")
if df_ops is not None and not df_ops.empty:
    st.table(df_ops.tail(10)) # عرض آخر 10 عمليات
else:
    st.info("بانتظار إضافة بيانات في ورقة 'سجل العمليات'")

# زر لتحديث البيانات يدوياً
if st.button("تحديث البيانات 🔄"):
    st.cache_data.clear()
    st.rerun()
