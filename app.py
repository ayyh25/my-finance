import streamlit as st
import pandas as pd

# إعدادات الصفحة والواجهة
st.set_page_config(page_title="ميزانية أبو ميار", layout="centered")

st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    div[data-testid="stMetricValue"] { text-align: right; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 نظام الإدارة المالية المطور")

# رابط ملف جوجل شيت V6
sheet_id = "1NsqAFO4_l8-EiLPlw3P1fQzOX0skjWO0DvwUI15gp8k"

# دوال لجلب أوراق محددة من الملف
@st.cache_data(ttl=300)
def get_sheet_data(sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    return pd.read_csv(url)

try:
    # 1. جلب بيانات الاستثمارات
    df_invest = get_sheet_data("الاستثمارات")
    
    # عرض إحصائيات سريعة في الأعلى
    st.subheader("💰 ملخص المحفظة")
    c1, c2 = st.columns(2)
    # ملاحظة: استبدل أسماء الأعمدة بما يطابق ملفك (مثلاً: 'السعر الحالي' و 'الزكاة')
    with c1:
        st.metric("حالة النظام", "متصل ✅")
    with c2:
        st.metric("تحديث البيانات", "تلقائي 🔄")

    st.divider()

    # 2. عرض جدول الاستثمارات بتنسيق لوني
    st.subheader("📈 محفظة الأسهم والاستثمارات")
    
    # دالة لتلوين الخلايا (أخضر للربح وأحمر للخسارة)
    def color_profit(val):
        if isinstance(val, (int, float)):
            color = 'green' if val > 0 else 'red' if val < 0 else 'black'
            return f'color: {color}; font-weight: bold'
        return ''

    # عرض الجدول (تأكد من وجود عمود باسم 'الربح/الخسارة' في ملفك)
    if 'الربح/الخسارة' in df_invest.columns:
        st.dataframe(df_invest.style.applymap(color_profit, subset=['الربح/الخسارة']))
    else:
        st.dataframe(df_invest)

    # 3. قسم سجل العمليات (المصاريف)
    st.divider()
    st.subheader("💸 سجل العمليات الأخيرة")
    df_ops = get_sheet_data("سجل العمليات")
    st.table(df_ops.tail(5)) # عرض آخر 5 عمليات فقط للتبسيط

    # زر تحديث يدوي
    if st.button("تحديث البيانات الآن"):
        st.cache_data.clear()
        st.rerun()

except Exception as e:
    st.error("لم نتمكن من قراءة أوراق البيانات. تأكد من تسمية الأوراق بـ 'الاستثمارات' و 'سجل العمليات' داخل ملف جوجل شيت.")
