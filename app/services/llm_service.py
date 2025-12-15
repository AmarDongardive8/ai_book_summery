# from langchain_openai import ChatOpenAI
# # from langchain.schema import HumanMessage
# from langchain_core.messages import HumanMessage


# OPENROUTER_API_KEY = "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"

# class LLMService:
#     def __init__(self):
#         self.llm = ChatOpenAI(
#             openai_api_key=OPENROUTER_API_KEY,
#             openai_api_base="https://openrouter.ai/api/v1",
#             model="meta-llama/llama-3-8b-instruct",
#             temperature=0.3
#         )

#     async def generate_summary(self, title: str, author: str, content: str) -> str:
#         prompt = f"""
#         Generate a short, clear summary for the following book.

#         Title: {title}
#         Author: {author}
#         Content: {content}
#         """

#         response = await self.llm.invoke([
#             [HumanMessage(content=prompt)]
#         ])

#         print(response)

#         return response.generations[0][0].text.strip()


import os
import certifi
import httpx
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_KEY = "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"


class LLMService:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            model="meta-llama/llama-3-8b-instruct",
            temperature=0.3,
            default_headers={
                "HTTP-Referer": "http://localhost:8000",  # required
                "X-Title": "Book Summary App"              # required
            },
            http_client=httpx.AsyncClient(
                verify=certifi.where()
            )
        )

    async def generate_summary(self, title: str, author: str, content: str) -> str:
        prompt = f"""
        Generate a short, clear summary for the following book.

        Title: {title}
        Author: {author}
        Content: {content}
        """

        response = await self.llm.ainvoke(
            [HumanMessage(content=prompt)]
        )

        return response.content.strip()


