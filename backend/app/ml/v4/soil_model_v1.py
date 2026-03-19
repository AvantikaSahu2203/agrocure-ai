import lightgbm as lgb
import joblib
import numpy as np
import os
from sklearn.multioutput import MultiOutputClassifier

def train_mock_soil_model():
    """
    Trains a LightGBM model on synthetic soil parameter data.
    Features: [pH, N, P, K]
    Outputs: Multi-label [N_def, P_def, K_def, Fe_def, Mg_def, RootRot, Fusarium, DampingOff, Clubroot]
    """
    # Synthetic Data Generation
    X = []
    y = []
    
    for _ in range(1200):
        ph = np.random.uniform(4.0, 9.0)
        n = np.random.uniform(0, 150)
        p = np.random.uniform(0, 80)
        k = np.random.uniform(0, 100)
        
        # Labels: [Deficiencies (5), Diseases (4)]
        labels = [0] * 9
        
        # Deficiencies
        if n < 35: labels[0] = 1 # Nitrogen
        if p < 20: labels[1] = 1 # Phosphorus
        if k < 25: labels[2] = 1 # Potassium
        if ph > 7.8: labels[3] = 1 # Iron
        if ph < 5.2: labels[4] = 1 # Magnesium
        
        # Diseases
        if ph < 5.0: labels[8] = 1 # Clubroot
        if ph > 6.0 and n > 120: labels[6] = 1 # Fusarium Wilt
        if ph > 5.5 and ph < 7.0 and n < 50: labels[5] = 1 # Root Rot (simplified)
        
        X.append([ph, n, p, k])
        y.append(labels)
        
    X = np.array(X)
    y = np.array(y)
    
    # Using MultiOutputClassifier to handle multi-label with LightGBM
    base_model = lgb.LGBMClassifier(n_estimators=100, random_state=42)
    model = MultiOutputClassifier(base_model)
    model.fit(X, y)
    
    os.makedirs("app/ml/v4", exist_ok=True)
    model_path = "app/ml/v4/soil_model_lgbm.joblib"
    joblib.dump(model, model_path)
    print(f"Soil Analysis Model saved to {model_path}")

if __name__ == "__main__":
    train_mock_soil_model()
