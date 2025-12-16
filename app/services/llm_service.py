# from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate



class LLMService:
    def __init__(self):
        self.llm = ChatOllama(
            model="llama3",
            base_url="http://localhost:11434",
            temperature=0.5,
        )

    async def generate_summary(self, title: str, author: str, content: str) -> str:
        template = PromptTemplate(
            template="""
                Generate a short, clear summary for the following book.
                Use the format: "Title: summary" without extra spaces. 
                {Title}
                {Author}
                {Content}
                """,
            input_variables=['title','author','content']
        )
        chain = template | self.llm
        result = chain.invoke({'Title':title,"Author":author,"Content":content})
        return result.content.strip()
       