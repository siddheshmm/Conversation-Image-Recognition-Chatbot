from flask import Flask
import os

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    app = Flask(__name__,
                static_folder='../static',  # Point to static folder
                template_folder='../templates')
    
    #app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
    
    from app.image_model import ImageRecognizer
    from app.chat_model import ChatBot
    app.image_recognizer = ImageRecognizer()
    app.chatbot = ChatBot()
    
    from app.routes import configure_routes
    configure_routes(app)
    
    return app