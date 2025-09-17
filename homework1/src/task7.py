import requests

# Given a url it can get the status code of that url
def fetch_status_code(url):
    response = requests.get(url)
    return response.status_code

# Returns a list containing the a bunch of different github keys
def fetch_github_api_root():
    response = requests.get("https://api.github.com/")
    return list(response.json().keys())
