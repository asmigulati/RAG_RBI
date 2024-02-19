import streamlit as st
import requests

st.title("RAG RBI_Notifications Chatbot")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "references" not in st.session_state:
    st.session_state.references = []

# Function to send a message to the API and get the response
def send_message(message):
    response = requests.post("https://1400-110-224-70-196.ngrok-free.app/query", json={"query": message})
    return response.json()

# Display the chatbot response in the chat
def display_response(response):
    with st.chat_message("assistant"):
        st.markdown(response["response"])
    st.session_state.messages.append({'role': 'assistant', 'content': response["response"]})

# If there are no previous messages, display dummy questions
if not st.session_state.messages:
    st.write("Try asking a question from the suggestions below or type your own:")
    dummy_questions = [
        "What are SBRs for NBFCs",
        "What is the requirement for the Financial Assets Acquisition Policy",
        "What is the purpose of the Securitisation Companies and Reconstruction Companies guidelines?",
        "what is the Pradhan Mantri Rozgar Yojana scheme?"
    ]
    cols = st.columns(4)
    for i, question in enumerate(dummy_questions):
        with cols[i]:
            if st.button(question):
                st.session_state.messages.append({'role': 'user', 'content': question})
                response = send_message(question)
                st.session_state.messages.append({'role': 'assistant', 'content': response["response"]})

                st.session_state.references = response["node_texts"]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("What is up?")
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({'role': 'user', 'content': user_input})

    # Clear previous references
    st.session_state.references = []

    # Show loading spinner while waiting for the response
    with st.spinner("Waiting for response..."):
        response = send_message(user_input)
        display_response(response)

    # Store new references
    st.session_state.references = response["node_texts"]

# Display new references as dropdowns
for i, node_text in enumerate(st.session_state.references):
    with st.expander(f"Reference {i+1}"):
        st.write(node_text)
