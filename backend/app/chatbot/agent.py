from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, SystemMessage
from typing import TypedDict, Annotated
from langgraph.prebuilt import ToolNode, tools_condition
from app.chatbot.rag.retrieval import rag_search
from app.chatbot.tools import refresh_ticket_context
import os


print("="*50)
print(" LangSmith Configuration:")
print(f"   Tracing: {os.getenv('LANGCHAIN_TRACING_V2')}")
print(f"   Project: {os.getenv('LANGCHAIN_PROJECT')}")
print(f"   API Key: {os.getenv('LANGCHAIN_API_KEY')[:15]}..." if os.getenv('LANGCHAIN_API_KEY') else "   API Key: NOT SET")
print("="*50)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [rag_search, refresh_ticket_context]
llm_with_tools = llm.bind_tools(tools)
tool_node = ToolNode(tools)


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState):
    rag_guardrail = SystemMessage(
        content=(
            "IMPORTANT:\n"
            "1. For troubleshooting questions, use the rag_search tool to find solutions.\n"
            "2. If the user mentions they updated the ticket or you need current ticket info, "
            "use the refresh_ticket_context tool.\n"
            "3. Always base your responses on tool results, not prior knowledge.\n\n"
            "If no relevant information is found, say: "
            "'I don't have enough information to answer this.'"
        )
    )
    messages = [rag_guardrail] + state["messages"]
    return {"messages": [llm_with_tools.invoke(messages)]}


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