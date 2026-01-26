from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.session import init_db
from app.routers import tickets, ticket_chat
from dotenv import load_dotenv
import os

load_dotenv()


app = FastAPI(title="Chatbot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("="*50)
print("Environment Variables Check:")
print(f"LANGCHAIN_TRACING_V2: {os.getenv('LANGCHAIN_TRACING_V2')}")
print(f"LANGCHAIN_API_KEY: {os.getenv('LANGCHAIN_API_KEY')[:10]}...")  # First 10 chars
print(f"LANGCHAIN_PROJECT: {os.getenv('LANGCHAIN_PROJECT')}")
print("="*50)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def root():
    return {'message': "Chatbot API is running"}

# Include routers
app.include_router(tickets.router)
app.include_router(ticket_chat.router)
#app.include_router(chat.router)
#app.include_router(threads.router)


"""
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

"""    

