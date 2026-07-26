import pandas as pd

FEATURE_COLUMNS = [
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



def prepare_input(
    age,
    education_level,
    years_employed,
    annual_income,
    credit_score,
    dependents,
    existing_monthly_debt,
    loan_amount,
    term_months,
    interest_rate,
    employment_status,
    home_ownership,
    loan_purpose,
    state
    
):
    education_map = {
    "High School": 1,
    "Associate": 2,
    "Bachelor": 3,
    "Master": 4,
    "Doctorate": 5
}
    education_level = education_map[education_level]

    customer=pd.DataFrame([[0]*len(FEATURE_COLUMNS)],columns=FEATURE_COLUMNS)

    customer["age"] = age
    customer["education_level"] = education_level
    customer["years_employed"] = years_employed
    customer["annual_income"] = annual_income
    customer["credit_score"] = credit_score
    customer["dependents"] = dependents
    customer["existing_monthly_debt"] = existing_monthly_debt
    customer["loan_amount"] = loan_amount
    customer["term_months"] = term_months
    customer["interest_rate"] = interest_rate

    monthly_income = annual_income / 12

    monthly_payment = loan_amount / term_months

    dti_ratio = existing_monthly_debt / monthly_income

    loan_income_ratio = loan_amount / annual_income

    income_per_dependent = monthly_income / (dependents + 1)

    high_dti = 1 if dti_ratio > 0.4 else 0

    customer["monthly_income"] = monthly_income
    customer["monthly_payment"] = monthly_payment
    customer["dti_ratio"] = dti_ratio
    customer["loan_income_ratio"] = loan_income_ratio
    customer["income_per_dependent"] = income_per_dependent
    customer["high_dti"] = high_dti

    customer[f"state_{state}"] = 1

    customer[f"employment_status_{employment_status}"] = 1

    customer[f"home_ownership_{home_ownership}"] = 1

    customer[f"loan_purpose_{loan_purpose}"] = 1

    return customer
    