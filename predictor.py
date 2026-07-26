import joblib
model = joblib.load("models/random_forest_tuned.pkl")

def predict(customer):
    prediction=model.predict(customer)[0]
    probability=model.predict_proba(customer)[0][1]
    return prediction, probability
