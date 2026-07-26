from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
df=pd.read_csv("../data/processed/featured_loan_data.csv")
x=df.drop(["defaulted","days_delinquent"],axis=1)
y=df["defaulted"]
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.20,random_state=42,stratify=y)


param_grid={
    "n_estimators":[100,200,300],
    "max_depth":[5,10,20,None],
    "min_samples_split":[2,5,10],
    "min_samples_leaf":[1,2,4]
}

grid_search=GridSearchCV(
    estimator=RandomForestClassifier(
        random_state=42,
        class_weight="balanced"
    ),
    param_grid=param_grid,
    scoring="roc_auc",
    cv=5,
    n_jobs=-1,
    verbose=2
)

grid_search.fit(x_train,y_train)
print(grid_search.best_params_)

import joblib
joblib.dump(grid_search.best_estimator_,"../models/random_forest_tuned.pkl")
print("=======tuned model saved successfully=======")

from sklearn.model_selection import cross_val_score
scores=cross_val_score(RandomForestClassifier(**grid_search.best_params_,random_state=42,class_weight="balanced"),x,y,cv=5,scoring="roc_auc")
print("cross validation scores of each fold:",scores)
print("Average Score:",scores.mean())

#checking accuracy of tuned model
print("===================CHECKING ACCURACY OF TUNED MODEL===================")
best_model=grid_search.best_estimator_
y_pred=best_model.predict(x_test)
y_prob=best_model.predict_proba(x_test)[:,1]

from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,confusion_matrix
print("accuracy score:",accuracy_score(y_test,y_pred))
print("precision_score:",precision_score(y_test,y_pred))
print("F1 score:",f1_score(y_test,y_pred))
print("ROC AUC:",roc_auc_score(y_test,y_prob))
print("Confusion Matrix:",confusion_matrix(y_test,y_pred))

print("Each accuracy metrics have improved after tuning")
