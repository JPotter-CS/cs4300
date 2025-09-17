import requests

def fetch_status_code(url):
    response = requests.get(url)
    return response.status_code

def fetch_github_api_root():
    response = requests.get("https://api.github.com/")
    return list(response.json().keys())
