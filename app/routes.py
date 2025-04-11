from flask import Blueprint, render_template, request, jsonify, current_app
from . import rag_handler
import traceback # For logging errors

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@bp.route('/chat', methods=['POST'])
def chat():
    """Handles chat messages from the user."""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "Missing 'message' in request body"}), 400

    current_app.logger.info(f"Received message: {user_message}")

    try:
        # Ensure RAG components are ready (lazy initialization if not already done)
        # This might take a moment on the very first request after server start
        rag_handler.initialize_rag_components()

        # Get the response from the RAG handler
        bot_response = rag_handler.get_rag_response(user_message)

        current_app.logger.info(f"Sending response: {bot_response}")
        return jsonify({"response": bot_response})

    except FileNotFoundError as fnf_error:
         current_app.logger.error(f"Initialization Error: {fnf_error}")
         current_app.logger.error(traceback.format_exc())
         return jsonify({"error": "Chatbot initialization failed. Please ensure the vector database is populated by running 'populate_db.py'."}), 500
    except Exception as e:
        # Log the full error for debugging
        current_app.logger.error(f"Error processing chat message: {e}")
        current_app.logger.error(traceback.format_exc())
        # Return a generic error message to the user
        return jsonify({"error": "An internal error occurred. Please try again later."}), 500
