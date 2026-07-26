import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,confusion_matrix

#loading dataset
df=pd.read_csv("../data/processed/featured_loan_data.csv")

#train_test_split
x=df.drop(["defaulted","days_delinquent"],axis=1)
y=df["defaulted"]
x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=42,test_size=0.20,stratify=y)

#loading all models
lr=joblib.load("../models/logistic_regression.pkl")
rf=joblib.load("../models/random_forest.pkl")
xgb=joblib.load("../models/xgboost.pkl")

#evaluation function
def evaluate_models(model,model_name):
    if model_name=="logistic_regression":
        scaler=joblib.load("../models/scaler.pkl")
        x=scaler.transform(x_test)
    else:
        x=x_test
    
    y_pred=model.predict(x)

    if hasattr(model,"predict_proba"):
        y_prob=model.predict_proba(x)[:,1]
    else:
        y_prob=y_pred

    

    metrics={
        "Model":model_name,
        "Accuracy":accuracy_score(y_test,y_pred),
        "Precision":precision_score(y_test,y_pred),
        "Recall":recall_score(y_test,y_pred),
        "F1 score":f1_score(y_test,y_pred),
        "ROC AUC":roc_auc_score(y_test,y_prob),
        "Confusion Matrix":confusion_matrix(y_test,y_pred)
    }

    return metrics

#store the results
result=[]
result.append(evaluate_models(lr,"logistic_regression"))
result.append(evaluate_models(rf,"random_forest"))
result.append(evaluate_models(xgb,"xgboost"))


#converting into dataframe
result_df=pd.DataFrame(result)
print(result_df)

#save this evaluation report
result_df.to_csv("../Reports/model_comparison.csv",index=False)
print("Model comparison saved successfully")



#this tells me the importance of feature 
importance = pd.DataFrame({
    "Feature": x.columns,
    "Importance": rf.feature_importances_
}).sort_values(by="Importance", ascending=False)

importance.to_csv("../Reports/feature_importance.csv",index=False)
#days delinquent could be the reasin of leakage
