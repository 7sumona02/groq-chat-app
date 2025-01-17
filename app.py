import streamlit as st
import os
from groq import Groq
import random

from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = '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'

def main():
    st.title("Groq Chat App")

    # Add customization options to the sidebar
    st.sidebar.title('Select an LLM')
    model = st.sidebar.selectbox(
        'Choose a model',
        ['mixtral-8x7b-32768', 'llama2-70b-4096']
    )
    conversational_memory_length = st.sidebar.slider('Conversational memory length:', 1, 10, value=5)

    memory = ConversationBufferWindowMemory(k=conversational_memory_length)

    user_question = st.text_area("Ask a question:")

    # Session state variable to hold chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    else:
        for message in st.session_state.chat_history:
            memory.save_context({'input': message['human']}, {'output': message['AI']})

    # Initialize Groq Langchain chat object and conversation
    groq_chat = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name=model
    )

    conversation = ConversationChain(
        llm=groq_chat,
        memory=memory
    )

    # Add a button to submit the question
    if st.button("Ask"):
        if user_question:
            response = conversation(user_question)
            message = {'human': user_question, 'AI': response['response']}
            st.session_state.chat_history.append(message)
            st.write("Chatbot:", response['response'])
        else:
            st.warning("Please enter a question before clicking 'Ask'.")

if __name__ == "__main__":
    main()