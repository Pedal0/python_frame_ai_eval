import os
from flask import Flask
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_app():
    """
    Factory function to create and configure the Flask application.
    """
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    # Basic configuration (can be expanded)
    app.config['SECRET_KEY'] = os.urandom(24) # For session management, flash messages etc.
    app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

    if not app.config['OPENAI_API_KEY']:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    # Import and register blueprints/routes
    from . import routes
    app.register_blueprint(routes.bp)

    # Initialize RAG handler (or relevant components) if needed globally
    # from . import rag_handler
    # rag_handler.init_rag_system() # Example if initialization is needed at app start

    print("Flask app created.")
    return app
