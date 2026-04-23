import requests
import sys

def verify_security(base_url):
    print(f"--- Verifying Security for: {base_url} ---")
    
    checks = [
        {
            "url": f"{base_url}/orchestrator/orchestrate",
            "data": {"crop_name": "Maize", "city": "Delhi", "state": "Delhi", "lat": 28.6, "lon": 77.2},
            "files": {"image": ("test.jpg", b"fake-image-content", "image/jpeg")}
        },
        {
            "url": f"{base_url}/advisory/get-advice",
            "json": {"lat": 28.6, "lon": 77.2, "crop_name": "Maize", "growth_stage": "Vegetative"}
        },
        {
            "url": f"{base_url}/disease-ai/analyze",
            "data": {"crop_name": "Maize"},
            "files": {"image": ("test.jpg", b"fake-image-content", "image/jpeg")}
        }
    ]
    
    for check in checks:
        url = check["url"]
        print(f"Checking {url} (Unauthenticated)...")
        try:
            if "files" in check:
                response = requests.post(url, data=check.get("data"), files=check["files"], timeout=5)
            else:
                response = requests.post(url, json=check.get("json"), timeout=5)
                
            if response.status_code in [401, 403]:
                print(f"  [PASS] Correcty rejected with {response.status_code}")
            else:
                print(f"  [FAIL] Security Bypass or Error! Status: {response.status_code}")
                print(f"  Response: {response.text}")
        except Exception as e:
            print(f"  [ERROR] {e}")

if __name__ == "__main__":
    verify_security("http://127.0.0.1:5000/api/v1")
