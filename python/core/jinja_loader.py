from jinja2 import Environment, select_autoescape, FileSystemLoader

TEMPLATE_FILE_PATH = "../template"
SEARCH_TICKET_PATH = "query_issues_template.jinja"


class JinjaLoader:
    def __init__(self):
        self._env = Environment(
            loader=FileSystemLoader("./python/template"),
            autoescape=select_autoescape()
        )

    def render_search_ticket_payload(self, team_key: str, and_filter_clause: str) -> str:
        template = self._env.get_template("query_issues_template.jinja")
        return template.render(
            TEAM_KEY=team_key,
            AND_FILTER_CLAUSE=and_filter_clause
        )
