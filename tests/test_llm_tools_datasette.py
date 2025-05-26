import llm
import json
from llm_tools_datasette import Datasette


def test_tool(httpx_mock):
    httpx_mock.add_response(
        url="https://example.com/datasette.json?sql=select+1&_shape=array",
        json={"rows": [{"1": "1"}]},
    )
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
    assert tool_results == [
        {
            "name": "Datasette_query",
            "output": '{"rows": [{"1": "1"}]}',
            "tool_call_id": None,
        }
    ]
