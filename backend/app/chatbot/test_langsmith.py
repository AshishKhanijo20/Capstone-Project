from dotenv import load_dotenv
load_dotenv()

import os
from langsmith import Client

# Print env vars
print("\n" + "="*60)
print("ENVIRONMENT VARIABLES:")
print(f"LANGCHAIN_TRACING_V2: {os.getenv('LANGCHAIN_TRACING_V2')}")
print(f"LANGCHAIN_API_KEY: {os.getenv('LANGCHAIN_API_KEY')[:20]}...")
print(f"LANGCHAIN_PROJECT: {os.getenv('LANGCHAIN_PROJECT')}")
print(f"LANGCHAIN_ENDPOINT: {os.getenv('LANGCHAIN_ENDPOINT')}")
print("="*60 + "\n")

# Test connection
try:
    client = Client()
    print("✅ LangSmith connection successful!")
    print(f"📊 Connected to project: {os.getenv('LANGCHAIN_PROJECT')}")
except Exception as e:
    print(f"❌ LangSmith connection failed: {e}")
    exit(1)

# Test a simple trace
print("\n🧪 Sending test trace...")
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
response = llm.invoke("Say 'LangSmith is working!'")
print(f"✅ Response: {response.content}")
print("\n👉 Check your traces at: https://smith.langchain.com")
print(f"👉 Project: {os.getenv('LANGCHAIN_PROJECT')}")