from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, SystemMessage
from typing import TypedDict, Annotated
from langgraph.prebuilt import ToolNode, tools_condition
from app.chatbot.rag.retrieval import rag_search

llm = ChatOpenAI()
tools = [rag_search]
llm_with_tools = llm.bind_tools(tools)
tool_node = ToolNode(tools)


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


def build_graph():
    graph = StateGraph(ChatState)
    graph.add_node("chat_node", chat_node)
    graph.add_node("tools", tool_node)

    graph.add_edge(START, "chat_node")
    graph.add_conditional_edges("chat_node", tools_condition)
    graph.add_edge("tools", "chat_node")
    graph.add_edge("chat_node", END)

    return graph.compile()

chatbot = build_graph()