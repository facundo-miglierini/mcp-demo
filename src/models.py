from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

load_dotenv()

model = AzureChatOpenAI(
    azure_endpoint="https://snoop-gpt.openai.azure.com/",
    azure_deployment="snoop-gpt-4o-mini-max",
    api_version="2024-08-01-preview"
)
