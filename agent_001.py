from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


from llm import get_llm, DEFAULT_MODEL

llm = get_llm()


def chatbot(state: State) -> dict:
    reply = llm.invoke(state["messages"])
    return {"messages": [reply]}


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()


def main():
    messages = [HumanMessage(content="用一句话介绍你自己")]
    result = graph.invoke({"messages": messages})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
