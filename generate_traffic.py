import requests
import time
import random
import json
from concurrent.futures import ThreadPoolExecutor

def normal_traffic():
    """Generate normal traffic"""
    urls = [
        'http://localhost:5000/',
        'http://localhost:5000/api/data'
    ]
    
    for _ in range(100):
        url = random.choice(urls)
        try:
            response = requests.get(url)
            print(f"Normal request to {url}: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(random.uniform(0.5, 2))

def suspicious_traffic():
    """Generate suspicious traffic"""
    # SQL injection attempts
    sqli_payloads = [
        "' OR '1'='1",
        "'; DROP TABLE users; --",
        "' UNION SELECT * FROM users --"
    ]
    
    for payload in sqli_payloads:
        try:
            response = requests.post('http://localhost:5000/login', 
                                   json={'username': payload, 'password': 'test'})
            print(f"Suspicious request: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(1)

def brute_force():
    """Simulate brute force attack"""
    for i in range(50):
        try:
            response = requests.post('http://localhost:5000/login',
                                   json={'username': 'admin', 'password': f'password{i}'})
            print(f"Brute force attempt {i}: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(0.5)

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(normal_traffic)
        executor.submit(suspicious_traffic)
        executor.submit(brute_force)
