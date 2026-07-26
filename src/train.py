import pandas as pd
import joblib

df=pd.read_csv("../data/processed/featured_loan_data.csv")
print(df.head())

x=df.drop(["defaulted","days_delinquent"],axis=1)
y=df["defaulted"]

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.20, random_state=42, stratify=y)

#logistic regression model
from sklearn.preprocessing import StandardScaler
scaler=StandardScaler()
temp_x_train=x_train
temp_x_test=x_test
temp_x_train=scaler.fit_transform(temp_x_train)
temp_x_test=scaler.transform(temp_x_test)
joblib.dump(scaler, "../models/scaler.pkl")

from sklearn.linear_model import LogisticRegression
lr=LogisticRegression(max_iter=1000,class_weight="balanced")
lr.fit(temp_x_train,y_train)

joblib.dump(lr, "C:/Users/ancha/Downloads/Loan Default Risk Analysis/models/logistic_regression.pkl")

#random forest classifier model
from sklearn.ensemble import RandomForestClassifier
rf=RandomForestClassifier(n_estimators=200, random_state=42,class_weight="balanced")
rf.fit(x_train,y_train)
joblib.dump(rf, "C:/Users/ancha/Downloads/Loan Default Risk Analysis/models/random_forest.pkl")

#XGBoost
from xgboost import XGBClassifier
xgb=XGBClassifier(random_state=42,eval_metric="logloss",scale_pos_weight=3.12)
xgb.fit(x_train,y_train)
joblib.dump(xgb,"C:/Users/ancha/Downloads/Loan Default Risk Analysis/models/xgboost.pkl")

print("all models saved successfully!!")
print(x_train.columns)