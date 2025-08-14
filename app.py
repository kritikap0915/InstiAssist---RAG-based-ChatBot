import streamlit as st
from langchain_community.llms import Ollama 
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import asyncio

# Initialize the embedding model
embedding_function = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

# Load the Chroma DB with precomputed embeddings
db = Chroma(persist_directory=r"/Users/saranshtiwari/Documents/Placement Preperation/Projects/ChatBot using Llama3/chroma_db", 
            embedding_function=embedding_function)

# Initialize the LLaMA model (ensure the model is optimized for speed, such as quantized or smaller version)
llm = Ollama(model="llama3.1")

st.set_page_config(
    page_title="InstiAssit ChatBot",
    page_icon="🦙",
    layout="centered"
)

with st.sidebar:
    st.title('🦙 InstiAssit - RAG based Chatbot 💬')
    st.write('This chatbot is created using the open-source LlaMa 3.1 from Meta.')
    st.write('It provides information related to student queries in IIT Bombay.')
    st.write('© Saransh Tiwari')

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Enter your prompt:")

if prompt:
    # Add user's question to chat and display it
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # Use asynchronous function for faster response time
    async def get_response():
        # Perform similarity search, adjust 'k' for faster retrieval
        docs = db.similarity_search(prompt, k=2)
        retrieved_contexts = "\n\n".join([f"Context {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])

        # Create a custom prompt with context
        custom_prompt = f"""Question: {prompt}
        
        Context: {retrieved_contexts}
        Answer the student's question using the context provided if relevant, otherwise rely on your general knowledge.
        """

        response = llm.invoke(custom_prompt)
        return response

    # Display loading spinner while processing the response
    with st.spinner("Generating response..."):
        response = asyncio.run(get_response())
        st.session_state.chat_history.append({"role": "assistant", "content": response})

    # Display the response in the chat
    with st.chat_message("assistant"):
        st.write(response)