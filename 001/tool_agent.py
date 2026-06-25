from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from llm import get_llm, DEFAULT_MODEL
from tools import multiply_tool, tools_map


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


llm = get_llm()

llm_with_tools = llm.bind_tools([multiply_tool])
def chatbot(state: State) -> dict:
    reply = llm_with_tools.invoke(state["messages"])
    return {"messages": [reply]}


# def chatbot(state: State) -> dict:
#     reply = llm.bind_tools([multiply_tool]).invoke(state["messages"])
#     return {"messages": [reply]}


# intent_map = {"weather": [weather_tool, location_tool], "math": [multiply_tool]}
#
# def chatbot(state):
#     intent = classify_intent(state["messages"])
#
#     tools = intent_map[intent]
#
#     reply = llm.bind_tools(tools).invoke(state["messages"])
#
#     return {"messages": [reply]}


def tool_executor(state: State) -> dict:
    last_msg = state["messages"][-1]
    results = []
    for tc in last_msg.tool_calls:
        fn = tools_map[tc["name"]]
        result = fn(**tc["args"])
        results.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))

    return {"messages": results}


def should_continue(state: State) -> str:
    if state["messages"][-1].tool_calls:
        return "tools"
    return END


builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_node("tools", tool_executor)

builder.add_edge(START, "chatbot")
builder.add_conditional_edges("chatbot", should_continue, {"tools": "tools", END: END})
builder.add_edge("tools", "chatbot")

graph = builder.compile()


def main():
    messages = [HumanMessage(content="计算 1234 × 5678")]

    # for msg, metadata in graph.stream({"messages": messages}, stream_mode="messages"):
    #     node = metadata.get("langgraph_node", "")
    #     content = msg.content if msg.content else ""
    #     if content:
    #         print(f"[{node}] {content}", end="", flush=True)

    for step in graph.stream({"messages": messages}):
        for node_name, output in step.items():
            print(f"\n== {node_name} ==")
            if "messages" in output:
                for m in output["messages"]:
                    role = type(m).__name__
                    content = m.content if m.content else "[tool call]"
                    print(f"{role}: {content}")

    # result = graph.invoke({"messages": messages})
    # for m in result["messages"]:
    #     role = type(m).__name__
    #     content = m.content if m.content else "[tool call]"
    #     print(f"{role}: {content}")


if __name__ == "__main__":
    main()
