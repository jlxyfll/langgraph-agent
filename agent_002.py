from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    category: str


from llm import get_llm, DEFAULT_MODEL

llm = get_llm()


def chatbot(state: State) -> dict:
    reply = llm.invoke([
        SystemMessage("回复的开头先写 [分类:weather] 或 [分类:chat]"),
        *state["messages"],
    ])
    reply_text = reply.content
    category = reply_text.split("[分类:")[1].split("]")[0] if "[分类:" in reply_text else "chat"
    reply_text_clean = reply_text.split("] ", 1)[1] if "] " in reply_text else reply_text
    return {"messages": [AIMessage(content=reply_text_clean)], "category": category}

def weather_node(state: State) -> dict:
    return {"messages": [AIMessage(content="⛅ 我是天气助手，这里应该查天气")]}


def chat_node(state: State) -> dict:
    return {"messages": [AIMessage(content="💬 我是闲聊助手，这里应该聊日常")]}


def route_by_category(state: State) -> str:
    if state["category"] == "weather":
        return "weather"
    return "chat"


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_node("weather", weather_node)
graph_builder.add_node("chat", chat_node)

graph_builder.add_edge(START, "chatbot")
# graph_builder.add_edge("chatbot", END)
graph_builder.add_conditional_edges("chatbot", route_by_category, {"weather": "weather", "chat": "chat"})
graph_builder.add_edge("weather", END)
graph_builder.add_edge("chat", END)
graph = graph_builder.compile()


def main():
    # messages = [HumanMessage(content="用一句话介绍你自己")]
    messages = [HumanMessage(content="明天北京天气怎么样")]
    result = graph.invoke({"messages": messages})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
