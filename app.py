import streamlit as st
from utils import prepare_input
from predictor import predict

st.set_page_config(
    page_title="Loan Default Prediction",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Loan Default Prediction System")
st.markdown("### Enter Customer details to predict loan default risk")
st.divider()

col1,col2=st.columns(2)

with col1:
    st.subheader("Customer Details")

    age=st.number_input("Age",min_value=18,max_value=100,value=30)
    education=st.selectbox("Education",["High School","Associate","Bachelor","Master","Doctorate"])
    years_employed=st.number_input("Years Employed",min_value=0, max_value=50,value=5)
    annual_income=st.number_input("Annual Income",min_value=1,max_value=60000,value=20000)
    credit_score=st.number_input("Credit Score",min_value=300,max_value=850,value=700)
    dependents=st.number_input("Depenedents",min_value=0,max_value=10,value=1)

with col2:
    st.subheader("Loan Details")
    existing_debt=st.number_input("Existing Monthly Debt",min_value=0,value=10000)
    loan_amount=st.number_input("Loan Amount",min_value=0,value=30000)
    term_months=st.selectbox("Loan Term(Months)",[12,24,36,48,60,72,84])
    interest_rate=st.slider("Interest Rate(%)",1.0,25.0,10.0)
    employment=st.selectbox("Employment Status",["Full-Time","Part-Time","Contract","Self-Employed","Retired"])
    home=st.selectbox("Home Ownership",["Own","Mortgage","Rent"])
    purpose=st.selectbox("Loan Purpose",["Auto Loan","Business Loan","Debt Consolidation","Education","Home Improvement","Major Purchase","Medical Expenses","Moving","Vacation","Wedding"])
    state=st.selectbox("State", [
            "AL","AZ","CA","CO","CT","FL","GA","IL","IN",
            "KY","LA","MA","MD","MI","MN","MO","NC","NJ",
            "NY","OH","OK","OR","PA","SC","TN","TX",
            "UT","VA","WA","WI"
        ])

st.divider()

predict_button=st.button("🔍 Predict Loan Default Risk",use_container_width=True)

if predict_button:

    customer = prepare_input(
        age=age,
        education_level=education,
        years_employed=years_employed,
        annual_income=annual_income,
        credit_score=credit_score,
        dependents=dependents,
        existing_monthly_debt=existing_debt,
        loan_amount=loan_amount,
        term_months=term_months,
        interest_rate=interest_rate,
        employment_status=employment,
        home_ownership=home,
        loan_purpose=purpose,
        state=state
    )

    prediction, probability = predict(customer)

    st.divider()
    st.subheader("📊 Prediction Result")

    if probability<0.30:
        risk_level="🟢 Low Risk"
        recommendation="Loan Can be Approved."
        box=st.success

    elif probability<0.60:
        risk_level= "🟡 Medium Risk"
        recommendation="⚠️ Manual review is recommended before approval."
        box=st.warning

    else:
        risk_level="🔴 High Risk"
        recommendation="❌ Loan should be rejected or investigated further."
        box=st.error

    #show risk level
    box(risk_level)

    #display metrics
    col1,col2=st.columns(2)

    with col1:
        st.metric(
            "probability of default",
            f"{probability:.2%}"
        )

    with col2:
        confidence=max(probability,1-probability)
        st.metric(
            "Model Confidence",
            f"{confidence:.2%}"
        )

    #progress bar
    st.write("### Default risk score")
    st.progress(float(probability))

    #recommendation
    st.write("### Recommendation")
    st.info(recommendation)

    st.divider()

    st.subheader("👤 Customer Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Age:** {age}")
        st.write(f"**Education:** {education}")
        st.write(f"**Employment:** {employment}")
        st.write(f"**Annual Income:** ₹{annual_income:,.0f}")
        st.write(f"**Credit Score:** {credit_score}")

    with col2:
        st.write(f"**Loan Amount:** ₹{loan_amount:,.0f}")
        st.write(f"**Interest Rate:** {interest_rate:.2f}%")
        st.write(f"**Loan Term:** {term_months} Months")
        st.write(f"**State:** {state}")
        st.write(f"**Home Ownership:** {home}")
        st.write(f"**Loan Purpose:** {purpose}")


    st.divider()

    st.subheader("📈 Financial Indicators")

    monthly_income = annual_income / 12
    monthly_payment = loan_amount / term_months
    dti_ratio = existing_debt / monthly_income
    loan_income_ratio = loan_amount / annual_income

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Monthly Income",
            f"₹{monthly_income:,.0f}"
        )

        st.metric(
            "Monthly Debt",
            f"₹{existing_debt:,.0f}"
        )

    with c2:
        st.metric(
            "Debt-to-Income Ratio",
            f"{dti_ratio:.2%}"
        )

        st.metric(
            "Loan-to-Income Ratio",
            f"{loan_income_ratio:.2f}"
        )

    st.divider()

    st.subheader("🏦 Loan Decision")

    if probability < 0.30:
        st.success("✅ APPROVED")

    elif probability < 0.60:
        st.warning("🟡 MANUAL REVIEW")

    else:
        st.error("❌ REJECTED")