import os
import shutil
import json
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from app.utils import load_config

# Hard-coded API key (temporairement pour débugger)
# Remplacez par votre clé API OpenAI valide
# OPENAI_API_KEY = ""
# Pour le reste, on utilise la configuration normale
config = load_config()
# Utiliser la clé API depuis le fichier .env via load_config()
OPENAI_API_KEY = config['openai_api_key']
# --- Configuration ---
SOURCE_DOCUMENTS_PATH = config['source_documents_path']
CHROMA_PERSIST_DIRECTORY = config['chroma_persist_directory']
OPENAI_EMBEDDING_MODEL = config['openai_embedding_model']
# On utilise la clé API définie directement ici plutôt que celle du fichier .env
# OPENAI_API_KEY = config['openai_api_key']

# Print the API key for debugging (only the first and last 5 characters)
print(f"API Key loaded: {OPENAI_API_KEY[:5]}...{OPENAI_API_KEY[-5:]}")

# Chunking parameters
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def load_documents_from_jsonl(file_path):
    """Loads documents from a JSONL file."""
    print(f"Loading documents from JSONL file: {file_path}")
    documents = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                # Parse each line as a JSON object
                data = json.loads(line)
                # Create a document with the text content and metadata
                from langchain_core.documents import Document
                doc = Document(
                    page_content=data.get('text', ''),
                    metadata={
                        'source': data.get('source', ''),
                        'id': data.get('id', '')
                    }
                )
                documents.append(doc)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON line: {e}")
                continue
    
    print(f"Loaded {len(documents)} documents from JSONL.")
    return documents

def load_documents(directory_path):
    """Loads documents from the specified directory."""
    print(f"Loading documents from: {directory_path}")
    
    # Check for data.jsonl file first
    jsonl_file_path = os.path.join(directory_path, "data.jsonl")
    if os.path.exists(jsonl_file_path):
        print(f"Found data.jsonl file at {jsonl_file_path}")
        return load_documents_from_jsonl(jsonl_file_path)
    
    # Then check if we have a data.txt file that is in JSONL format
    jsonl_file_path = os.path.join(directory_path, "data.txt")
    if os.path.exists(jsonl_file_path):
        # First line check to see if it looks like JSONL
        with open(jsonl_file_path, 'r', encoding='utf-8') as file:
            first_line = file.readline().strip()
            try:
                # If we can parse the first line as JSON, assume it's JSONL
                json.loads(first_line)
                return load_documents_from_jsonl(jsonl_file_path)
            except json.JSONDecodeError:
                # Not JSONL, continue with regular text loading
                pass
    
    # Regular text loading with DirectoryLoader
    loader = DirectoryLoader(directory_path, glob="**/*.txt", loader_cls=TextLoader, show_progress=True, use_multithreading=True)
    documents = loader.load()
    print(f"Loaded {len(documents)} documents.")
    return documents

def split_documents(documents):
    """Splits documents into smaller chunks."""
    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        add_start_index=True, # Helpful for potential source tracking
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks.")
    return chunks

def create_and_persist_vectorstore(chunks):
    """Creates embeddings and persists them in Chroma."""
    print("Initializing OpenAI embeddings...")
    embeddings = OpenAIEmbeddings(
        model=OPENAI_EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY
    )

    # --- Chroma DB Setup ---
    # Check if the persistence directory exists and remove it to start fresh
    # Be cautious with this in production; you might want to update instead
    if os.path.exists(CHROMA_PERSIST_DIRECTORY):
        print(f"Removing existing Chroma database at: {CHROMA_PERSIST_DIRECTORY}")
        shutil.rmtree(CHROMA_PERSIST_DIRECTORY)

    print(f"Creating and persisting Chroma vector store at: {CHROMA_PERSIST_DIRECTORY}")
    # Create a new Chroma database from the documents and persist it
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PERSIST_DIRECTORY
    )
    print("Vector store created and persisted successfully.")
    return vectorstore

def main():
    """Main function to run the data population process."""
    print("--- Starting Database Population ---")

    # 1. Check if source documents exist
    if not os.path.exists(SOURCE_DOCUMENTS_PATH) or not os.listdir(SOURCE_DOCUMENTS_PATH):
        print(f"Error: Source documents directory '{SOURCE_DOCUMENTS_PATH}' is empty or does not exist.")
        print("Please create the 'data' directory and add your source text files (.txt) there.")
        return

    # 2. Load documents
    documents = load_documents(SOURCE_DOCUMENTS_PATH)
    if not documents:
        print("No documents loaded. Exiting.")
        return

    # 3. Split documents
    chunks = split_documents(documents)
    if not chunks:
        print("No chunks created. Exiting.")
        return

    # 4. Create and persist vector store
    try:
        create_and_persist_vectorstore(chunks)
    except Exception as e:
        print(f"An error occurred during vector store creation: {e}")
        # Consider more specific error handling based on potential Chroma/OpenAI errors
        return

    print("--- Database Population Complete ---")

if __name__ == "__main__":
    main()