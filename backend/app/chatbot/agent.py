from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, SystemMessage
from typing import TypedDict, Annotated
from langgraph.prebuilt import ToolNode, tools_condition
from app.chatbot.rag.retrieval import rag_search
from app.chatbot.tools import refresh_ticket_context, suggest_ticket_status_update
import os


print("="*50)
print(" LangSmith Configuration:")
print(f"   Tracing: {os.getenv('LANGCHAIN_TRACING_V2')}")
print(f"   Project: {os.getenv('LANGCHAIN_PROJECT')}")
print(f"   API Key: {os.getenv('LANGCHAIN_API_KEY')[:15]}..." if os.getenv('LANGCHAIN_API_KEY') else "   API Key: NOT SET")
print("="*50)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [rag_search, refresh_ticket_context, suggest_ticket_status_update]
llm_with_tools = llm.bind_tools(tools)
tool_node = ToolNode(tools)


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState):
    rag_guardrail = SystemMessage(
        content=(
            "CRITICAL RULES - YOU MUST FOLLOW THESE:\n\n"
            
            "1. TROUBLESHOOTING:\n"
            "   - For technical questions, ALWAYS use rag_search tool first\n"
            "   - Base answers ONLY on rag_search results\n\n"
            
            "2. TICKET STATUS:\n"
            "   - If user mentions ticket updates, use refresh_ticket_context tool\n"
            "   - NEVER assume ticket information without checking\n\n"
            
            "3. RESOLVING TICKETS - EXTREMELY IMPORTANT:\n"
            "   - When user confirms issue is resolved, call suggest_ticket_status_update tool\n"
            "   - After the tool runs, YOU MUST copy its EXACT output word-for-word\n"
            "   - DO NOT reformat, summarize, or prettify the tool output\n"
            "   - DO NOT convert JSON to markdown or bullet points\n"
            "   - The tool output contains special markers that trigger UI buttons\n"
            "   - Example: If tool returns 'TICKET_UPDATE_SUGGESTION: {...}', return that EXACT text\n\n"
            
            "4. IMPORTANT:\n"
            "   - You cannot directly update tickets\n"
            "   - You can only SUGGEST updates via the tool\n"
            "   - The user must confirm via UI buttons\n\n"
            
            "If you don't have information, say: 'I don't have enough information to answer this.'"
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


