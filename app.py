import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# إعداد الصفحة وتنسيق الاتجاه (من اليمين لليسار)
st.set_page_config(page_title="نظام أبو معاذ المالي", layout="wide")
st.markdown('<style>div.block-container{direction: rtl; text-align: right;}</style>', unsafe_allow_html=True)

# الربط مع جوجل شيت باستخدام الأسرار
try:
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    
    # معرف الملف الخاص بك
    sheet_id = "1NsqAFO4_l8-EiLPlw3P1fQzOX0skjWO0DvwUI15gp8k"
    sh = client.open_by_key(sheet_id)
except Exception as e:
    st.error(f"حدث خطأ في الاتصال: {e}")
    st.stop()

st.title("📊 نظام ميزانية أبو معاذ الذكي")

# --- نموذج إدخال البيانات ---
with st.expander("📥 إضافة عملية جديدة (مصاريف / أسهم)"):
    with st.form("add_form", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            date = st.date_input("التاريخ")
            desc = st.text_input("البيان (مثلاً: قسط، فاتورة، سهم)")
        with col_b:
            amount = st.number_input("المبلغ", min_value=0.0)
            target = st.selectbox("نوع العملية:", ["سجل العمليات", "الاستثمارات"])
        
        if st.form_submit_button("حفظ وإرسال ✅"):
            try:
                ws = sh.worksheet(target)
                ws.append_row([str(date), desc, amount])
                st.success("تم الحفظ في جوجل شيت بنجاح!")
                st.cache_data.clear()
            except Exception as e:
                st.error(f"فشل الحفظ: {e}")

# --- عرض البيانات المحدثة ---
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 محفظة الأسهم")
    try:
        data_inv = sh.worksheet("الاستثمارات").get_all_records()
        if data_inv:
            st.dataframe(pd.DataFrame(data_inv), use_container_width=True)
        else:
            st.info("لا توجد بيانات في ورقة الاستثمارات.")
    except:
        st.warning("تأكد من وجود ورقة باسم 'الاستثمارات'")

with col2:
    st.subheader("💸 آخر العمليات")
    try:
        data_ops = sh.worksheet("سجل العمليات").get_all_records()
        if data_ops:
            st.table(pd.DataFrame(data_ops).tail(5))
        else:
            st.info("لا توجد بيانات في سجل العمليات.")
    except:
        st.warning("تأكد من وجود ورقة باسم 'سجل العمليات'")
