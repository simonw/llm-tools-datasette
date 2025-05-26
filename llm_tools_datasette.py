import llm
import httpx


class Datasette(llm.Toolbox):
    def __init__(self, url: str):
        self.url = url.rstrip("/")

    def query(self, sqlite_sql: str):
        "Execute provided SQLite SQL query - read-only, only use SELECT"
        params = {"sql": sqlite_sql, "_shape": "array"}
        # Construct the URL - append .json to the base URL
        query_url = f"{self.url}.json"

        try:
            with httpx.Client(follow_redirects=True) as client:
                response = client.get(query_url, params=params)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"HTTP error querying Datasette: {e}")
        except Exception as e:
            raise Exception(f"Error querying Datasette: {e}")

    def schema(self):
        "View the SQLite schema of the attached database"
        # Should call self.query() with "select group_concat(sql, ';') from sqlite_master"
        return self.query(
            "SELECT group_concat(sql, ';') FROM sqlite_master WHERE sql IS NOT NULL"
        )


@llm.hookimpl
def register_tools(register):
    register(Datasette)
