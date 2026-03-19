import requests

url = "http://localhost:8000/api/v1/orchestrator/full-analysis"

# Use any small image for testing
with open("backend/test_image.jpg", "rb") as f:
    files = {"image": ("test.jpg", f, "image/jpeg")}
    data = {
        "crop_name": "Tomato",
        "city": "Pune",
        "state": "Maharashtra",
        "lat": "18.5204",
        "lon": "73.8567",
        "language": "en"
    }
    
    try:
        response = requests.post(url, files=files, data=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")
