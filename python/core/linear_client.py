import json
from typing import Dict

from .http_client import HttpClient
from .jinja_loader import JinjaLoader

MAX_TICKET_NUMBER_DIGITS = 4
LINEAR_URL = "https://api.linear.app/graphql"


class LinearClient:
    def __init__(self, api_key: str):
        self.http_client = HttpClient()
        self._headers = self._build_headers(api_key)

    @staticmethod
    def _build_headers(api_key: str) -> Dict:
        return {
            'Content-Type': "application/json",
            'Authorization': api_key
        }

    @staticmethod
    def _generate_and_filter_clause(search_field: int) -> str:
        if search_field is None:
            return ""
        and_filter_clause = f"{{number: {{eq: {search_field}}}}}"
        x = 1
        for i in range(len(str(search_field)), MAX_TICKET_NUMBER_DIGITS):
            x = x * 10
            min_value = search_field * x
            max_value = min_value + x - 1
            and_filter_clause += f",{{ and: [{{number: {{gte: {min_value}}}}}, {{number: {{lt: {max_value} }}}}]}},"

        return and_filter_clause

    def search_tickets(self, ticket_prefix: str, search_field: int) -> json:
        and_filter_clause = self._generate_and_filter_clause(search_field)
        payload = JinjaLoader().render_search_ticket_payload(ticket_prefix, and_filter_clause)

        return self.http_client.post(url=LINEAR_URL, headers=self._headers, payload={"query": payload})
