import numpy as np
import mlflow.sklearn
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


mlflow.sklearn.autolog()

# ------------------------------------
# Create training data
# ------------------------------------
hours_studied = np.array([1, 2, 3, 4, 5, 6], dtype=float)

exam_scores = np.array([45, 50, 60, 65, 70, 80], dtype=float)

# sklearn expects 2D input features
X = hours_studied.reshape(-1, 1)

y = exam_scores
mlflow.set_experiment("SklearnLinearRegression")

with mlflow.start_run():
    # Create model
    model = LinearRegression()

    # Train model
    model.fit(X, y)

    # Predictions
    predictions = model.predict(X)

    # Calculate metrics
    mse = mean_squared_error(
        y,
        predictions
    )

    r2 = r2_score(
        y,
        predictions
    )

    print("Training completed")
    print("------------------")
    print(f"Slope      : {model.coef_[0]}")
    print(f"Intercept  : {model.intercept_}")
    print(f"MSE        : {mse}")
    print(f"R2 Score   : {r2}")

print("Done")
