import llm
import json
from llm_tools_datasette import Datasette


def test_tool(httpx2_mock):
    httpx2_mock.get(
        "https://example.com/datasette.json",
        params={"sql": "select 1", "_shape": "array"},
    ).respond(json={"rows": [{"1": "1"}]})
    model = llm.get_model("echo")
    chain_response = model.chain(
        json.dumps(
            {
                "tool_calls": [
                    {
                        "name": "Datasette_query",
                        "arguments": {"sqlite_sql": "select 1"},
                    }
                ]
            }
        ),
        tools=[Datasette("https://example.com/datasette")],
    )
    responses = list(chain_response.responses())
    tool_results = json.loads(responses[-1].text())["tool_results"]
    assert [(r["name"], r["output"]) for r in tool_results] == [
        ("Datasette_query", '{"rows": [{"1": "1"}]}')
    ]
