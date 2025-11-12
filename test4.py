from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from test3 import conv
from langchain_chroma import Chroma
load_dotenv()
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
#embeddings.embed_query(message)
doc=conv(10)
vector_store=Chroma(
    embedding_function=GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001"),
    persist_directory="chroma_db",
    collection_name="Sample"
)
vector_store.add_documents(doc)
print(vector_store.similarity_search(
    query="do i have any mails from Sameer Tiwary?",
    k=2
))

        
