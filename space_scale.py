import pandas as pd
import streamlit as st

# معاملات الجاذبية للكواكب مقارنة بالأرض
GRAVITY = {
    "Mercury": 0.38,
    "Venus": 0.90,
    "Earth": 1.00,
    "Moon": 0.17,
    "Mars": 0.38,
    "Jupiter": 2.53,
    "Saturn": 1.07,
    "Uranus": 0.89,
    "Neptune": 1.14,
}

st.title("🪐 ميزان الفضاء")
st.write("تطبيق صغير يقول للمستخدم كم يزن على الكواكب الأخرى مقارنة للأرض[span_0](start_span)[span_0](end_span).")

# 1. إدخال وزن المستخدم واختيار الكوكب
weight_earth = st.number_input(
    "أدخل وزنك على الأرض (كجم):", min_value=1.0, value=60.0
)
planet = st.selectbox("اختر الكوكب:", list(GRAVITY.keys()))

# حساب الوزن الجديد
planet_weight = weight_earth * GRAVITY[planet]
diff = planet_weight - weight_earth

# 2. عرض النتيجة باستخدام st.metric مع الفرق
st.metric(
    label=f"وزنك على {planet}",
    value=f"{planet_weight:.2f} كجم",
    delta=f"{diff:.2f} كجم مقارنة بالأرض",
)

# 3. رسالة مختلفة حسب النتيجة (أخف أو أثقل)
if planet_weight < weight_earth:
    st.success(
        f"يا سلام! ستكون أخف في {planet} بمقدار {abs(diff):.2f} كجم. هل أنت جاهز للقفز لأعلى؟"
    )
elif planet_weight > weight_earth:
    st.warning(
        f"ستكون أثقل في {planet} بمقدار {diff:.2f} كجم بسبب الجاذبية العالية!"
    )
else:
    st.info("وزنك مطابق تماماً لوزنك على الأرض.")

# 4. رسم بياني يوضح الوزن على كل الكواكب
st.subheader("📊 مقارنة وزنك على كل الكواكب")
chart_data = pd.DataFrame(
    {
        "Planet": list(GRAVITY.keys()),
        "Weight": [weight_earth * g for g in GRAVITY.values()],
    }
)
st.bar_chart(chart_data.set_index("Planet"))