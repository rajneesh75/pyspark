import mlflow
import numpy as np

model_uri = "runs:/1a6b0112699948989347ede0e8451a02/model"
loaded_model = mlflow.pyfunc.load_model(model_uri)

input_data = np.array([[8]], dtype=float)
prediction = loaded_model.predict(input_data)

print(prediction)