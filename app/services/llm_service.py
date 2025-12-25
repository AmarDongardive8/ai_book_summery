# from langchain_community.chat_models import ChatOllama
# from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from app.config import settings
# from langchain
import os

load_dotenv()

class LLMService:
    def __init__(self):
        
        # self.llm = ChatOpenAI(model="gpt-4o-mini",temperature=1.5)
        self.llm = ChatOpenAI(model=settings.OPENAI_MODEL,max_output_tokens=settings.OPENAI_MAX_TOKENS,temperature=1.5)
        
        self.template = PromptTemplate(
            template="""
                Generate a short, clear summary for the following book.
                Use the format: "Title: summary" without extra spaces. 
                {Title}
                {Author}
                {Content} 
                """,
            input_variables=['title','author','content']
        )

    async def generate_summary(self, title: str, author: str, content: str) -> str:
        chain = self.template | self.llm 
        result = chain.invoke({'Title':title,"Author":author,"Content":content})
        return result.content.strip()
    

class LLMRecomndationService(LLMService):
    def __init__(self):
            super().__init__()
            self.template = PromptTemplate(
                template="""
                You are an AI assistant for a technical book recommendation system.

                Available book genres in the database are:
                {all_genres_str}

                Based on the user's preference, select the MOST RELEVANT genre(s)
                from the above list.

                User preference:
                {preference}

                Rules:
                - Choose only from the provided genres
                - Return 1 to 2 genres
                - Return as a comma-separated list
                - Do NOT add explanations or extra text
            """,
                input_variables=['preference','all_genres_str']
            )

    async def extract_genre(self, preference: str,all_genres_str: str) -> str:
        chain = self.template | self.llm
        result = chain.invoke({'preference':preference,"all_genres_str":all_genres_str})
        return result.content.strip()

       