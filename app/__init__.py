from flask import Flask
import os

def create_app():
    # Get base directory
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    # Configure template folder
    app = Flask(__name__,
                static_folder='../static',  # Point to static folder
                template_folder='../templates')
    
    # Rest of your existing configuration
    #app.config['UPLOAD_FOLDER'] = 'static/uploads'
    # ... rest of config
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
    
    # Initialize models
    from app.image_model import ImageRecognizer
    from app.chat_model import ChatBot
    app.image_recognizer = ImageRecognizer()
    app.chatbot = ChatBot()
    
    # Register routes
    from app.routes import configure_routes
    configure_routes(app)
    
    return app