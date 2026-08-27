from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.messages import HumanMessage, AIMessage

# Import our compiled LangGraph application
from backend.agent import agent_app

app = FastAPI(
    title="ilmLLM API",
    description="A locally scalable, industry-level chatbot API",
    version="1.0.0"
)

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str
    session_id: str

# In-memory store for session histories to demonstrate statefulness without a full DB setup
# In production, this is replaced by the LangGraph checkpointer (e.g., PostgreSQL/Redis)
session_store = {}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        session_id = request.session_id
        user_message = request.message

        # Retrieve existing history or start fresh
        if session_id not in session_store:
            session_store[session_id] = []
        
        # We append the new human message to the graph execution
        # LangGraph will manage appending this to the state
        messages_to_send = session_store[session_id] + [HumanMessage(content=user_message)]
        
        # Run the LangGraph agent
        result = agent_app.invoke({"messages": messages_to_send})
        
        # The result["messages"] contains the full history including the new AIMessage
        full_history = result["messages"]
        ai_message = full_history[-1]
        
        # Update our simple session store
        session_store[session_id] = full_history
        
        return ChatResponse(
            response=ai_message.content,
            session_id=session_id
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ilmLLM"}
