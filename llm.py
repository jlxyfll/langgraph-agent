import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_llm(model: str = "z-ai/glm-5.1") -> OpenAI:
    return OpenAI(
        base_url=os.environ["OPENAI_API_URL"],
        api_key=os.environ["OPENAI_API_KEY"],
    )

# 测试
if __name__ == "__main__":
    client = get_llm()
    print(client.models.list().data[0].id)