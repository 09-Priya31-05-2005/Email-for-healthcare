import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

api_key = os.getenv("api_key")
base_url = os.getenv("base_url")
model = os.getenv("model_name")

llm = ChatOpenAI(
    model=model,
    api_key=api_key,
    base_url=base_url,
    temperature=0
)

response = llm.invoke(
    "Explain in one sentence what a patient complaint management system does."
)

print(response.content)