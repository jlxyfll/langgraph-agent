import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

DEFAULT_MODEL = os.getenv("LLM_MODEL", "gpt-5.4")

def get_llm(model: str = DEFAULT_MODEL) -> ChatOpenAI:
    return ChatOpenAI(
        model=model,
        base_url=os.environ["OPENAI_API_URL"],
        api_key=os.environ["OPENAI_API_KEY"],
    )

# 测试
if __name__ == "__main__":
    client = get_llm()
    print(f"Model: {client.model_name}, Base URL: {client.openai_api_base}")