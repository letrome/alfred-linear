from core.workflow_io import get_api_key, get_team_key, get_ticket_number_arg, format_tickets, format_no_result_response
from core.linear_client import LinearClient


def main():
    api_key = get_api_key()
    team_key = get_team_key()
    is_valid, search_ticket_number = get_ticket_number_arg()

    if not is_valid:
        output = format_no_result_response()
    else:
        response = LinearClient(api_key).search_tickets(team_key, search_ticket_number)
        output = format_tickets(response)

    print(output)
    exit(0)


if __name__ == "__main__":
    main()
