import streamlit as st

st.set_page_config(page_title="S&P 500 Pension Simulator", layout="centered")

# Step 1: Choose language
if "lang" not in st.session_state:
    st.session_state.lang = st.radio("Choose language / בחר שפה", ["English", "עברית"])

lang = st.session_state.lang

# Step 2: Define translations
TEXT = {
    "English": {
        "title": "📈 S&P 500 Pension Simulator",
        "intro": "Estimate your pension balance with realistic return scenarios.",
        "years_until_ret": "Years until retirement:",
        "years_contributing": "How many of those years will you be actively contributing?",
        "current_balance": "Current pension balance (NIS):",
        "salary": "Expected gross monthly salary (NIS):",
        "run": "Run Simulation",
        "results_title": "📊 Estimated Total Pension Balance (after management fees):",
        "monthly_check": "Show estimated monthly pension",
        "custom_annuity": "I want to enter a custom annuity factor",
        "gender_prompt": "Your gender (for estimating annuity factor):",
        "monthly_title": "💰 Estimated Monthly Pension (Annuity Factor = {annuity_factor}):",
        "male": "Male",
        "female": "Female"
    },
    "עברית": {
        "title": "📈 מחשבון פנסיה לפי S&P 500",
        "intro": "הערכת צבירת פנסיה על בסיס תרחישי תשואה ריאליים.",
        "years_until_ret": "כמה שנים עד לפרישה:",
        "years_contributing": "כמה מהשנים האלו תפריש בפועל:",
        "current_balance": "כמה יש לך כרגע בקרן (ש\"ח):",
        "salary": "שכר חודשי ברוטו בעת עבודה (ש\"ח):",
        "run": "חשב פנסיה",
        "results_title": "📊 סכום פנסיה כולל צפוי (לאחר דמי ניהול):",
        "monthly_check": "הצג הערכת קצבה חודשית",
        "custom_annuity": "אני רוצה להזין מקדם קצבה בעצמי",
        "gender_prompt": "מה המגדר שלך (לצורך מקדם):",
        "monthly_title": "💰 קצבת פנסיה חודשית מוערכת (מקדם = {annuity_factor}):",
        "male": "זכר",
        "female": "נקבה"
    }
}

txt = TEXT[lang]

# Title
st.title(txt["title"])
st.write(txt["intro"])

# Inputs
years_until_retirement = st.number_input(txt["years_until_ret"], min_value=1, max_value=70, value=41)
years_contributing = st.number_input(txt["years_contributing"], min_value=0, max_value=70, value=39)
years_until_start = years_until_retirement - years_contributing

initial_balance = st.number_input(txt["current_balance"], min_value=0.0, value=27500.0)
expected_salary = st.number_input(txt["salary"], min_value=0.0, value=18000.0)

# Constants
management_fee = 0.007
monthly_contribution_rate = 0.18

return_scenarios = {
    "Very Optimistic (10%)": 0.10,
    "Optimistic (7%)": 0.07,
    "Realistic (6%)": 0.06,
    "Conservative (4%)": 0.04,
    "Minimum Scenario (3%)": 0.03
}

def simulate(years, contribute_years, delay, balance, salary, rate):
    for year in range(years):
        if year >= delay:
            annual_contrib = salary * 12 * monthly_contribution_rate
        else:
            annual_contrib = 0
        balance = balance * (1 + rate - management_fee) + annual_contrib
    return balance

if "results" not in st.session_state:
    st.session_state.results = None

if st.button(txt["run"]):
    results = {}
    for label, r in return_scenarios.items():
        results[label] = round(simulate(
            years_until_retirement,
            years_contributing,
            years_until_start,
            initial_balance,
            expected_salary,
            r
        ), 2)
    st.session_state.results = results

if st.session_state.results:
    st.subheader(txt["results_title"])
    for label, amount in st.session_state.results.items():
        st.write(f"{label}: {amount:,.2f} NIS")

    if st.checkbox(txt["monthly_check"]):
        use_custom = st.checkbox(txt["custom_annuity"])
        if use_custom:
            annuity_factor = st.number_input("Enter annuity factor / הזן מקדם קצבה", min_value=1.0, value=205.0)
        else:
            gender = st.radio(txt["gender_prompt"], [txt["male"], txt["female"]])
            annuity_factor = 205 if gender == txt["male"] else 215

        st.subheader(txt["monthly_title"].format(annuity_factor=annuity_factor))
        for label, total in st.session_state.results.items():
            monthly = round(total / annuity_factor, 2)
            st.write(f"{label}: {monthly:,.2f} NIS/month")
