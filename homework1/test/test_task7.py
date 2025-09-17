import sys
import os
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from task7 import fetch_status_code, fetch_github_api_root

def test_fetch_status_code():
    code = fetch_status_code("https://www.google.com")
    assert isinstance(code, int)
    assert 100 <= code < 600  # All possible HTTP status codes

def test_fetch_github_api_root():
    keys = fetch_github_api_root()
    assert isinstance(keys, list)
    # The GitHub API root always includes at least these keys
    for key in ["current_user_url", "current_user_authorizations_html_url"]:
        assert key in keys
