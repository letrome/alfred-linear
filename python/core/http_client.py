import json
from typing import Optional, Dict

import requests


class HttpClient:
    def __init__(self):
        self._requests = requests

    @staticmethod
    def post(url, headers: Dict, payload: json) -> Optional[json]:
        response = requests.post(url=url, headers=headers, json=payload)
        code = response.status_code
        if code == 200:
            return response.json()
        else:
            return None
