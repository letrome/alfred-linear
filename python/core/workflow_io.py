import json
import logging
import os
import sys
from typing import Optional, Dict, Tuple

STATUS_SYMBOL_MAP = {
    "Backlog": "🔘",
    "Ready to Dev": "☑️",
    "Dev": "🟡",
    "Dev Review": "🟠",
    "Product Review": "🟠",
    "Feedback": "🗣️",
    "Ready to Go-Live": "🔵",
    "Completed": "✅",
    "Canceled": "❌",
    "Triage": "⚖️",
    "Default": "❓"
}


def _load_env_variables(key: str) -> Optional[str]:
    return os.path.expanduser(os.getenv(key, ''))


def get_api_key() -> Optional[str]:
    return _load_env_variables('api_key')


def get_team_key() -> Optional[str]:
    return _load_env_variables('team_key')


def get_ticket_number_arg() -> Tuple[bool, Optional[int]]:
    if len(sys.argv) <= 1:
        return True, None

    if sys.argv[1][:1] != '-':
        return False, None

    if len(sys.argv[1][1:]) <= 0:
        return True, None

    try:
        return True, int(sys.argv[1][1:])
    except ValueError:
        logging.error(f"ticket number value '{sys.argv[1][1:]}' is not valid")

    return False, None


def _format_title(ticket: json) -> str:
    return f"{ticket['identifier']} ➤ {ticket['title']}"


def _format_subtitle(ticket: json) -> str:
    state_symbol = STATUS_SYMBOL_MAP[ticket['state']['name']] if ticket['state'][
                                                                     'name'] in STATUS_SYMBOL_MAP.keys() else \
        STATUS_SYMBOL_MAP["Default"]
    state = state_symbol + ticket['state']['name']
    priority = "📶" + ticket['priorityLabel']
    if ticket['project'] is not None:
        project = "📂" + ticket['project']['name']
    else:
        project = ""

    return f"{state}{priority}{project}"


def format_no_result_response():
    return json.dumps({
        "items": [
            {
                "title": "No result"
            }
        ]
    })


def format_tickets(response: Optional[Dict]) -> str:
    formatted_tickets = []
    if response is not None:
        dct = response['data']['issues']['nodes']
        for ticket in dct:
            formatted_tickets.append({
                "title": f"{ticket['identifier']} ➤ {ticket['title']}",
                "subtitle": _format_subtitle(ticket),
                "arg": ticket['url']

            })

    if len(formatted_tickets) <= 0:
        return format_no_result_response()
    else:
        return json.dumps({"items": formatted_tickets})
