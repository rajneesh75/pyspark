import json
import numpy as np
import mlflow

hours_studied = np.array([1, 2, 3, 4, 5, 6], dtype=float)
exam_scores = np.array([45, 50, 60, 65, 70, 79], dtype=float)

learning_rate = 0.01
epochs = 1000
slope = 0.0
intercept = 0.0

number_of_samples = len(hours_studied)
mlflow.set_experiment("LinearRegressionScratch")

with mlflow.start_run():
    # Log parameters
    mlflow.log_param("learning_rate", learning_rate)
    mlflow.log_param("epochs", epochs)

    for epoch in range(epochs):

        # Predictions
        pred_exam_scores = slope * hours_studied + intercept
        print(f"pred_exam_scores {pred_exam_scores}")

        # Mean Squared Error
        loss = np.mean((exam_scores - pred_exam_scores) ** 2)
        print(f"loss {loss}")

        # Gradients
        dm = (-2 / number_of_samples) * np.sum(hours_studied * (exam_scores - pred_exam_scores))
        dc = (-2 / number_of_samples) * np.sum(exam_scores - pred_exam_scores)

        # Update weights
        slope = slope - learning_rate * dm
        intercept = intercept - learning_rate * dc

        # Log loss every 100 epochs
        if epoch % 100 == 0:
            print(f"Epoch {epoch:4d} Loss = {loss:.2f}")
            mlflow.log_metric("loss", loss, step=epoch)

    print("\nTraining Finished")
    print(f"Slope = {slope:.3f}")
    print(f"Intercept = {intercept:.3f}")

    # Log final values
    mlflow.log_metric("final_loss", loss)
    mlflow.log_param("slope", slope)
    mlflow.log_param("intercept", intercept)

print("Creating model json file")

model = {
    "slope": float(slope),
    "intercept": float(intercept)
}

with open("LinearRegressionScratch.json", "w") as f:
    json.dump(model, f, indent=4)

print("Model trained. Now prediction")
hours_studied = 7
predicted_score = slope * hours_studied + intercept
print(f" hours_studied {hours_studied} predicted_score {predicted_score}")