import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
# from langgraph.prebuilt import create_react_agent
from langchain.agents import create_agent
from llm import get_llm, DEFAULT_MODEL

llm = get_llm()


# 创建工具
@tool
def multiply(a: int, b: int) -> int:
    """计算两个整数的乘积"""
    return a * b


# 创建agent
tools = [multiply]
# agent = create_react_agent(llm, tools)
agent = create_agent(llm, tools)


# 测试
def main():
    result = agent.invoke({"messages": [("user", "计算 1234 × 5678")]})
    for m in result["messages"]:
        role = type(m).__name__
        content = m.content if m.content else "[tool call]"
        print(f"{role}: {content}")

if __name__ == "__main__":
    main()