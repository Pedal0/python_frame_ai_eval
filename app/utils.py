import os
import re

def load_config():
    """
    Loads configuration from environment variables.
    """
    # Tenter de charger la clé API directement à partir du fichier .env
    dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
    print(f"Looking for .env file at: {dotenv_path}")
    print(f"File exists: {os.path.exists(dotenv_path)}")
    
    # Lire directement le contenu du fichier .env
    api_key = None
    if os.path.exists(dotenv_path):
        try:
            with open(dotenv_path, 'r') as f:
                env_content = f.read()
                # Rechercher la clé API avec une expression régulière
                match = re.search(r'OPENAI_API_KEY=([^\n"]+)', env_content)
                if match:
                    api_key = match.group(1).strip()
                    print(f"Directly loaded API key from .env file: {api_key[:5]}...{api_key[-5:]}")
                else:
                    print("API key pattern not found in .env file")
        except Exception as e:
            print(f"Error reading .env file: {e}")
    
    # Configuration avec la clé directement lue du fichier
    config = {
        'openai_api_key': api_key,
        'openai_generation_model': 'gpt-4o-mini',  # Valeur par défaut
        'openai_embedding_model': 'text-embedding-3-large',  # Valeur par défaut
        'chroma_persist_directory': os.path.abspath('chromadb_data'),
        'source_documents_path': os.path.abspath('data'),
        'k_retriever': 4  # Number of documents to retrieve
    }
    
    # Vérification des autres variables dans le .env
    if os.path.exists(dotenv_path):
        try:
            with open(dotenv_path, 'r') as f:
                env_content = f.read()
                # Chercher le modèle de génération
                gen_model_match = re.search(r'OPENAI_GENERATION_MODEL=["\']?([^"\'\n]+)["\']?', env_content)
                if gen_model_match:
                    config['openai_generation_model'] = gen_model_match.group(1).strip()
                
                # Chercher le modèle d'embedding
                emb_model_match = re.search(r'OPENAI_EMBEDDING_MODEL=["\']?([^"\'\n]+)["\']?', env_content)
                if emb_model_match:
                    config['openai_embedding_model'] = emb_model_match.group(1).strip()
        except Exception as e:
            print(f"Error parsing other config values from .env: {e}")
    
    if not config['openai_api_key']:
        raise ValueError("Error: OPENAI_API_KEY not found in .env file or environment.")
    
    return config

# You can add other utility functions here if needed