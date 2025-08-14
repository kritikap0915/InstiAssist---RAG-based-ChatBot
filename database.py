from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

# Load and split the PDF document
loader = PyPDFLoader(r"/Users/saranshtiwari/Documents/Placement Preperation/Projects/ChatBot using Llama3/Department Handbook 2024-25.pdf")
pages = loader.load_and_split()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
documents = text_splitter.split_documents(pages)

# Initialize the embedding model
embedding_function = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

db = Chroma.from_documents(documents, embedding_function, persist_directory=r"/Users/saranshtiwari/Documents/Placement Preperation/Projects/ChatBot using Llama3/chroma_db")
db.persist()