import os 
import requests
import streamlit as st

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
)

UPLOAD_URL = f"{API_BASE_URL}/api/v1/documents/upload"
CHAT_URL = f"{API_BASE_URL}/api/v1/chat"


st.set_page_config(
    page_title="Vietnamese Banking RAG",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Vietnamese Banking Assistant")
st.caption(
    "AI-powered question answering for Vietnamese banking documents"
)


#Session state

if "messages" not in st.session_state:
    st.session_state.messages = []
    
#Sidebar

with st.sidebar:
    st.header("📄 Document Management")
    
    uploaded_file = st.file_uploader(
        "Upload a PDF document",
        type=["pdf"]
    )
    if st.button(
        "Index Document",
        use_container_width=True,
        disabled=uploaded_file is None
    ):
        with st.spinner("Processing document..."):
            try:
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "application/pdf"
                    )
                }
                
                response = requests.post(
                    UPLOAD_URL,
                    files=files,
                    timeout=300
                )
                response.raise_for_status()
                result = response.json()

                st.success("Document indexed successfully!")
                st.json(result)

                
            except requests.RequestException as e:
                st.error(f"Upload failed: {e}")
    
    st.divider()

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    
#Chat history

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant":
            sources = message.get("sources", [])

            if sources:
                with st.expander("📚 Retrieved Sources"):
                    for i, source in enumerate(sources, 1):
                        st.markdown(f"**Source {i}**")
                        st.write(
                            f"File: {source.get('source', 'Unknown')}"
                        )
                        st.write(
                            f"Page: {source.get('page', 'Unknown')}"
                        )

#Chat input

question = st.chat_input(
    "Ask a question about banking documents..."
)
if question:
    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })
    with st.chat_message("user"):
        st.markdown(question)
        
      # Call FastAPI
    with st.chat_message("assistant"):
        with st.spinner("Searching documents and generating answer..."):
            try:
                response = requests.post(
                    CHAT_URL,
                    json={"question": question},
                    timeout=120
                )

                response.raise_for_status()
                result = response.json()

                answer = result.get("answer", "No answer returned.")
                sources = result.get("sources", [])
                
                st.markdown(answer)
                
                if sources:
                    with st.expander("📚 Retrieved Sources"):
                        for i, source in enumerate(sources, 1):
                            st.markdown(f"**Source {i}**")
                            st.write(
                                f"File: {source.get('source', 'Unknown')}"
                            )
                            st.write(
                                f"Page: {source.get('page', 'Unknown')}"
                            )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })
                
            except requests.RequestException as e:
                error_message = f"Failed to connect to backend: {e}"
                st.error(error_message)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message,
                    "sources": []
                })