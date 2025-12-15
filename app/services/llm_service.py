from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage


class LLMService:
    def __init__(self):
        self.llm = ChatOllama(
            model="llama3",
            base_url="http://localhost:11434",
            temperature=0.3,
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
        
        print(response)

        return response.content.strip()
