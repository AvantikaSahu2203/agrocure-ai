import requests
import json

def test_full_analysis_api():
    url = "http://localhost:8000/api/v1/orchestrator/full-analysis"
    
    # Get a token first
    login_url = "http://localhost:8000/api/v1/login/access-token"
    # Assuming farmer@agrocure.com / password
    login_data = {"username": "farmer@agrocure.com", "password": "password"}
    login_res = requests.post(login_url, data=login_data)
    if login_res.status_code != 200:
        print(f"Login failed: {login_res.text}")
        return
    
    token = login_res.json()["access_token"]
    headers = {
        "Authorization": f"Bearer {token}",
        "Origin": "http://localhost:3000"
    }
    
    # Prepare files and data
    files = {
        "image": ("test.jpg", open("test_image.jpg", "rb"), "image/jpeg")
    }
    data = {
        "crop_name": "Tomato",
        "city": "Pune",
        "state": "Maharashtra",
        "lat": "18.5204",
        "lon": "73.8567"
    }
    
    print("Sending Analysis Request...")
    res = requests.post(url, headers=headers, files=files, data=data)
    
    print(f"Status Code: {res.status_code}")
    print(f"Response Headers: {res.headers}")
    try:
        print(f"Response: {json.dumps(res.json(), indent=2)}")
    except:
        print(f"Response (text): {res.text}")

if __name__ == "__main__":
    test_full_analysis_api()
