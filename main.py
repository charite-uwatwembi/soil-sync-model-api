from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
    
app = FastAPI()
    
    # Load your trained model and any other required files (like encoders)
    # Make sure the 'model.joblib' file is in the same folder
try:
        model = joblib.load('soil_fertility_rf_model.joblib')
except FileNotFoundError:
        model = None # Handle case where model is not found
    
    # Define the structure of the input data from your frontend
class SoilData(BaseModel):
        phosphorus: float
        potassium: float
        nitrogen: float
        organicCarbon: float
        cationExchange: float
        sandPercent: float
        clayPercent: float
        siltPercent: float
        rainfall: float
        elevation: float
        cropType: str
    
@app.get("/")
def read_root():
        return {"message": "SoilSync ML Model API is running!"}
    
@app.post("/predict")
def predict(data: SoilData):
        if model is None:
            return {"error": "Model not loaded. Check server logs."}
    
        # IMPORTANT: Convert the incoming data into the exact format
        # your model was trained on. This is a sample DataFrame creation.
        # You might need to adjust column names or order.
        input_df = pd.DataFrame([data.dict()])
    
        # If your model needs specific column names or order, define them here
        # E.g., model_columns = ['N', 'P', 'K', 'temperature', 'humidity', ...]
        # input_df = input_df[model_columns]
    
        # Make a prediction
        prediction_result = model.predict(input_df)
    
        # IMPORTANT: Format the prediction into the response your frontend expects.
        # This is just an example. You must adjust it to match your model's output.
        # For example, if your model returns just "Urea", you build the rest.
        recommendation = {
            "fertilizer": prediction_result[0], # Assuming the model returns the fertilizer name
            "rate": 150,  # Example static value
            "confidence": 92.5, # Example static value
            "expected_yield_increase": 18 # Example static value
        }
    
        return recommendation