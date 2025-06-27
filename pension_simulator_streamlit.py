import streamlit as st

st.set_page_config(page_title="Pension Simulator", page_icon="📊")
st.title("📊 Pension Simulator")

st.markdown("""
This tool simulates your future pension savings based on expected salary and savings behavior.
Realistic S&P 500-based return scenarios are included, with management fees taken into account.
""")

# Input section
years_until_withdrawal = st.number_input("1. Years until you retire:", min_value=1, value=41)
years_until_work = st.number_input("2. Years until you start working and contributing (0 if already contributing):", min_value=0, value=2)
initial_amount = st.number_input("3. Current pension balance (NIS):", min_value=0.0, value=27500.0)
average_salary = st.number_input("4. Expected gross monthly salary when working (NIS):", min_value=0.0, value=18000.0)

if st.button("Run Simulation"):
    # Parameters
    contribution_rate = 0.185
    management_fee_contribution = 0.02
    management_fee_balance = 0.0025

    annual_gross_contribution = average_salary * 12 * contribution_rate
    annual_net_contribution = annual_gross_contribution * (1 - management_fee_contribution)

    base_rates = {
        "Very Optimistic (10%)": 0.10,
        "Optimistic (7%)": 0.07,
        "Realistic (6%)": 0.06,
        "Conservative (4%)": 0.04,
        "Minimum Scenario (3%)": 0.03
    }

    net_rates = {label: round(rate - management_fee_balance, 5) for label, rate in base_rates.items()}

    results = {}

    for label, rate in net_rates.items():
        amount = initial_amount
        for year in range(years_until_withdrawal):
            if year >= years_until_work:
                amount = amount * (1 + rate) + annual_net_contribution
            else:
                amount *= (1 + rate)
        results[label] = round(amount, 2)

    st.subheader("📈 Estimated Total Pension Balance (after management fees):")
    for label, amount in results.items():
        st.write(f"{label}: {amount} NIS")

    # Monthly pension estimate
    if st.checkbox("Show estimated monthly pension"):
        use_custom_factor = st.checkbox("I want to enter a custom annuity factor")

        if use_custom_factor:
            annuity_factor = st.number_input("Enter your annuity factor (e.g. 205):", min_value=1.0, value=205.0)
        else:
            gender = st.radio("Your gender:", ["Male", "Female"])
            annuity_factor = 205 if gender == "Male" else 215

        st.subheader(f"💰 Estimated Monthly Pension (Annuity Factor = {annuity_factor}):")
        for label, total in results.items():
            monthly = round(total / annuity_factor, 2)
            st.write(f"{label}: {monthly} NIS/month")
