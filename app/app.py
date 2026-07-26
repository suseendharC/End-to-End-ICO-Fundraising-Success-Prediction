import streamlit as st
import pandas as pd
import joblib
import os

# -------------------------
# Load saved model files
# -------------------------
model = joblib.load("models/ico_success_model.pkl")
scaler = joblib.load("models/scaler.pkl")
feature_names = joblib.load("models/feature_names.pkl")

# -------------------------
# Page configuration
# -------------------------
st.set_page_config(page_title="ICO Success Prediction")

st.title("🚀 ICO Fundraising Success Prediction")

st.write("This app predicts whether an ICO fundraising campaign will be successful.")

st.header("Project by Suseendhar")

# -------------------------
# Sidebar
# -------------------------
st.sidebar.title("About")

st.sidebar.info(
    """
    This application predicts whether an ICO fundraising campaign
    is likely to be successful using a Machine Learning model.

    **Model Used:**
    - Random Forest (Hyperparameter Tuned)
    """
)

st.markdown("---")

st.header("Enter ICO Details")

price_usd = st.number_input(
    "Token Price (USD)",
    min_value=0.0,
    value=0.15,
    step=0.01
)

distributed_in_ico = st.number_input(
    "Tokens Distributed (%)",
    min_value=0.0,
    value=60.0
)

token_for_sale = st.number_input(
    "Tokens for Sale",
    min_value=0.0,
    value=150000000.0
)

rating = st.slider(
    "ICO Rating",
    0.0,
    5.0,
    4.0,
    0.1
)

teamsize = st.number_input(
    "Team Size",
    min_value=1,
    value=10
)

kyc = st.selectbox(
    "KYC Required?",
    ["Yes", "No"]
)

bonus = st.selectbox(
    "Bonus Available?",
    ["Yes", "No"]
)

whitelist = st.selectbox(
    "Whitelist?",
    ["Yes", "No"]
)

ico_start_year = st.number_input(
    "ICO Start Year",
    2014,
    2030,
    2024
)

ico_start_month = st.slider(
    "ICO Start Month",
    1,
    12,
    1
)

ico_end_year = st.number_input(
    "ICO End Year",
    2014,
    2030,
    2024
)

ico_end_month = st.slider(
    "ICO End Month",
    1,
    12,
    3
)

ico_duration_days = st.number_input(
    "ICO Duration (Days)",
    min_value=1,
    value=60
)

country = st.selectbox(
    "Country",
    [
        "USA",
        "Singapore",
        "Switzerland",
        "United Kingdom",
        "Russia",
        "Estonia",
        "Canada",
        "Australia",
        "China",
        "Japan",
        "Germany",
        "France",
        "India",
        "South Korea",
        "Other"
    ]
)

predict = st.button("Predict Success")

if predict:

    input_data = {
        "price_usd": price_usd,
        "distributed_in_ico": distributed_in_ico,
        "token_for_sale": token_for_sale,
        "rating": rating,
        "teamsize": teamsize,
        "kyc": 1 if kyc == "Yes" else 0,
        "bonus": 1 if bonus == "Yes" else 0,
        "whitelist": 1 if whitelist == "Yes" else 0,
        "ico_start_year": ico_start_year,
        "ico_start_month": ico_start_month,
        "ico_end_year": ico_end_year,
        "ico_end_month": ico_end_month,
        "ico_duration_days": ico_duration_days
    }

    input_df = pd.DataFrame([[0.0] * len(feature_names)], columns=feature_names)

    for key, value in input_data.items():
        if key in input_df.columns:
            input_df.at[0, key] = value

    country_column = f"country_{country}"

    if country_column in input_df.columns:
        input_df.at[0, country_column] = 1

    # Scale the input
    input_scaled = scaler.transform(input_df)

    # Make prediction
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0][1]

    st.markdown("---")

    if prediction == 1:
        st.success("🎉 Prediction: SUCCESS")
        st.write("The ICO fundraising campaign is likely to be successful.")
    else:
        st.error("❌ Prediction: FAILURE")
        st.write("The ICO fundraising campaign is likely to fail.")

    st.subheader("Model Confidence")

    st.progress(float(probability))

    st.metric(
        "Success Probability",
        f"{probability:.2%}"
    )

    st.markdown("---")

    st.subheader("Probability Breakdown")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Success Probability",
            f"{probability:.2%}"
        )

    with col2:
        st.metric(
            "Failure Probability",
            f"{1 - probability:.2%}"
        )