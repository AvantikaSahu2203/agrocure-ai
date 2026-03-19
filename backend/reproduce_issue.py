import requests

url = "http://localhost:8000/api/v1/disease-ai/analyze"

# Create a dummy image file
with open("test_image.jpg", "wb") as f:
    f.write(b"fake image data")

files = {
    "image": ("test_image.jpg", open("test_image.jpg", "rb"), "image/jpeg")
}
data = {
    "crop_name": "Tomato",
    "growth_stage": "Vegetative"
}

try:
    response = requests.post(url, files=files, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
