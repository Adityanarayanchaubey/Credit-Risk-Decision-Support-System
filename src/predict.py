import pandas as pd
import joblib

# ==========================
# Load Model
# ==========================
model = joblib.load("../models/random_forest_tuned.pkl")

# ==========================
# Create Base Customer
# ==========================
columns = [
'age', 'education_level', 'years_employed', 'annual_income',
'credit_score', 'dependents', 'existing_monthly_debt', 'loan_amount',
'term_months', 'interest_rate', 'monthly_payment', 'dti_ratio',
'state_AL', 'state_AZ', 'state_CA', 'state_CO', 'state_CT', 'state_FL',
'state_GA', 'state_IL', 'state_IN', 'state_KY', 'state_LA', 'state_MA',
'state_MD', 'state_MI', 'state_MN', 'state_MO', 'state_NC', 'state_NJ',
'state_NY', 'state_OH', 'state_OK', 'state_OR', 'state_PA', 'state_SC',
'state_TN', 'state_TX', 'state_UT', 'state_VA', 'state_WA', 'state_WI',
'employment_status_Contract', 'employment_status_Full-Time',
'employment_status_Part-Time', 'employment_status_Retired',
'employment_status_Self-Employed', 'home_ownership_Mortgage',
'home_ownership_Own', 'home_ownership_Rent', 'loan_purpose_Auto Loan',
'loan_purpose_Business Loan', 'loan_purpose_Debt Consolidation',
'loan_purpose_Education', 'loan_purpose_Home Improvement',
'loan_purpose_Major Purchase', 'loan_purpose_Medical Expenses',
'loan_purpose_Moving', 'loan_purpose_Vacation', 'loan_purpose_Wedding',
'monthly_income', 'loan_income_ratio', 'high_dti',
'income_per_dependent'
]


def base_customer():
    return pd.DataFrame([[0]*len(columns)], columns=columns)


customers = []

# ==========================================================
# 1. LOW RISK CUSTOMER
# ==========================================================
c = base_customer()

c["age"] = 35
c["education_level"] = 2
c["years_employed"] = 10
c["annual_income"] = 1200000
c["credit_score"] = 780
c["dependents"] = 2
c["existing_monthly_debt"] = 10000
c["loan_amount"] = 300000
c["term_months"] = 36
c["interest_rate"] = 8.5
c["monthly_payment"] = 9500
c["dti_ratio"] = 0.22

c["state_TX"] = 1
c["employment_status_Full-Time"] = 1
c["home_ownership_Own"] = 1
c["loan_purpose_Home Improvement"] = 1

c["monthly_income"] = 100000
c["loan_income_ratio"] = 0.25
c["high_dti"] = 0
c["income_per_dependent"] = 33333

customers.append(("Low Risk", c))

# ==========================================================
# 2. MEDIUM RISK CUSTOMER
# ==========================================================
c = base_customer()

c["age"] = 30
c["education_level"] = 1
c["years_employed"] = 5
c["annual_income"] = 700000
c["credit_score"] = 680
c["dependents"] = 2
c["existing_monthly_debt"] = 18000
c["loan_amount"] = 500000
c["term_months"] = 60
c["interest_rate"] = 10.5
c["monthly_payment"] = 11000
c["dti_ratio"] = 0.38

c["state_CA"] = 1
c["employment_status_Full-Time"] = 1
c["home_ownership_Mortgage"] = 1
c["loan_purpose_Debt Consolidation"] = 1

c["monthly_income"] = 58333
c["loan_income_ratio"] = 0.71
c["high_dti"] = 0
c["income_per_dependent"] = 19444

customers.append(("Medium Risk", c))

# ==========================================================
# 3. HIGH RISK CUSTOMER
# ==========================================================
c = base_customer()

c["age"] = 24
c["education_level"] = 0
c["years_employed"] = 1
c["annual_income"] = 300000
c["credit_score"] = 520
c["dependents"] = 4
c["existing_monthly_debt"] = 30000
c["loan_amount"] = 800000
c["term_months"] = 84
c["interest_rate"] = 18.5
c["monthly_payment"] = 22000
c["dti_ratio"] = 0.75

c["state_FL"] = 1
c["employment_status_Part-Time"] = 1
c["home_ownership_Rent"] = 1
c["loan_purpose_Medical Expenses"] = 1

c["monthly_income"] = 25000
c["loan_income_ratio"] = 2.67
c["high_dti"] = 1
c["income_per_dependent"] = 5000

customers.append(("High Risk", c))

# ==========================================================
# 4. SELF EMPLOYED CUSTOMER
# ==========================================================
c = base_customer()

c["age"] = 42
c["education_level"] = 2
c["years_employed"] = 12
c["annual_income"] = 900000
c["credit_score"] = 710
c["dependents"] = 1
c["existing_monthly_debt"] = 15000
c["loan_amount"] = 450000
c["term_months"] = 48
c["interest_rate"] = 9.8
c["monthly_payment"] = 12000
c["dti_ratio"] = 0.32

c["state_NY"] = 1
c["employment_status_Self-Employed"] = 1
c["home_ownership_Own"] = 1
c["loan_purpose_Business Loan"] = 1

c["monthly_income"] = 75000
c["loan_income_ratio"] = 0.50
c["high_dti"] = 0
c["income_per_dependent"] = 37500

customers.append(("Self Employed", c))

# ==========================================================
# 5. YOUNG FIRST-TIME BORROWER
# ==========================================================
c = base_customer()

c["age"] = 22
c["education_level"] = 1
c["years_employed"] = 0
c["annual_income"] = 450000
c["credit_score"] = 640
c["dependents"] = 0
c["existing_monthly_debt"] = 5000
c["loan_amount"] = 250000
c["term_months"] = 60
c["interest_rate"] = 11.2
c["monthly_payment"] = 5600
c["dti_ratio"] = 0.30

c["state_CA"] = 1
c["employment_status_Full-Time"] = 1
c["home_ownership_Rent"] = 1
c["loan_purpose_Auto Loan"] = 1

c["monthly_income"] = 37500
c["loan_income_ratio"] = 0.56
c["high_dti"] = 0
c["income_per_dependent"] = 37500

customers.append(("Young Borrower", c))

# ==========================================================
# Predictions
# ==========================================================

print("="*70)
print("LOAN DEFAULT PREDICTIONS")
print("="*70)

for name, customer in customers:

    prediction = model.predict(customer)[0]
    probability = model.predict_proba(customer)[0][1]

    print(f"\n{name}")
    print("-"*40)
    print("Prediction :", "DEFAULT" if prediction==1 else "NO DEFAULT")
    print(f"Probability of Default : {probability:.2%}")

