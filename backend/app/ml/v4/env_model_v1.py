from sklearn.ensemble import RandomForestClassifier
import joblib
import numpy as np
import os

def train_mock_env_model():
    """
    Trains a base Random Forest model on synthetic agro-environmental data.
    This provides a starting point that can be refined with real dataset.
    """
    # Features: [Temperature, Humidity, Rainfall, Soil Moisture]
    # Label: 0 (Low Risk), 1 (High Risk)
    
    # Synthetic Data Generation
    X = []
    y = []
    
    for _ in range(1000):
        temp = np.random.uniform(10, 45)
        hum = np.random.uniform(20, 100)
        rain = np.random.uniform(0, 50)
        soil = np.random.uniform(0.1, 0.6)
        
        # Basic logic for synthetic 'High Risk' (fungal-like scenario)
        risk = 0
        if hum > 80 and temp > 15 and temp < 35:
            risk = 1
        if rain > 10 and hum > 70:
            risk = 1
        if soil > 0.5 and hum > 60:
            risk = 1
            
        X.append([temp, hum, rain, soil])
        y.append(risk)
        
    X = np.array(X)
    y = np.array(y)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    os.makedirs("app/ml/v4", exist_ok=True)
    model_path = "app/ml/v4/env_risk_rf.joblib"
    joblib.dump(model, model_path)
    print(f"Environmental Risk Model saved to {model_path}")

if __name__ == "__main__":
    train_mock_env_model()
