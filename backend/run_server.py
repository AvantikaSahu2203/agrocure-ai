import uvicorn
import sys
import os

# Add the current directory to sys.path to ensure 'app' is findable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import app

if __name__ == "__main__":
    print("Starting AgroCure AI Backend Server on Port 5000...")
    # Using Port 5000 to avoid conflicts on 8000
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
