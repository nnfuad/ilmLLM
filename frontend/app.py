import streamlit as st
import requests
import uuid

# Configuration for the FastAPI backend
API_URL = "http://localhost:8000/chat"

st.set_page_config(page_title="ilmLLM Chat", page_icon="🧠", layout="centered")

st.title("🧠 ilmLLM - Knowledge Chatbot")
st.markdown("A locally scalable AI chatbot. Powered by FastAPI, LangGraph, and Ollama.")

# Initialize session state for memory and session ID
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask ilmLLM anything..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prepare the payload for FastAPI
    payload = {
        "message": prompt,
        "session_id": st.session_state["session_id"]
    }

    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Send POST request to FastAPI backend
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                assistant_reply = data.get("response", "No response generated.")
                message_placeholder.markdown(assistant_reply)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
            else:
                error_msg = f"Error: Backend returned status code {response.status_code}"
                message_placeholder.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                
        except requests.exceptions.ConnectionError:
            error_msg = "Error: Could not connect to the backend API. Is FastAPI running on http://localhost:8000?"
            message_placeholder.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
