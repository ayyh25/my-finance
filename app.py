import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# إعداد الربط الآمن
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
client = gspread.authorize(creds)

# معرف ملفك
sheet_id = "1NsqAFO4_l8-EiLPlw3P1fQzOX0skjWO0DvwUI15gp8k"
sh = client.open_by_key(sheet_id)

st.title("📊 نظام ميزانية أبو معاذ الذكي")

# نموذج الإدخال
with st.form("entry_form"):
    st.subheader("📥 إضافة عملية جديدة")
    date = st.date_input("التاريخ")
    desc = st.text_input("البيان (مثلاً: راتب، تسوق، أسهم)")
    amount = st.number_input("المبلغ", min_value=0.0)
    target = st.selectbox("إرسال إلى:", ["سجل العمليات", "الاستثمارات"])
    
    if st.form_submit_button("حفظ البيانات ✅"):
        ws = sh.worksheet(target)
        ws.append_row([str(date), desc, amount])
        st.success("تم الحفظ في جوجل شيت بنجاح!")
        st.cache_data.clear()

# عرض ملخص بسيط
st.divider()
st.subheader("📝 آخر العمليات")
try:
    df = pd.DataFrame(sh.worksheet("سجل العمليات").get_all_records())
    st.table(df.tail(5))
except:
    st.info("بانتظار إدخال أول عملية لعرضها هنا.")
    return pd.read_csv(url)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 الاستثمارات")
    df_invest = get_data("الاستثمارات")
    st.dataframe(df_invest, use_container_width=True)

with col2:
    st.subheader("💸 آخر العمليات")
    df_ops = get_data("سجل العمليات")
    st.dataframe(df_ops, use_container_width=True)
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
