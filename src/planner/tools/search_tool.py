from crewai.tools import BaseTool
from exa_py import Exa
import os
from typing import Type, Optional, Dict, Any
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import asyncio

load_dotenv()

class SearchToolInput(BaseModel):
    query: str = Field(..., description="The query to search the web for")

class SearchTool(BaseTool):
    name: str = "Search Tool"
    description: str = "Search the web for information"
    args_schema: Type[BaseModel] = SearchToolInput

    def _run(self, query: str) -> str:
        return asyncio.run(self._arun(query=query))

    async def _arun(self, query: str) -> str:
        exa = Exa(api_key=os.getenv("EXA_API_KEY"))
        response = exa.search(
            query,
            numResults=10,
            )

        print(response)
        return response


if __name__ == "__main__":
    search_tool = SearchTool()
    print(search_tool.run("What is the weather in Tokyo?"))