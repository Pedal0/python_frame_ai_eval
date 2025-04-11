from app import create_app
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = create_app()

if __name__ == '__main__':
    # Note: debug=True is helpful for development but should be False in production
    # Use 'flask run' command instead for production deployments with a proper WSGI server (like Gunicorn or Waitress)
    app.run(debug=True, host='0.0.0.0', port=5000)