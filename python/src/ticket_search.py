import json
import os
import sys
from typing import Optional, Dict

import requests
import logging

MAX_TICKET_NUMBER_DIGITS = 4


def parse_env_variables():
    token = os.path.expanduser(os.getenv('api_key', ''))
    ticket_prefix = os.path.expanduser(os.getenv('team_key', ''))
    return token, ticket_prefix


def parse_argument() -> Optional[int]:
    if len(sys.argv) > 1 and sys.argv[1][:1] == '-':
        ticket_number = sys.argv[1][1:]

        try:
            return int(ticket_number)
        except ValueError:
            logging.error(f"ticket number value '{ticket_number}' is not valid")


def generate_and_filter_clause(search_field: int) -> str:
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


def search_tickets(ticket_prefix: str, search_field: int, api_key: str) -> Optional[str]:
    team_id = '19a2a5d9-1460-4391-ba36-71389e7f3021'
    payload = f'''
    query Team {{
    team(id: "{team_id}") {{name
    issues(
            orderBy: updatedAt
            filter: {{
                and: [
                    {{team: {{ key: {{eq: "{ticket_prefix}"}}}}}}
                    {{or: [
                        {generate_and_filter_clause(search_field)}
                    ]}},
                ]
            }}
        ) {{
            nodes {{
                title
                identifier
                url
                number
                priorityLabel
                                state {{
                    name
                }}
                                project {{
                    name
                }}
            }}
        }}
    }}
}}
    '''
    headers = {
        'Content-Type': "application/json",
        'Authorization': api_key
    }

    response = requests.post("https://api.linear.app/graphql", json={"query": payload}, headers=headers)
    code = response.status_code
    if code == 200:
        return response.json()
    else:
        return None


def format_tickets(response: Optional[Dict]) -> json:
    formatted_tickets = []
    if response is not None:
        dct = response['data']['team']['issues']['nodes']
        for ticket in dct:
            formatted_tickets.append({
                "title": f"{ticket['identifier']} ➤ {ticket['title']}",
                "subtitle": f"🔘{ticket['state']['name']}📶{ticket['priorityLabel']}{"📂"+ticket['project']['name'] if ticket['project'] is not None else ""}",
                "arg": ticket['url']

            })

    if len(formatted_tickets) <= 0:
        formatted_tickets = [
            {
                "title": "No result"
             }
        ]

    return formatted_tickets


def main():
    api_key, ticket_prefix = parse_env_variables()
    search_field = parse_argument()

    response = search_tickets(ticket_prefix, search_field, api_key)

    output = format_tickets(response)
    print(json.dumps({"items": output}))
    exit(0)


if __name__ == "__main__":
    main()
