# RAG Chatbot Application

This is a web application demonstrating a Retrieval-Augmented Generation (RAG) chatbot. It uses Python/Flask for the backend and HTML/Tailwind CSS/JavaScript for the frontend. The chatbot answers questions based on documents provided in the `data/` directory.

## Features

- **Flask Backend:** Handles API requests and serves the frontend.
- **RAG Pipeline:** Uses LangChain to orchestrate document retrieval (from ChromaDB) and question answering (using OpenAI).
- **Vector Database:** Uses ChromaDB to store and query document embeddings (generated using OpenAI's `text-embedding-3-large`).
- **Web Interface:** A modern, colorful chat interface built with HTML, Tailwind CSS, and vanilla JavaScript.
- **Persistent Storage:** ChromaDB data is persisted locally in the `chromadb_data/` directory.
- **Configurable:** OpenAI API key and models can be configured via a `.env` file.

## Project Structure

```
app/                # Flask application package
├── __init__.py     # App factory
├── routes.py       # Flask routes (API and frontend serving)
├── rag_handler.py  # Core RAG logic (embedding, retrieval, generation)
└── utils.py        # Utility functions (e.g., config loading)
templates/          # HTML templates
├── base.html       # Base HTML structure
└── index.html      # Chat interface page
static/             # Static files (CSS, JS, images)
├── css/
│   ├── input.css   # Tailwind input CSS
│   └── style.css   # Generated Tailwind output (add to .gitignore)
├── js/
│   └── chat.js     # Frontend JavaScript for chat interaction
└── img/            # Placeholder for images (e.g., favicon)
data/               # Directory for source documents (add your .txt files here)
chromadb_data/      # Persistent storage for ChromaDB (add to .gitignore)
run.py              # Script to run the Flask development server
populate_db.py      # Script to process data and populate ChromaDB
requirements.txt    # Python dependencies
package.json        # Node.js dependencies (for Tailwind)
tailwind.config.js  # Tailwind CSS configuration
postcss.config.js   # PostCSS configuration (for Tailwind)
.env.example        # Example environment variable file
.gitignore          # Git ignore file
README.md           # This file
```

## Setup and Installation

**Prerequisites:**

- Python 3.8+ and pip
- Node.js and npm (for Tailwind CSS)
- An OpenAI API Key

**Steps:**

1.  **Clone the Repository:**

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create Python Virtual Environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install Python Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Node.js Dependencies (for Tailwind):**

    ```bash
    npm install
    ```

5.  **Configure Environment Variables:**

    - Rename `.env.example` to `.env`.
    - Open `.env` and add your OpenAI API key and models:
      ```
      OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
      OPENAI_GENERATION_MODEL="gpt-4o-mini"
      OPENAI_EMBEDDING_MODEL="text-embedding-3-large"
      ```

6.  **Add Source Documents:**

    - Create the `data/` directory if it doesn't exist.
    - Place your source documents (currently supports `.jsonl` files) inside the `data/` directory. The content of these files will be used by the chatbot.

7.  **Build Tailwind CSS:**

    - Run the build command once, or keep it running in a separate terminal during development for automatic updates:
      ```bash
      npm run build:css
      ```
      _This watches `input.css` and files specified in `tailwind.config.js` and generates `static/css/style.css`._

8.  **Populate the Vector Database:**
    - Run the script to load, chunk, embed, and store your documents in ChromaDB. This needs to be done only once initially, or whenever you update the documents in the `data/` directory.
    ```bash
    python populate_db.py
    ```
    - This will create the `chromadb_data/` directory for persistence.

## Running the Application

1.  **Ensure your Python virtual environment is active.**
    ```bash
    source venv/bin/activate # Or `venv\Scripts\activate` on Windows
    ```
2.  **Ensure the Tailwind build process is running (or has been run).**
    ```bash
    # If not already running in another terminal:
    npm run build:css
    ```
3.  **Start the Flask Development Server:**
    ```bash
    flask run
    # Or using the run.py script directly (useful for some debuggers):
    # python run.py
    ```
4.  **Access the Application:**
    Open your web browser and navigate to `http://127.0.0.1:5000` (or the address provided by Flask).

## How it Works (RAG Flow)

1.  **User Query:** The user types a message in the web interface and sends it.
2.  **API Request:** The frontend JavaScript sends the message to the Flask backend (`/chat` endpoint).
3.  **Initialization (First Request):** If not already done, the `rag_handler` initializes the OpenAI Embeddings model, loads the persistent ChromaDB vector store, initializes the OpenAI Chat model (LLM), and sets up the LangChain RAG chain.
4.  **Retrieval:** The `rag_handler` uses the user's query to find the most relevant document chunks from the ChromaDB vector store based on embedding similarity.
5.  **Augmentation:** The retrieved document chunks (context) are combined with the original user query using a specific prompt template. This template instructs the LLM to answer based _only_ on the provided context.
6.  **Generation:** The combined prompt is sent to the OpenAI LLM (e.g., `gpt-4o-mini`).
7.  **Response:** The LLM generates a response based on the query and the retrieved context.
8.  **API Response:** The Flask backend sends the LLM's response back to the frontend in JSON format.
9.  **Display:** The frontend JavaScript receives the response and displays the chatbot's message in the chat interface.

## Customization

- **Source Documents:** Add/modify `.jsonl` files in the `data/` directory and re-run `python populate_db.py`. For other file types (PDF, DOCX), you'll need to modify `populate_db.py` to use appropriate LangChain document loaders (e.g., `PyPDFLoader`).
- **Models:** Change the OpenAI models used for embeddings or generation in the `.env` file or `app/utils.py`.
- **Prompt Template:** Modify the `template` string in `app/rag_handler.py` to change how the LLM is instructed.
- **Retrieval:** Adjust the number of retrieved documents (`k_retriever`) in `app/utils.py`.
- **Styling:** Modify Tailwind classes in the HTML templates (`templates/*.html`) or adjust the `tailwind.config.js` file. Remember to rebuild the CSS (`npm run build:css`).
- **Chunking:** Experiment with `CHUNK_SIZE` and `CHUNK_OVERLAP` in `populate_db.py` for different document splitting strategies.

## Deployment (Basic Notes)

For production, do not use the Flask development server (`flask run` or `app.run(debug=True)`). Instead, use a production-grade WSGI server like Gunicorn or Waitress behind a reverse proxy like Nginx or Apache.

Example using Gunicorn:

```bash
pip install gunicorn
gunicorn --workers 4 --bind 0.0.0.0:8000 run:app
```

Remember to set `debug=False` in `run.py` or remove the `app.run()` call if using a WSGI server entry point. Ensure your `.env` file is securely managed on the production server.
