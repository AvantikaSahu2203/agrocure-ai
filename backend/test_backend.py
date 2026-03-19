import requests
import os

# Create a dummy image
with open("test_image.jpg", "wb") as f:
    f.write(os.urandom(1024))

url = "http://localhost:8000/api/v1/orchestrator/full-analysis"

data = {
    "crop_name": "Tomato",
    "city": "Pune",
    "state": "Maharashtra",
    "lat": 18.5204,
    "lon": 73.8567,
    "humidity": 60.0,
    "temperature": 25.0
}

files = {
    "image": ("test_image.jpg", open("test_image.jpg", "rb"), "image/jpeg")
}

try:
    print(f"Sending request to {url}...")
    response = requests.post(url, data=data, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Request Failed: {e}")
