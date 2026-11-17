import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Loan Dashboard", layout="wide")


@st.cache_data
def load_data():
    df = pd.read_csv("loan_clean.csv")
    # إذا كان القرار Y/N نحوله إلى 1/0
    if df["Loan_Status"].dtype == "object":
        df["Loan_Status"] = df["Loan_Status"].map({"Y": 1, "N": 0})
    return df


df = load_data()

# 1) العنوان والوصف
st.title("Loan Approval Dashboard")
st.write("Explore loan applications and approval rates. Use the sidebar filters to change the results.")

# 2) الفلاتر في الـ Sidebar
st.sidebar.header("Filters")

all_areas = sorted(df["Property_Area"].dropna().unique())
areas = st.sidebar.multiselect("Property Area", all_areas, default=all_areas)

education = st.sidebar.radio("Education", ["All"] + sorted(df["Education"].dropna().unique()))

max_income = int(df["ApplicantIncome"].max())
income_limit = st.sidebar.slider("Max applicant income", 0, max_income, max_income)

# تطبيق الفلاتر
filtered = df[df["Property_Area"].isin(areas) & (df["ApplicantIncome"] <= income_limit)]
if education != "All":
    filtered = filtered[filtered["Education"] == education]

# 7) حالة صفر صفوف
if filtered.empty:
    st.warning("No applications match these filters. Try widening them.")
    st.stop()

# 3) الأرقام الرئيسية
m1, m2, m3 = st.columns(3)
m1.metric("Applications", len(filtered))
m2.metric("Approval rate", f"{filtered['Loan_Status'].mean() * 100:.1f}%")
m3.metric("Median loan amount", f"{filtered['LoanAmount'].median():.0f}")

# 4) رسمتان في عمودين
col_left, col_right = st.columns(2)

with col_left:
    fig1, ax1 = plt.subplots()
    sns.countplot(data=filtered, x="Loan_Status", ax=ax1)
    ax1.set_title("Approvals (1) vs Rejections (0)")
    st.pyplot(fig1)
    plt.close(fig1)

with col_right:
    fig2, ax2 = plt.subplots()
    sns.barplot(data=filtered, x="Credit_History", y="Loan_Status", ax=ax2)
    ax2.set_title("Approval Rate by Credit History")
    st.pyplot(fig2)
    plt.close(fig2)

# 5) اختيار عمود رقمي وعرض توزيعه
st.subheader("Distribution of a numeric column")
num_cols = filtered.select_dtypes(include="number").columns.tolist()
chosen = st.selectbox("Choose a column", num_cols)

fig3, ax3 = plt.subplots(figsize=(8, 4))
sns.histplot(data=filtered, x=chosen, kde=True, ax=ax3)
ax3.set_title(f"Distribution of {chosen}")
st.pyplot(fig3)
plt.close(fig3)

# 6) الجدول داخل expander
with st.expander("Show filtered data"):
    st.dataframe(filtered)