from langchain_core.tools import tool
from langchain_core.messages import ToolMessage, AIMessage

from pydantic import BaseModel, SecretStr
import aiohttp
import os

SERPAPI_API_KEY = SecretStr(os.environ["SERPAPI_API_KEY"])

class Article(BaseModel):
    title: str
    source: str
    link: str
    snippet: str

    @classmethod
    def from_seprapi_results(cls, result: dict) -> "Article":
        return cls(
            title=result["title"],
            source=result["source"],
            link=result["link"],
            snippet=result["snippet"]
        )


# Tools definition
# note: we define all tools as async to simplify later code, but only the serpapi
# tool is actually async
@tool
async def add(x: float, y: float) -> float:
    """Add 'x' and 'y'."""
    return x + y

@tool
async def multiply(x: float, y: float) -> float:
    """Multiply 'x' and 'y'."""
    return x * y

@tool
async def exponentiate(x: float, y: float) -> float:
    """Raise 'x' to the power of 'y'."""
    return x ** y

@tool
async def subtract(x: float, y: float) -> float:
    """Subtract 'x' from 'y'."""
    return y - x

@tool
async def serpapi(query: str) -> list[Article]:
    """Search the web for information related to the query."""
    params = {
        "api_key": SERPAPI_API_KEY.get_secret_value(),
        "engine": "google",
        "q": query
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://serpapi.com/search",
            params=params
        ) as response:
            results = await response.json()
        return [Article.from_seprapi_results(result) for result in results["organic_results"]]

@tool
async def final_answer(answer: str, tools_used: list[str]) -> dict[str, str | list[str]]:
    """Use this tool to provide a final answer to the user."""
    return {"answer": answer, "tools_used": tools_used}


async def execute_tool(tool_call: AIMessage) -> ToolMessage:
    """Execute a tool call."""
    tools = [add, subtract, multiply, exponentiate, final_answer, serpapi]
# note when we have sync tools we use tool.func, when async we use tool.coroutine
    name2tool = {tool.name: tool.coroutine for tool in tools}
    tool_name = tool_call.tool_calls[0]["name"]
    tool_args = tool_call.tool_calls[0]["args"]
    tool_out = await name2tool[tool_name](**tool_args)
    return ToolMessage(
        content=f"{tool_out}",
        tool_call_id=tool_call.tool_calls[0]["id"]
    )