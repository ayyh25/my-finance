import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="نظام الإدارة المالية", layout="wide")

# إعدادات الرابط
sheet_id = "1NsqAFO4_l8-EiLPlw3P1fQzOX0skjWO0DvwUI15gp8k"

# قائمة جانبية للإدخال
st.sidebar.header("📥 إدخال بيانات جديدة")
tab_choice = st.sidebar.selectbox("اختر نوع الإدخال:", ["سجل العمليات", "الاستثمارات"])

if tab_choice == "سجل العمليات":
    with st.sidebar.form("ops_form"):
        date = st.date_input("التاريخ", datetime.now())
        desc = st.text_input("البيان (مثلاً: راتب، قسط، تسوق)")
        amount = st.number_input("المبلغ", min_value=0.0)
        cat = st.selectbox("التصنيف", ["راتب", "مصاريف ثابتة", "أسهم", "نثريات"])
        submit = st.form_submit_button("حفظ العملية")
        if submit:
            st.sidebar.success("سيتم الحفظ في جوجل شيت..")
            # هنا سيتم الربط البرمجي للكتابة لاحقاً

elif tab_choice == "الاستثمارات":
    with st.sidebar.form("invest_form"):
        stock_name = st.text_input("اسم السهم")
        buy_price = st.number_input("سعر الشراء")
        current_price = st.number_input("السعر الحالي")
        submit = st.form_submit_button("إضافة للمحفظة")

# --- عرض البيانات الحالي ---
st.title("📊 لوحة التحكم المالية")

def get_data(sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
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
