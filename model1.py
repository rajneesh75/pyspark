import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib

df = pd.DataFrame({
    "age": [25, 45, 52, 23, 40],
    "income": [40000, 80000, 90000, 35000, 70000],
    "city": [0, 1, 1, 0, 1],   # already encoded
    "label": [0, 1, 1, 0, 1]
})

X = df[["age", "income", "city"]]
y = df["label"]

model = LogisticRegression()
model.fit(X, y)

joblib.dump(model, "churn_model.pkl")